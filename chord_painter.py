# -*- coding: utf-8 -*-
"""
Created on 12.10.2021 21:57 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['ChordPainter']
__date__ = '2021-10-12'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QPixmap


class ChordPainter(object):
    """
    The class actually responsible for painting the chord schemes and saving image files from them
    """

    def __init__(self):
        self.string_offset = 40  # pixels
        self.string_thickness = 2
        self.bar_zero_width = 4
        self.fret_width = 120  # pixels
        self.finger_size = 16  # pixels
        self.dots_on_frets = False  # If True, the painter will draw dots on 3rd, 5, 7 etc frets

        self.size = QSize(640, 480)
        self.colors = {"string": QColor(Qt.black),
                       "fret": QColor(Qt.black),
                       "finger": QColor(Qt.black),
                       "fret_dot": QColor(Qt.gray)}

        self.dir = os.getcwd()
        self.orientation = Qt.Vertical

    def setDir(self, dir):
        """
        Set directory where the files should be saved
        """
        if os.path.isdir(dir):
            self.dir = dir

    def drawChord(self, scheme) -> QPixmap:
        """
        Set up a QPainter object and use scheme to draw a chord
        :param scheme: a tuple of tuples of numbers encoding the chord
               for example:
               ((0), (1,1), (2,3))
               will paint a three-stringed fretboard (three elements in the tuple); the first string is not pressed,
               the second is pressed on the 1st fret with 1st finger; the third is pressed on 2nd fret with 3rd finger

               If each "subtuple" has only one element, the dots on the chord diagram will not have finger numbers

        :return: a QPainter object with the chord scheme
        """
        px = QPixmap(self.size)
        w = self.size.width()
        h = self.size.height()
        p = QPainter(px)

        margin = self.finger_size / 2
        pen = p.pen()
        pen.setColor(self.colors["fret"])
        pen.setWidth(self.bar_zero_width)
        p.drawLine(margin, margin, w - margin, margin)

        pen.setColor(self.colors["string"])
        pen.setWidth(self.string_thickness)

        n = len(scheme) - 1
        if n == 0:
            # Draw only one string
            string_positions = [w / 2]
        else:
            string_positions = [margin + i * (w - self.finger_size) / n for i in range(n)] + [w - margin]

        for sp in string_positions:
            p.drawLine(sp, margin, sp, h - margin)

        p.end()

        return px