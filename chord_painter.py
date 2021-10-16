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

        self.string_thickness = 2  # width of the string lines (pixels)

        self.nfrets = 5  # number of frets visible

        self.openStringMarkSize = 20  # pixels
        self.muteStringMarkSize = 20  # pixels

        self.firstFretVisible = 0

        self.pos_string = []
        self.pos_fret = []

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



    def size(self):
        return self.pixmap.size()

    def drawChord(self):
        for s, i in enumerate(self.chord.scheme):
            if not isinstance(s, int):
                s = s[0]
            if s < 0:
                self.drawMuteString(i)
            elif s == 0:
                self.drawOpenString(i)
            else:
                self.drawFinger(i)

    def drawStrings(self):
        string_thickness = 2
        string_color = QColor(Qt.black)

        w = self.pixmap.width()
        h = self.pixmap.height()

        n = len(self.chord)
        offset = w / n
        margin = int(0.5 * offset)

        self.pos_string = [margin + i * offset for i in range(n)]

        pen = self.p.pen()
        pen.setColor(string_color)
        pen.setWidth(string_thickness)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)

        for sp in self.pos_string:
            self.p.drawLine(sp, margin, sp, h - margin)

    def drawFrets(self):
        color = QColor(Qt.black)
        bar_zero_width = 4  # width of the 0-th fret (pixels)
        fret_line_width = 2
        next_fret_fragment = 0.1  # draw the strings little bit longer than to the last fret, so thay slightly extend
        #                           (by a fraction of the fret width)

        h = self.pixmap.height()
        fret_first = int(max(self.muteStringMarkSize, self.openStringMarkSize) * 1.1)
        fingerboard_length = h - fret_first
        self.fret_width = int((fingerboard_length) / (self.nfrets + next_fret_fragment))
        self.pos_fret = [fret_first + i * self.fret_width for i in range(self.nfrets + 1)]

        # Draw all frets
        pen = self.p.pen()
        pen.setWidth(fret_line_width)
        pen.setStyle(Qt.SolidLine)
        pen.setColor(color)
        self.p.setPen(pen)
        for f in self.pos_fret:
            self.p.drawLine(self.pos_string[0], f, self.pos_string[-1], f)

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
                "Chord {} diagram cannot be shown on range of {} frets".format(self.chord.name, self.nfrets))

        if fret_max <= self.nfrets:
            self.firstFretVisible = 0
            # Draw the 0th fret
            pen = self.p.pen()
            pen.setWidth(bar_zero_width)
            pen.setStyle(Qt.SolidLine)
            pen.setColor(color)
            self.p.setPen(pen)
            self.p.drawLine(self.pos_fret[0], self.pos_string[0], self.pos_fret[0], self.pos_string[-1])
        else:
            self.firstFretVisible = fret_min - 1

    def drawFinger(self, istring):
        margin = 0
        color = QColor(Qt.black)
        offsetFromFret = 0.2  # Of the fret width
        labelFinger = False
        labelColor = QColor(Qt.white)
        pen = self.p.pen()
        brush = QBrush()
        brush.setColor(color)

        pen.setColor(color)
        pen.setBrush(brush)
        self.p.setPen()

        rect = self._getMarkerRect(istring, margin)
        fret = self.chord.scheme(istring)
        if isinstance(fret, int):
            finger = None
        else:
            finger = fret[1]
            fret = fret[0]

        rect.moveBottom(self.pos_fret[fret - self.firstFretVisible] - int(self.fret_width * offsetFromFret))

        self.p.drawEllipse(rect)

        if finger not in list(range(5)) or not labelFinger:
            return

        pen = self.p.pen()
        pen.setColor(labelColor)
        self.p.setPen(pen)

        self.p.drawText(rect, Qt.AlignCenter, str(finger), rect)

    def drawOpenString(self, istring):
        lineWidth = 2
        margin = 2
        pen = self.p.pen()
        pen.setBrush(Qt.NoBrush)
        pen.setWidth(lineWidth)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)

        self.p.drawEllipse(self._getMarkerRect(istring, margin))

    def drawMuteString(self, istring):
        lineWidth = 2
        margin = 2
        pen = self.p.pen()
        pen.setBrush(Qt.NoBrush)
        pen.setWidth(lineWidth)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)

        rect = self._getMarkerRect(istring, margin)

        self.p.drawLine(rect.topLeft(), rect.bottomRight())
        self.p.drawLine(rect.topRight(), rect.bottomLeft())

    def drawFretDot(self, fret):
        color = QColor(Qt.gray)
        size = 0.8  # fraction of the distance between strings

        radius = size * self.pos_string[0]

        center = self._fretRect(fret).center()
        topLeft = center - QPoint(radius, radius)
        bottomRight = center + QPoint(radius, radius)

        pen = self.p.pen()
        brush = QBrush()
        brush.setColor(color)
        pen.setStyle(Qt.NoPen)
        pen.setBrush(brush)
        self.p.setPen(pen)

        self.p.drawEllipse(QRect(topLeft, bottomRight))

    def _getMarkerRect(self, istring, margin):
        topLeft = QPoint(self.pos_string[istring] - self.openStringMarkSize / 2 + margin,
                         margin)
        bottomRight = QPoint(self.pos_string[istring] + self.openStringMarkSize / 2 - margin,
                             self.openStringMarkSize - margin)
        rect = QRect(topLeft, bottomRight)
        return rect

    def _fretRect(self, fret):
        """
        Returns a rectangle representing a given fret.
        The rectangle position takes the firstFretVisible into consideration
        """

        # Basic fret rectangle:
        rect = QRect(self.pos_string[0], self.pos_fret[0], self.pos_string[-1], self.pos_fret[1])

        rect.moveBottom(rect.height() * (fret - 1 - self.firstFretVisible))
