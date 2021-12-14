# -*- coding: utf-8 -*-
"""
Created on 04.12.2021 23:06 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Collection of general princoples from music theory
"""

__date__ = '2021-12-04'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import re
from collections import namedtuple

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

ChordType = namedtuple("ChordType", ["interval", "name"])


class ChordInterval(object):
    """
    Lists of intervals that define different kinds of chords
    """
    # Triads:
    major = ChordType((4, 3), "major")
    minor = ChordType((3, 4), "minor")
    diminished = ChordType((3, 3), "diminished")
    augmented = ChordType((4, 4), "augmented")

    # Seventh
    major_7 = ChordType((4, 3, 4), "major 7th")
    dominant_7 = ChordType((4, 3, 3), "dominant 7th")
    minor_major_7 = ChordType((3, 4, 4), "minor major 7th")
    min_7 = ChordType((3, 4, 3), "minor 7th")
    halfdim_7 = ChordType((3, 3, 4), "half diminished 7th")
    dim7 = ChordType((3, 3, 3), "diminished 7th")

    @staticmethod
    def getInterval(intvl_name):
        for chord in ChordInterval.getAllChordTypes():
            if intvl_name == chord.name:
                return chord

    @staticmethod
    def getAllChordTypes():
        """
        Returns a list of all chord types that are defined in this class
        """
        chordTypes = []
        for a in dir(ChordInterval):
            if a.startswith("__") or a.endswith("__"):
                continue
            attr = getattr(ChordInterval, a)
            if isinstance(attr, ChordType):
                chordTypes.append(attr)
        return chordTypes


def getChordNotes(root: str, chordIntervals=None):
    """
    Determine the notes in a chord. Returns a list of notes, the first note being the root note
    """
    assert root.upper() in NOTES

    if chordIntervals is None:
        chordIntervals = ChordInterval.major

    allNotes = 3 * NOTES
    noteIndex = allNotes.index(root.upper())

    notes = [root]

    for intvl in chordIntervals:
        noteIndex += (intvl) % 12
        notes.append(allNotes[noteIndex])

    return notes


CHORD_SUFFIXES = r"(\+|0|6|6\/9|7|7b5|7sus4|9|sus2|sus4|add9)?"
CHORD_ENGLISH = re.compile(r"[A-G]#?m?" + CHORD_SUFFIXES)
CHORD_GERMAN = re.compile(r"([AaEe]s?|[CDcdF-hf-h](is)?)" + CHORD_SUFFIXES)
