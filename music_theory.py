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

# Regular expression useful for finding notes in a string. Uses reversed(NOTES) so that sharp notes can be resolved
# first
NOTEre = re.compile("({})".format("|".join(reversed(NOTES))), re.IGNORECASE)

ChordType = namedtuple("ChordType", ["interval", "name", "annotations"])
ChordType.interval.__doc__ = "A tuple of halftone intervals between subsequent notes of a chord"
ChordType.name.__doc__ = "Name of the chord type"
ChordType.annotations.__doc__ = "Possible annotations of the chord that can be used in HTML documents"


class ChordInterval(object):
    """
    Lists of intervals that define different kinds of chords
    """
    # Triads:
    major = ChordType((4, 3), "major", [''])
    minor = ChordType((3, 4), "minor", ['m'])
    diminished = ChordType((3, 3), "diminished", ['m&#176;'])
    augmented = ChordType((4, 4), "augmented", ['+'])

    #
    power = ChordType((7, 12), "power", ['5'])

    # Seventh
    major_7 = ChordType((4, 3, 4), "major 7th", ['M7', '&Delta;7'])
    dominant_7 = ChordType((4, 3, 3), "dominant 7th", ["7"])
    minor_major_7 = ChordType((3, 4, 4), "minor major 7th",['minMaj7'])
    min_7 = ChordType((3, 4, 3), "minor 7th", ['m7'])
    halfdim_7 = ChordType((3, 3, 4), "half diminished 7th", ['&emptyv;7'])
    dim7 = ChordType((3, 3, 3), "diminished 7th", ['&#x25CB;7'])

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


def notesFromString(s):
    """
    Extract the valid note names from the input list and returns a list of notes.
    """
    notes = []
    for substr in NOTEre.split(s):
        if substr in NOTES:
            notes.append(substr)
    return notes


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

    for intvl in chordIntervals.interval:
        noteIndex += intvl % 12
        notes.append(allNotes[noteIndex])

    return notes


CHORD_SUFFIXES = r"(\+|0|6|6\/9|7|7b5|7sus4|9|sus2|sus4|add9)?"
CHORD_ENGLISH = re.compile(r"[A-G]#?m?" + CHORD_SUFFIXES)
CHORD_GERMAN = re.compile(r"([AaEe]s?|[CDcdF-hf-h](is)?)" + CHORD_SUFFIXES)
