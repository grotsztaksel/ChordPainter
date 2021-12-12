# -*- coding: utf-8 -*-
"""
Created on 04.12.2021 23:06 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Collection of general princoples from music theory
"""

__date__ = '2021-12-04'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import re

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


class ChordInterval(object):
    """
    Lists of intervals that define different kinds of chords
    """
    # Triads:
    major = (4, 3)
    minor = (3, 4)
    diminished = (3, 3)
    augmented = (4, 4)

    # Seventh
    major_7 = (4, 3, 4)
    dominant_7 = (4, 3, 3)
    minor_major_7 = (3, 4, 4)
    min_7 = (3, 4, 3)
    halfdim_7 = (3, 3, 4)
    dim7 = (3, 3, 3)

    @staticmethod
    def getAllChordTypes__():
        """
        Returns a list of all chord types that are defined in this class
        """
        chordTypes = []
        for a in dir(ChordInterval):
            if a.startswith("__") or a.endswith("__"):
                continue
            attr = getattr(ChordInterval, a)
            if isinstance(attr, list):
                chordTypes.append(a)
        return chordTypes


CHORD_SUFFIXES = r"(\+|0|6|6\/9|7|7b5|7sus4|9|sus2|sus4|add9)?"
CHORD_ENGLISH = re.compile(r"[A-G]#?m?" + CHORD_SUFFIXES)
CHORD_GERMAN = re.compile(r"([AaEe]s?|[CDcdF-hf-h](is)?)" + CHORD_SUFFIXES)
