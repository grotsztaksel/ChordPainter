# -*- coding: utf-8 -*-
"""
Created on 12.10.2021 21:57 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['ChordPainter']
__date__ = '2021-10-12'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QSize, QPoint, QRect
from PyQt5.QtGui import QColor, QPainter, QPixmap, QBrush, QImage

from chord import Chord


class ChordPainter(object):
    """
    The class actually responsible for painting the chord scheme and saving image files from them
    """

    def __init__(self, chord=None, size=None):

        self.p = QPainter()
        self.setChord(chord)
        self.setSize(size)

        topMargin = 0.15
        rightMargin = 0.15
        # Use only a part of the available space to draw the fretboard: leave some margins for open/mute string marks
        # and for fret numbering, if the diagram does not start at fret 0

        offset_w = int(-rightMargin * float(self.pixmap.width()))
        offset_h = int(topMargin * float(self.pixmap.height()))
        self.fretBoard = self.pixmap.rect().adjusted(0, offset_h,
                                                     offset_w, 0)

        self.nfrets = 5  # number of frets visible

        self.firstFretVisible = 0

        self.strings = StringPainter(self)
        self.frets = FretPainter(self)
        self.symbols = SymbolPainter(self)

        self.pos_fret = self.frets.getFretPositions(self.nfrets)
        self.pos_string = self.strings.getStringPositions()

        # pen = self.p.pen()
        # pen.setColor(QColor(Qt.green))
        # self.p.setPen(pen)
        # self.p.drawRect(self.fretBoard)
        # pen.setColor(QColor(Qt.magenta))
        # brush = QBrush(QColor(Qt.blue))
        #
        # pen.setBrush(brush)
        # self.p.setPen(pen)
        #
        # self.p.drawRect(QRect(self.pixmap.rect().topLeft(), self.fretBoard.topRight()))

    def setChord(self, chord):
        """
        Set the chord scheme
        """
        assert isinstance(chord, Chord)
        self.chord = chord

    def setSize(self, size: QSize):
        """
        Set the size of the output image
        """
        if size is None:
            return
        self.pixmap = QPixmap(size)
        self.pixmap.fill(QColor(Qt.white))
        self.p.begin(self.pixmap)
        self.p.setRenderHint(QPainter.Antialiasing)

    def size(self):
        return self.pixmap.size()

    def drawChord(self):
        for s, i in enumerate(self.chord.scheme):
            if not isinstance(s, int):
                s = s[0]
            if s < 0:
                self.symbols.drawMuteString(i)
            elif s == 0:
                self.symbols.drawOpenString(i)
            else:
                self.symbols.drawFinger(i)


class AbstractPainter(object):
    def __init__(self, parent: ChordPainter):
        self.parent = parent
        self.chord = parent.chord
        self.nfrets = parent.nfrets
        self.fretBoard = parent.fretBoard
        self.p = parent.p
        self.pixmap = self.p.device()
        self.size = None
        self.color = None

    def draw(self):
        raise NotImplementedError

    def fretRect(self, fret):
        fret_width = self.parent.pos_fret[1] - self.fretBoard.top()
        fret_pos = self.parent.pos_fret[fret - 1] - self.parent.firstFretVisible
        return QRect(self.fretBoard.left(), fret_pos, self.fretBoard.width(), fret_width)

    def stringOffset(self):
        return 2 * (self.parent.pos_string[0] - self.fretBoard.left())


class StringPainter(AbstractPainter):
    def __init__(self, parent):
        super(StringPainter, self).__init__(parent)
        self.string_thickness = 2  # width of the string lines (pixels)
        self.color = QColor(Qt.black)

    def getStringPositions(self):
        n = len(self.chord)
        offset = self.fretBoard.width() / n
        margin = int(0.5 * offset)

        return [int(self.fretBoard.left() + margin + i * offset) for i in range(n)]

    def draw(self):
        pen = self.p.pen()
        pen.setColor(self.color)
        pen.setWidth(self.string_thickness)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)

        for sp in self.parent.pos_string:
            self.p.drawLine(sp, self.fretBoard.top(), sp, self.fretBoard.bottom())


class FretPainter(AbstractPainter):
    def __init__(self, parent):
        super().__init__(parent)
        self.color = QColor(Qt.black)
        self.dotColor = QColor(Qt.gray)
        self.dotSize = 0.8  # fraction of the distance between strings
        self.bar_zero_width = 4  # width of the 0-th fret (pixels)
        self.fret_line_width = 2
        self.next_fret_fragment = 0.1  # draw the strings little bit longer than to the last fret, so they are slightly
        #                                extended (by a fraction of the fret width)

    def getFretPositions(self, nfrets):
        fret_width = int(self.fretBoard.height() / float(nfrets + self.next_fret_fragment))
        return [self.fretBoard.top() + i * fret_width for i in range(nfrets + 1)]

    def draw(self):
        pen = self.p.pen()
        pen.setWidth(self.fret_line_width)
        pen.setStyle(Qt.SolidLine)
        pen.setColor(self.color)
        self.p.setPen(pen)
        for f in self.parent.pos_fret:
            self.p.drawLine(self.parent.pos_string[0], f, self.parent.pos_string[-1], f)

        # If the zeroth fret is visible on the diagram (i.e the diagram does not start from, for example, fret III,
        # draw the bar
        frets_used = []
        for string in self.chord.scheme:
            if isinstance(string, int):
                s = string
            else:
                s = string[0]
            frets_used.append(s)

        fret_max = max(frets_used)
        fret_min = fret_max
        for fret in frets_used:
            if fret > 0 and fret < fret_min:
                fret_min = fret

        if fret_max - fret_min > self.nfrets:
            raise ValueError(
                "Chord {} diagram cannot be shown on range of {} frets".format(self.chord.name,
                                                                               self.nfrets))

        if fret_max <= self.nfrets:
            self.parent.firstFretVisible = 0
            # Draw the 0th fret
            pen = self.p.pen()
            pen.setWidth(self.bar_zero_width)
            pen.setStyle(Qt.SolidLine)
            pen.setColor(self.color)
            self.p.setPen(pen)
            self.p.drawLine(self.parent.pos_string[0], self.fretBoard.top(),
                            self.parent.pos_string[-1], self.fretBoard.top())
        else:
            self.parent.firstFretVisible = fret_min - 1

    def drawDot(self, fret):
        radius = int(self.dotSize * self.parent.pos_string[0])

        center = self.fretRect(fret).center()
        topLeft = center - QPoint(radius, radius)
        bottomRight = center + QPoint(radius, radius)

        pen = self.p.pen()
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.dotColor)
        pen.setStyle(Qt.NoPen)
        pen.setBrush(brush)
        self.p.setBrush(brush)
        self.p.setPen(pen)

        self.p.drawEllipse(QRect(topLeft, bottomRight))

    def drawFretNumber(self):
        if self.parent.firstFretVisible == 0:
            return
        rom = int_to_roman(self.parent.firstFretVisible)
        pen = self.p.pen()
        pen.setWidth(self.bar_zero_width)
        pen.setStyle(Qt.SolidLine)
        pen.setColor(self.color)
        self.p.setPen(pen)

        width = self.pixmap.rect().right() - self.parent.pos_string[-1]
        height = width
        topLeft = QPoint(self.parent.pos_string[-1], self.fretBoard.top())
        bottomRight = QPoint(self.pixmap.rect().right(), topLeft.y() + height)

        rect = QRect(topLeft, bottomRight)

        font = self.p.font()
        font.setFamily("Times New Roman")
        font.setPixelSize(rect.height())
        self.p.setFont(font)

        # self.p.drawRect(rect)
        self.p.drawText(rect, Qt.AlignCenter, rom)


class SymbolPainter(AbstractPainter):
    def __init__(self, parent):
        super().__init__(parent)
        self.color = QColor(Qt.black)
        self.fingerNumberColor = QColor(Qt.white)
        self.lineWidth = 2  # Line width for the open and mute string symbols ('x' and 'o')
        self.margin = 6
        self.fingerOnFretWidth = 0.7  # Percentage of the where the finger marker should be painted

    def drawFinger(self, istring, fret, finger=None):
        fret = self.fretRect(fret)

        symbolCenter = QPoint(self.parent.pos_string[istring],
                              fret.top() + self.fingerOnFretWidth * fret.height())
        topLeft = symbolCenter - QPoint(0.5 * self.stringOffset(), 0.5 * self.stringOffset())
        bottomRight = symbolCenter + QPoint(0.5 * self.stringOffset(), 0.5 * self.stringOffset())

        pen = self.p.pen()
        pen.setStyle(Qt.NoPen)

        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)

        self.p.setBrush(brush)
        self.p.setPen(pen)
        rect = QRect(topLeft, bottomRight)
        self.p.drawEllipse(rect)

        if finger is None:
            return

        brush.setColor(self.fingerNumberColor)
        pen.setColor(self.fingerNumberColor)
        pen.setStyle(Qt.SolidLine)
        pen.setBrush(brush)
        pen.setColor(brush.color())
        font = self.p.font()
        font.setPixelSize(rect.height() * 0.8)

        self.p.setFont(font)
        self.p.setPen(pen)
        self.p.setBrush(brush)

        self.p.drawText(rect, Qt.AlignCenter, str(finger))
        print("Drawint text")

    def drawOpenString(self, istring):
        pen = self.p.pen()
        brush = QBrush(Qt.NoBrush)
        pen.setColor(self.color)
        pen.setWidth(self.lineWidth)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)
        self.p.setBrush(brush)

        self.p.drawEllipse(self._getMarkerRect(istring, self.margin))

    def drawMuteString(self, istring):
        pen = self.p.pen()
        brush = QBrush(Qt.NoBrush)

        pen.setWidth(self.lineWidth)
        pen.setStyle(Qt.SolidLine)

        self.p.setPen(pen)
        self.p.setBrush(brush)

        rect = self._getMarkerRect(istring, self.margin)

        self.p.drawLine(rect.topLeft(), rect.bottomRight())
        self.p.drawLine(rect.topRight(), rect.bottomLeft())

    def _getMarkerRect(self, istring, margin):
        markerSize = int(0.8 * self.stringOffset())
        bottomRight = QPoint(self.parent.pos_string[istring] + markerSize / 2,
                             self.fretBoard.top() - margin)

        topLeft = bottomRight - QPoint(markerSize, markerSize)

        rect = QRect(topLeft, bottomRight)
        return rect


def int_to_roman(input):
    """
    Convert an integer to a Roman numeral. 
    Copy-pasted from https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html
    """

    if not isinstance(input, type(1)):
        raise (TypeError, "expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise (ValueError, "Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)
