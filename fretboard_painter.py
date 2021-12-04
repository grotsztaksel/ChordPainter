# -*- coding: utf-8 -*-
"""
Created on 04.12.2021 22:00 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['FretboardPainter']
__date__ = '2021-12-04'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QSize, QPoint, QRect
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

        self.chordNotes = None

        self.p = QPainter()
        self.pixmap = None

        self.fontSize = 8
        self.size = size
        self.setFontSize(self.fontSize)

        self.fret0Position = QPoint(0, 0)
        self.scaleLength = 0

        self.string_thickness = 2  # width of the string lines (pixels)
        self.string_color = QColor(Qt.black)
        self.dotSize = 0.5  # fraction of the distance between strings
        self.bar_zero_width = 8  # width of the 0-th fret (pixels)
        self.fret_line_width = 2

    def setFontSize(self, size):
        """Set font size. Basing on that, set the overall size of the picture"""
        self.fontSize = size
        self.fret0Position = (self.fontSize / 0.8)
        d = self.calculateFretboardLength(self.fontSize, self.instrument.nfrets)

        h = self.fret0Position + d

        size = QSize(self.size.width(), h)
        self.setSize(size)
        # Add space for the open string annotation

    def calculateFretboardLength(self, fontSize, nfrets):
        # Determine the scale length (length of a string in pixels)
        w = self.fret0Position * 1.4  # size of the last fret. Has enough space for the notes annotation.
        # d = s - (s/(2^(n/12))) is the formula for the fret distance from the nut
        # therefore fret width:
        # w = s - (s/(2^(n/12))) - s - (s/(2^(n-1/12)))
        # Therefore
        # s = w / (  1/(2^(n/12)) - 1/(2^((n-1)/12)) )
        n = nfrets  # for shorter notation
        s = w / (1 / (2 ^ (n / 12)) - 1 / (2 ^ ((n - 1) / 12)))
        self.scaleLength = s
        d = s - (s / (2 ^ (n / 12)))  # This is the length of the entire fretboard.

        return d

    def fretPos(self, ifret):
        """
        Return position of a fret in the pixmap. Formula taken from https://www.liutaiomottola.com/formulae/fret.htm
        """
        d = self.scaleLength - (self.scaleLength / (2 ^ (ifret / 12)))
        return self.fret0Position.y() + d

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

    def setChordNotes(self, notes):
        """
        Define a set of notes that belong to the chord whose notes are marked. The first note is the root note of a
        chord
        """
        self.chordNotes = notes

    def drawDot(self, fret):
        radius = int(self.dotSize * self.parent.pos_string[0])

        center = self.fretRect(fret).center()
        if not self.fretBoard.contains(center):
            return
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

    def fretRect(self, fret):
        top = self.fretPos(fret - 1)
        bottom = self.fretPos(fret)
        left = self.p.viewport().left()
        right = self.p.viewport().right()
        return QRect(QPoint(left, top), QPoint(right, bottom))

    def drawString(self, i):
        """
        Draw the ith string, including its note annotations
        """
        font = self.p.font()
        font.setPixelSize(self.fontSize)
        self.p.setFont(font)

        nstrings = len(self.instrument.strings)
        w = self.p.viewport().width()

        openNote = self.instrument.strings[i]
        ibase = NOTES.index(openNote)
        rootFret = self.instrument.rootfrets[i]

        l = self.p.viewport().left() + (i + 0) * (w / nstrings)
        r = self.p.viewport().left() + (i + 1) * (w / nstrings)

        nutPos = self.fretPos(rootFret)

        # Rectangle for the open string note annotation

        top = nutPos - (r - l)

        rect = QRect(l, top, (r - l), (r - l))
        height = rect.height()
        size = rect.size()
        c = rect.center().x()

        self.annotateNote(openNote, rect)

        # Draw the string
        pen = self.p.pen()
        pen.setColor(self.string_color)
        pen.setWidth(self.string_thickness)
        pen.setStyle(Qt.SolidLine)
        self.p.setPen(pen)
        self.p.drawLine(QPoint(c, nutPos), QPoint(c, self.p.viewport().bottom()))

        # Draw the 0-th fret bar
        pen.setWidth(self.bar_zero_width)
        self.p.setPen(pen)
        self.p.drawLine(QPoint(l, nutPos), QPoint(r, nutPos))

        for i in range(1, self.instrument.nfrets + 1):
            noteName = NOTES[(ibase + i) % 12]
            fretCenter = self.fretRect(i).center()
            fretBottom = self.fretRect(i).bottom()

            pen.setWidth(self.fret_line_width)
            self.p.setPen(pen)
            self.p.drawLine(QPoint(l, fretBottom), QPoint(r, fretBottom))

            rect = QRect(QPoint(l, fretCenter - height / 2), size)
            self.annotateNote(noteName, rect)

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
            pen.setColor(Qt.white)
            font.setBold(True)
        elif isChordNote:
            brush.setColor(Qt.white)
            pen.setColor(Qt.black)
            font.setBold(False)
        else:
            brush.setColor(Qt.white)
            pen.setColor(Qt.black)
            pen.setStyle(Qt.NoPen)
            font.setBold(False)

        self.p.setFont(font)
        self.p.setPen(pen)
        self.p.setBrush(brush)

        self.p.drawEllipse(rect)

        pen.setStyle(Qt.SolidLine)
        self.p.drawText(rect, Qt.AlignCenter, noteName)

        self.p.setFont(font_old)
        self.p.setPen(pen_old)
        self.p.setBrush(brush_old)
