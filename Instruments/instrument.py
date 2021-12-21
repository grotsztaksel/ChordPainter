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
from music_theory import NOTES, notesFromString


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
        self.strings = list()  # Names (tones) of the strings. 1st string is the one the farthest to the bottom
        # (the thinnest in guitar)
        self.nfrets = 0  # number of frets
        self.chords = list()
        self.tuning = [("Standard", self.strings)]

        # Numbers of frets on which each string begins. Usually is all zeros, but for bluegrass banjo
        # the 5th string will have value 5
        self.rootfrets = list()

        self.dotsOnFrets = list()

    def defineChord(self, name, scheme=None, frets=None, fingers=None, prefix=None):
        """
        Add a chord diagram to the class
        """
        if prefix is None:
            prefix = ""
        if frets is not None and fingers is not None:
            if fingers is None:
                scheme = frets
            else:
                scheme = tuple((fr, fg) for fr, fg in zip(frets, fingers))
        else:
            assert scheme is not None
        chord = Chord(name, scheme, prefix=prefix)
        if chord not in self.chords:
            self.chords.append(chord)
        # print(f'self.defineChord("{name}", prefix="{type(self).__name__}"', old2new(scheme), ")")

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

    def getNote(self, string, fret):
        """
        Return the name of the note on the given string and fret
        """

        if fret < self.rootfrets[string]:
            return None
        root = self.strings[string]
        ibase = NOTES.index(root)

        return NOTES[(ibase - self.rootfrets[string] + fret) % 12]

    @staticmethod
    def fromData(d):
        """Instantiates and returns a new Instrument object basing on the data provided"""
        instrument = Instrument()
        instrument.name = d["name"]
        if type(d["strings"]) is list:
            instrument.strings = notesFromString(", ".join(d["strings"]))
        else:
            instrument.strings = notesFromString(d["strings"])
        instrument.nfrets = d["nfrets"]
        if "dotsOnFrets" in d:
            instrument.dotsOnFrets = d["dotsOnFrets"]
        if "rootfrets" in d:
            instrument.rootfrets = d["rootfrets"]
        else:
            instrument.rootfrets = [0] * len(instrument.strings)

        instrument.tuning = [("Standard", instrument.strings)]

        invalid = []
        if "tuning" in d:
            for i, t in enumerate(d["tuning"]):
                s = notesFromString(t["strings"])
                if len(s) != len(instrument.strings):
                    # Ignore this one
                    invalid.append(i)
                    continue
                if "name" in t:
                    name = t["name"]
                else:
                    name = ", ".join(s)
                instrument.tuning.append((name, s))
            for inv in reversed(invalid):
                d["tuning"].pop(inv)

        # ToDo: restore chords saved in the data

        return instrument


def old2new(old):
    """ Helper function converting old argument list todefineChord to a new one"""
    frets = []
    fingers = []
    for t in old:
        try:
            frets.append(t[0])
            fingers.append(t[1])
        except TypeError:
            frets.append(t)
            fingers.append(0)

    return ("frets=", tuple(frets), "fingers = ", tuple(fingers))
