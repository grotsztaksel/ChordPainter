# -*- coding: utf-8 -*-
"""
Created on 14.10.2021 22:47 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['Banjo_5string']
__date__ = '2021-10-14'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from instrument import Instrument


class Banjo_5string(Instrument):
    def __init__(self):
        super().__init__()
        self.name = "Banjo"
        self.strings = list("GDGHD")
        self.dotsOnFrets = [3, 5, 7, 10, 12, 15, 17]

        self.defineChord("C", ((2, 2), 0, (1, 1), (2, 3)))
        self.defineChord("c", ((2, 1), 0, (2, 2), (2, 3)))
        self.defineChord("C7", ((2, 1), (3, 4), (1, 1), (2, 3)))

        self.defineChord("C#", ((3, 3), (1, 1), (2, 2), (3, 4)))
        self.defineChord("C#7", ((3, 3), (1, 1), (2, 2), (3, 4)))

        self.defineChord("D", (0, (2, 1), (3, 2), (4, 4)))  # Could probably also be (4,3)
        self.defineChord("d", (0, (2, 1), (3, 2), (3, 3)))
        self.defineChord("D7", (0, (2, 2), (1, 1), 0))
        self.defineChord("D7", (0, (2, 2), (1, 1), (4, 4)))

        self.defineChord("D#", ((3 + 2, 3), (1 + 2, 1), (2 + 2, 2), (3 + 2, 4)))
        self.defineChord("D#", (((8, 1), (8, 1), (8, 1), (8, 1))))
        self.defineChord("D#7", (((1, 1), 0, (2, 3), (1, 2))))
        # self.defineChord("D#7", (((1, 1), (3, 3), (2, 2), (5, 4))))

        self.defineChord("E", ((2, 2), (1, 1), 0, (2, 3)))
        self.defineChord("e", ((2, 2), 0, 0, (2, 3)))
        self.defineChord("E7", ((2, 2), (1, 1), (3, 4), (2, 3)))

        self.defineChord("F", ((3, 3), (2, 2), (1, 1), (3, 4)))
        self.defineChord("f", ((3, 3), (1, 1), (1, 1), (3, 4)))
        self.defineChord("F7", ((3, 3), (2, 2), (1, 1), (1, 1)))

        self.defineChord("F#", ((3 + 1, 3), (2 + 1, 2), (1 + 1, 1), (3 + 1, 4)))
        self.defineChord("F#7", ((3 + 1, 3), (2 + 1, 2), (1 + 1, 1), (1 + 1, 1)))

        self.defineChord("G", (0, 0, 0, 0))
        self.defineChord("G", ((3 + 2, 3), (2 + 2, 2), (1 + 2, 1), (3 + 2, 4)))
        self.defineChord("g", ((5, 3), (3, 1), (3, 1), (5, 4)))
        self.defineChord("G7", (0, 0, 0, (3, 3)))

        self.defineChord("G#", ((1, 1), (1, 1), (1, 1), (1, 1)))
        self.defineChord("G#", ((3 + 3, 3), (2 + 3, 2), (1 + 3, 1), (3 + 3, 4)))
        self.defineChord("G#7", ((1, 1), (1, 1), (1, 1), (4, 4)))

        self.defineChord("A", ((2, 1), (2, 1), (2, 1), (2, 1)))
        self.defineChord("A", ((3 + 4, 3), (2 + 4, 2), (1 + 4, 1), (3 + 4, 4)))
        self.defineChord("a", ((2, 2), (2, 3), (1, 1), (2, 4)))
        self.defineChord("A7", ((2, 1), 0, (2, 2), (2, 2)))

        self.defineChord("A#", ((3, 1), (3, 1), (3, 1), (3, 1)))
        self.defineChord("A#", ((3 + 5, 3), (2 + 5, 2), (1 + 5, 1), (3 + 5, 4)))
        self.defineChord("A#m", ((3, 2), (3, 3), (2, 1), (3, 4)))
        self.defineChord("A#7", ((3, 1), (3, 1), (3, 1), (6, 4)))

        self.defineChord("H", ((4, 1), (4, 1), (4, 1), (4, 1)))
        self.defineChord("H", ((3 + 6, 3), (2 + 6, 2), (1 + 6, 1), (3 + 6, 4)))
        self.defineChord("h", ((2 + 2, 2), (2 + 2, 3), (1 + 2, 1), (2 + 2, 4)))
        self.defineChord("H7", ((1, 1), (2, 3), 0, (1, 2)))

    def checkStringCount(self, chord):
        """
        In the five-string banjo, the 1st string usually does not participate in the chord scheme
        """
        if len(chord.scheme) not in [4, 5]:
            self.stringCountWarning(chord)
