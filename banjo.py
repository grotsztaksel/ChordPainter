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
        self.nfrets = 22
        self.rootfrets = [0, 0, 0, 0, 5]

        self.dotsOnFrets = [3, 5, 7, 10, 12, 15, 17]

        self.defineChord("C", prefix="banjo_", frets=(2, 0, 1, 2), fingers=(2, 0, 1, 3))
        self.defineChord("C", prefix="banjo_", frets=(5, 5, 5, 5), fingers=(1, 1, 1, 1))
        self.defineChord("C", prefix="banjo_", frets=(10, 9, 8, 10), fingers=(3, 2, 1, 4))
        self.defineChord("C", prefix="banjo_", frets=(14, 12, 13, 14), fingers=(3, 1, 2, 4))
        self.defineChord("C", prefix="banjo_", frets=(17, 17, 17, 17), fingers=(1, 1, 1, 1))

        self.defineChord("c", prefix="banjo_", frets=(2, 0, 2, 2), fingers=(1, 0, 2, 3))
        self.defineChord("c", prefix="banjo_", frets=(5, 4, 5, 5), fingers=(2, 3, 1, 4))
        self.defineChord("c", prefix="banjo_", frets=(10, 8, 8, 10), fingers=(3, 1, 1, 4))
        self.defineChord("c", prefix="banjo_", frets=(13, 11, 13, 13), fingers=(2, 1, 3, 4))
        self.defineChord("c", prefix="banjo_", frets=(17, 16, 17, 17), fingers=(2, 3, 1, 4))

        self.defineChord("C7", prefix="banjo_", frets=(2, 3, 1, 2), fingers=(1, 4, 1, 3))
        self.defineChord("C7", prefix="banjo_", frets=(5, 5, 5, 8), fingers=(1, 1, 1, 4))
        self.defineChord("C7", prefix="banjo_", frets=(8, 5, 5, 5), fingers=(4, 1, 1, 1))
        self.defineChord("C7", prefix="banjo_", frets=(8, 9, 8, 10), fingers=(1, 2, 1, 3))
        self.defineChord("C7", prefix="banjo_", frets=(10, 12, 11, 14), fingers=(1, 3, 2, 4))
        self.defineChord("C7", prefix="banjo_", frets=(10, 9, 11, 10), fingers=(2, 1, 4, 3))

        self.defineChord("c7", prefix="banjo_", frets=(1, 3, 1, 1), fingers=(1, 3, 1, 1))
        self.defineChord("c7", prefix="banjo_", frets=(10, 8, 8, 8), fingers=(3, 1, 1, 3))
        self.defineChord("c7", prefix="banjo_", frets=(8, 8, 8, 10), fingers=(1, 1, 1, 3))
        self.defineChord("c7", prefix="banjo_", frets=(10, 12, 11, 13), fingers=(1, 3, 2, 4))
        self.defineChord("c7", prefix="banjo_", frets=(10, 8, 11, 10), fingers=(2, 1, 4, 3))

        self.defineChord("C#", prefix="banjo_", frets=(3, 1, 2, 3), fingers=(3, 1, 2, 4))
        self.defineChord("C#", prefix="banjo_", frets=(6, 6, 6, 6), fingers=(1, 1, 1, 1))
        self.defineChord("C#", prefix="banjo_", frets=(11, 10, 9, 11), fingers=(3, 2, 1, 4))
        self.defineChord("C#", prefix="banjo_", frets=(15, 13, 14, 15), fingers=(3, 1, 2, 4))
        self.defineChord("C#", prefix="banjo_", frets=(18, 18, 18, 18), fingers=(1, 1, 1, 1))

        self.defineChord("C#7", prefix="banjo_", frets=(3, 1, 2, 3), fingers=(3, 1, 2, 4))
        self.defineChord("C#7", prefix="banjo_", frets=(6, 6, 6, 9), fingers=(1, 1, 1, 4))
        self.defineChord("C#7", prefix="banjo_", frets=(9, 6, 6, 6), fingers=(4, 1, 1, 1))
        self.defineChord("C#7", prefix="banjo_", frets=(9, 10, 9, 11), fingers=(1, 2, 1, 3))
        self.defineChord("C#7", prefix="banjo_", frets=(11, 10, 9, 9), fingers=(3, 2, 1, 1))
        self.defineChord("C#7", prefix="banjo_", frets=(11, 13, 12, 15), fingers=(1, 3, 2, 4))
        self.defineChord("C#7", prefix="banjo_", frets=(11, 10, 12, 11), fingers=(2, 1, 4, 3))

        self.defineChord("D", prefix="banjo_", frets=(0, 2, 3, 4), fingers=(0, 1, 2, 4))
        self.defineChord("D", prefix="banjo_", frets=(4, 2, 3, 4), fingers=(3, 1, 2, 4))
        self.defineChord("D", prefix="banjo_", frets=(0, 7, 7, 7), fingers=(0, 1, 1, 1))
        self.defineChord("D", prefix="banjo_", frets=(7, 7, 7, 7), fingers=(1, 1, 1, 1))
        self.defineChord("D", prefix="banjo_", frets=(0, 11, 10, 12), fingers=(0, 2, 1, 3))
        self.defineChord("D", prefix="banjo_", frets=(12, 11, 10, 12), fingers=(3, 2, 1, 4))

        self.defineChord("d", prefix="banjo_", frets=(0, 2, 3, 3), fingers=(0, 1, 2, 3))

        self.defineChord("D7", prefix="banjo_", frets=(0, 2, 1, 0), fingers=(0, 2, 1, 0))
        self.defineChord("D7", prefix="banjo_", frets=(0, 2, 1, 4), fingers=(0, 2, 1, 4))

        self.defineChord("D#", prefix="banjo_", frets=(5, 3, 4, 5), fingers=(3, 1, 2, 4))
        self.defineChord("D#", prefix="banjo_", frets=(8, 8, 8, 8), fingers=(1, 1, 1, 1))
        self.defineChord("D#7", prefix="banjo_", frets=(1, 0, 2, 1), fingers=(1, 0, 3, 2))

        self.defineChord("E", prefix="banjo_", frets=(2, 1, 0, 2), fingers=(2, 1, 0, 3))
        self.defineChord("e", prefix="banjo_", frets=(2, 0, 0, 2), fingers=(2, 0, 0, 3))
        self.defineChord("E7", prefix="banjo_", frets=(2, 1, 3, 2), fingers=(2, 1, 4, 3))

        self.defineChord("F", prefix="banjo_", frets=(3, 2, 1, 3), fingers=(3, 2, 1, 4))
        self.defineChord("f", prefix="banjo_", frets=(3, 1, 1, 3), fingers=(3, 1, 1, 4))
        self.defineChord("F7", prefix="banjo_", frets=(3, 2, 1, 1), fingers=(3, 2, 1, 1))

        self.defineChord("F#", prefix="banjo_", frets=(4, 3, 2, 4), fingers=(3, 2, 1, 4))
        self.defineChord("F#7", prefix="banjo_", frets=(4, 3, 2, 2), fingers=(3, 2, 1, 1))

        self.defineChord("G", prefix="banjo_", frets=(0, 0, 0, 0), fingers=(0, 0, 0, 0))
        self.defineChord("G", prefix="banjo_", frets=(5, 4, 3, 5), fingers=(3, 2, 1, 4))
        self.defineChord("g", prefix="banjo_", frets=(5, 3, 3, 5), fingers=(3, 1, 1, 4))
        self.defineChord("G7", prefix="banjo_", frets=(0, 0, 0, 3), fingers=(0, 0, 0, 3))
        self.defineChord("G7", prefix="banjo_", frets=(5, 4, 3, 3), fingers=(3, 2, 1, 1))
        self.defineChord("G#", prefix="banjo_", frets=(1, 1, 1, 1), fingers=(1, 1, 1, 1))
        self.defineChord("G#", prefix="banjo_", frets=(6, 5, 4, 6), fingers=(3, 2, 1, 4))
        self.defineChord("G#7", prefix="banjo_", frets=(1, 1, 1, 4), fingers=(1, 1, 1, 4))
        self.defineChord("G#7", prefix="banjo_", frets=(6, 5, 4, 4), fingers=(3, 2, 1, 1))

        self.defineChord("A", prefix="banjo_", frets=(2, 2, 2, 2), fingers=(1, 1, 1, 1))
        self.defineChord("A", prefix="banjo_", frets=(7, 6, 5, 7), fingers=(3, 2, 1, 4))
        self.defineChord("a", prefix="banjo_", frets=(2, 2, 1, 2), fingers=(2, 3, 1, 4))
        self.defineChord("A7", prefix="banjo_", frets=(2, 0, 2, 2), fingers=(1, 0, 2, 2))
        self.defineChord("A7", prefix="banjo_", frets=(7, 6, 5, 5), fingers=(3, 2, 1, 1))
        self.defineChord("A#", prefix="banjo_", frets=(3, 3, 3, 3), fingers=(1, 1, 1, 1))
        self.defineChord("A#", prefix="banjo_", frets=(8, 7, 6, 8), fingers=(3, 2, 1, 4))
        self.defineChord("A#m", prefix="banjo_", frets=(3, 3, 2, 3), fingers=(2, 3, 1, 4))
        self.defineChord("A#7", prefix="banjo_", frets=(3, 3, 3, 6), fingers=(1, 1, 1, 4))
        self.defineChord("H", prefix="banjo_", frets=(4, 4, 4, 4), fingers=(1, 1, 1, 1))
        self.defineChord("H", prefix="banjo_", frets=(9, 8, 7, 9), fingers=(3, 2, 1, 4))
        self.defineChord("h", prefix="banjo_", frets=(4, 4, 3, 4), fingers=(2, 3, 1, 4))
        self.defineChord("H7", prefix="banjo_", frets=(1, 2, 0, 1), fingers=(1, 3, 0, 2))

    def checkStringCount(self, chord):
        """
        In the five-string banjo, the 1st string usually does not participate in the chord scheme
        """
        if len(chord.scheme) not in [4, 5]:
            self.stringCountWarning(chord)
