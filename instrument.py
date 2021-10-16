# -*- coding: utf-8 -*-
"""
Created on 14.10.2021 22:29 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['Instrument']
__date__ = '2021-10-14'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import warnings
from chord import Chord


class Instrument(object):
    """
    A class collecting chord diagram schemes for a stringed instrument
    """

    def __init__(self):
        """
        Constructor. Override the constructor in subclasses by adding the chord schemes.
        """
        # Name of the instrument. May be used to prefix the filenames with chord diagrams
        self.name = None
        self.strings = list()  # Names (tones) of the strings
        self.chords = set()

    def defineChord(self, name, scheme):
        """
        Add a chord diagram to the class
        """
        self.chords.add(Chord(name, scheme))

    def checkChords(self):
        """
        Check if the chord schemes match the number of strings and the chord name pattern. Throw warnings if not
        """
        for chord in self.chords:
            self.checkChordName(chord)

            self.checkStringCount(chord)

    def checkStringCount(self, chord):
        if len(chord.scheme) != len(self.strings):
            self.stringCountWarning(chord)

    def stringCountWarning(self, chord):
        warnings.warn(
            "{} describes {} strings, while {} has {} strings".format(chord.name, len(chord.scheme),
                                                                      self.name, len(self.strings)))

    def checkChordName(self, chord):
        if not CHORD_PATTERN.match(chord.name):
            self.chordNameWarning(chord)

    def chordNameWarning(self, chord):
        warnings.warn(chord.name + " seems to be not a valid chord name")
