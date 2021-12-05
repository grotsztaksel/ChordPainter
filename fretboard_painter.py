# -*- coding: utf-8 -*-
"""
Created on 04.12.2021 22:00 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['FretboardPainter']
__date__ = '2021-12-04'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QSize, QPoint, QRect, QMargins
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen

from music_theory import NOTES


class FretboardPainter(object):
    """
    An object drawing the image of the whole fretboard of a string instrument. It can also mark notes belonging to a
    selected chord
    """

    def __init__(self, size, instrument):
        self.instrument = instrument
        self.offsets = None

        self.chordNotes = ["A", "C", "E"]

        self.p = QPainter()
        self.fretBoardRect = QRect()  # Rectangle of the fretboard itself (smaller than the viewport, using margins)
        self.pixmap = None

        self.fontSize = 12
        self.fingerCircleSizeFactor = 1 / 0.6  # How many times the circle in which the note is inscribed is larger than
        # the font size
        self.fret0Position = 0
        self.scaleLength = 0

        self.size = size
        self.setFontSize(self.fontSize)

        self.string_thickness = 1  # width of the string lines (pixels)
        self.string_color = QColor(Qt.black)
        self.bar_zero_width = 6  # width of the 0-th fret (pixels)
        self.fret_line_width = 2
        self.dotColor = QColor(Qt.gray)

        if self.instrument is not None:
            for dotFret in self.instrument.dotsOnFrets:
                self.drawDot(dotFret)
        for i, s in enumerate(self.instrument.strings):
            self.drawString(i)

    def setFontSize(self, size):
        """Set font size. Basing on that, set the overall size of the picture"""
        self.fontSize = size
        self.fret0Position = self.fontSize * self.fingerCircleSizeFactor
        d = self.calculateFretboardLength(self.fontSize, self.instrument.nfrets)

        h = self.fret0Position + d

        size = QSize(self.size.width(), h)
        self.setSize(size)

    def calculateFretboardLength(self, fontSize, nfrets):
        # Determine the scale length (length of a string in pixels)
        w = self.fret0Position  # size of the last fret. Has enough space for the notes annotation.
        # d = s - (s/(2^(n/12))) is the formula for the fret distance from the nut
        # therefore fret width:
        # w = s - (s/(2^(n/12))) - s - (s/(2^(n-1/12)))
        # Therefore
        # s = w / (  1/(2^(n/12)) - 1/(2^((n-1)/12)) )
        n = nfrets  # for shorter notation
        s = w / (1 / pow(2, ((n) / 12)) - 1 / pow(2, ((n + 1) / 12)))
        self.scaleLength = s
        d = s - (s / pow(2, (n / 12)))  # This is the length of the entire fretboard.

        return d

    def fretPos(self, ifret):
        """
        Return position of a fret in the pixmap. Formula taken from https://www.liutaiomottola.com/formulae/fret.htm
        """
        d = self.scaleLength - (self.scaleLength / pow(2, (ifret / 12)))
        return self.fret0Position + d

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
        self.fretBoardRect = self.p.viewport().marginsRemoved(QMargins(5, 5, 5, 5))

    def setChordNotes(self, notes):
        """
        Define a set of notes that belong to the chord whose notes are marked. The first note is the root note of a
        chord
        """
        self.chordNotes = notes

    def drawDot(self, fret):
        radius = 8

        center = self.fretRect(fret).center()
        if not self.fretBoardRect.contains(center):
            return
        topLeft = center - QPoint(radius, radius)
        bottomRight = center + QPoint(radius, radius)
        dots = 1
        rect = QRect(topLeft, bottomRight)

        if fret == 12:
            dots = 2
            rect.moveLeft(0.2 * self.fretRect(fret).width())

        pen = self.p.pen()
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.dotColor)
        pen.setStyle(Qt.NoPen)
        pen.setBrush(brush)
        self.p.setBrush(brush)
        self.p.setPen(pen)

        for i in range(dots):
            # Draw 2 dots for the 12th fret and one for the others
            self.p.drawEllipse(rect)
            rect.moveRight(0.8 * self.fretRect(fret).width())

    def fretRect(self, fret):
        top = self.fretPos(fret - 1)
        bottom = self.fretPos(fret)
        left = self.fretBoardRect.left()
        right = self.fretBoardRect.right()
        return QRect(QPoint(left, top), QPoint(right, bottom))

    def drawString(self, i):
        """
        Draw the ith string, including its note annotations
        """
        font = self.p.font()
        font.setPixelSize(self.fontSize)
        self.p.setFont(font)

        openNote = self.instrument.strings[i]
        ibase = NOTES.index(openNote)

        rect = self.getNoteRect(i, self.instrument.rootfrets[i])

        # Draw the 0-th fret bar
        pen = self.p.pen()
        pen.setWidth(self.bar_zero_width)
        pen.setColor(Qt.black)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)

        self.p.drawLine(rect.bottomLeft(), rect.bottomRight())

        # Annotate the open string note
        self.annotateNote(openNote, self.square(rect))

        # For each fret, draw the segments of strings (break them to make room for the note annotations) frets
        # and the note annotations
        for f in range(self.instrument.rootfrets[i] + 1, self.instrument.nfrets + 1):
            noteName = NOTES[(ibase - self.instrument.rootfrets[i] + f) % 12]
            fretRect = self.fretRect(f)

            # Draw the fret
            pen.setWidth(self.fret_line_width)
            pen.setColor(Qt.black)
            pen.setStyle(Qt.SolidLine)
            self.p.setPen(pen)
            self.p.drawLine(fretRect.bottomLeft(), fretRect.bottomRight())

            # Draw the note
            rect = self.getNoteRect(i, f)

            self.annotateNote(noteName, self.square(rect))

            # Draw two segments of the string - before and after the note
            pen.setWidth(self.string_thickness)
            pen.setColor(self.string_color)
            self.p.setPen(pen)
            self.p.drawLine(QPoint(rect.center().x(), fretRect.top()), QPoint(rect.center().x(), rect.top()))
            self.p.drawLine(QPoint(rect.center().x(), fretRect.bottom()), QPoint(rect.center().x(), rect.bottom()))

    @staticmethod
    def square(rect, maximize=False):
        """
        Return a square with the center in the center the same as the input rectangle. With the size adjusted to match
        the largest (maximize = True) or smallest (maximize = False) side of the inpiut rect
        """
        c = rect.center()
        rect = QRect(rect)
        w = rect.width()
        h = rect.height()
        if maximize:
            s = max(w, h)
        else:
            s = min(w, h)
        rect.setSize(QSize(s, s))
        rect.moveCenter(c)
        return rect

    def getNoteRect(self, i, fret):
        """
        Returns the rectangle in which the note annotation should be inscribed. The rectangle top/bottom/center can
        also be used as points for, for example, string fragments
        """
        nstrings = len(self.instrument.strings)
        w = self.fretBoardRect.width()
        l = self.fretBoardRect.left() + (nstrings - i - 1) * (w / nstrings)
        r = self.fretBoardRect.left() + (nstrings - i + 0) * (w / nstrings)
        bottom = self.fretPos(fret)
        h = self.fontSize * self.fingerCircleSizeFactor
        top = bottom - h - 2
        rect = QRect(l, top, (r - l), h)
        return rect

    def annotateNote(self, noteName, rect):
        """
        Draw the note annotation. Adjust styling to whether:
        - The note does belong to a chord
        - The note is a root note of the chord
        - The note does not belong to the chord
        """
        isRootNote = False
        isChordNote = False
        if self.chordNotes is not None:
            if noteName == self.chordNotes[0]:
                isRootNote = True
            elif noteName in self.chordNotes:
                isChordNote = True
        brush_old = self.p.brush()
        pen_old = self.p.pen()
        font_old = self.p.font()
        brush = self.p.brush()
        pen = self.p.pen()
        font = self.p.font()
        if isRootNote:
            brush.setColor(Qt.black)
            brush.setStyle(Qt.SolidPattern)
            pen.setStyle(Qt.NoPen)
            font.setBold(True)
            textColor = QColor(Qt.white)
        elif isChordNote:
            brush.setColor(QColor(Qt.darkGray).darker(120))
            brush.setStyle(Qt.SolidPattern)
            pen.setStyle(Qt.NoPen)
            font.setBold(False)
            textColor = QColor(Qt.white)
        else:
            brush.setStyle(Qt.NoBrush)
            pen.setColor(Qt.black)
            pen.setStyle(Qt.NoPen)
            font.setBold(False)
            textColor = QColor(Qt.black)

        self.p.setFont(font)
        self.p.setPen(pen)
        self.p.setBrush(brush)

        self.p.drawEllipse(rect)

        pen.setStyle(Qt.SolidLine)
        pen.setColor(textColor)
        self.p.setPen(pen)
        self.p.drawText(rect, Qt.AlignCenter, noteName)

        self.p.setFont(font_old)
        self.p.setPen(pen_old)
        self.p.setBrush(brush_old)
