# -*- coding: utf-8 -*-
"""
Created on 04.12.2021 22:00 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['FretboardPainter']
__date__ = '2021-12-04'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QColor, QPainter


class FretboardPainter(object):
    """
    An object drawing the image of the whole fretboard of a string instrument. It can also mark notes belonging to a
    selected chord
    """

    def __init__(self, instrument):
        self.instrument = instrument
        self.offsets = None

        self.chordNotes = None

        self.p = QPainter()
        self.pixmap = None

        self.fontSize = 8
        self.setFontSize(self.fontSize)

    def setFontSize(self, size):
        """Set font size. Basing on that, set the overall size of the picture"""
        self.fontSize = size

        d = self.calculateFretboardLength(self.fontSize, self.instrument.nfrets)

        # Add space for the open string annotation

    @staticmethod
    def calculateFretboardLength(fontSize, nfrets):
        # Determine the scale length (length of a string in pixels)
        w = (fontSize / 0.8) * 1.4  # size of the last fret
        # d = s - (s/(2^(n/12))) is the formula for the fret distance from the nut
        # therefore fret width:
        # w = s - (s/(2^(n/12))) - s - (s/(2^(n-1/12)))
        # Therefore
        # s = w / (  1/(2^(n/12)) - 1/(2^((n-1)/12)) )
        n = nfrets  # for shorter notation
        s = w / (1 / (2 ^ (n / 12)) - 1 / (2 ^ ((n - 1) / 12)))
        d = s - (s / (2 ^ (n / 12)))  # This is the length of the entire fretboard.

        return d

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

    def fretPos(self, ifret):
        """
        Return position of a fret. Formula taken from https://www.liutaiomottola.com/formulae/fret.htm
        """
