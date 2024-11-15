# -*- coding: utf-8 -*-
"""
Created on 03.12.2021 21:12 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['ChordInventor']
__date__ = '2021-12-03'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from Instruments.instrument import Instrument
from music_theory import NOTES, ChordInterval

# An abandoned class
class ChordInventor(object):
    """
    Figures out chord configurations given the instrument's tuning. Implements very little ergonomyy rules, so the
    results are not guaranteed to be doable for humans
    """

    def __init__(self, instrument=None):
        # primitive way to filter possibly ergonomic chords
        self.maxFingerStretch = 4

        self.instrument = None
        self.notes = None
        if instrument is not None:
            self.setInstrument(instrument)

    def setInstrument(self, instrument):
        """Set the notes on the open strings"""
        assert isinstance(instrument, Instrument)
        self.instrument = instrument
        self.figureOutStrings()

    def buildChords(self, root: str, chordType=None):

        chords = []

        for fret in range(0, self.instrument.nfrets - self.maxFingerStretch):
            pass

    def figureOutStrings(self):
        """
        Determine what notes are on which fret of each string.
        """
        if self.instrument is None:
            return
        # Temporarily build a repeatable list of notes
        notes = []
        while len(notes) <= 2 * self.instrument.nfrets:
            notes += NOTES
        self.notes = []
        for i, string in enumerate(self.instrument.strings):
            string = string.replace("h", "b").replace("H", "B")
            notes_on_string = []
            baseNoteIndex = notes.index(string)
            for i in range(self.instrument.rootfrets[i]):
                notes_on_string.append(None)

            for i in range(self.instrument.nfrets - self.instrument.rootfrets[i] + 1):
                notes_on_string.append(notes[baseNoteIndex + i])
            self.notes.append(notes_on_string)
