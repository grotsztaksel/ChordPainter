#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['TestChordInterval', 'TestMusicTheory']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-14'

import unittest

from music_theory import ChordInterval, getChordNotes, NOTES, ChordType, notesFromString


class TestChordInterval(unittest.TestCase):
    def test_getInterval(self):
        self.assertEqual(ChordInterval.major, ChordInterval.getInterval("major"))
        self.assertEqual(ChordInterval.minor, ChordInterval.getInterval("minor"))
        self.assertEqual(ChordInterval.diminished, ChordInterval.getInterval("diminished"))
        self.assertEqual(ChordInterval.augmented, ChordInterval.getInterval("augmented"))
        self.assertEqual(ChordInterval.major_7, ChordInterval.getInterval("major 7th"))
        self.assertEqual(ChordInterval.dominant_7, ChordInterval.getInterval("dominant 7th"))
        self.assertEqual(ChordInterval.minor_major_7, ChordInterval.getInterval("minor major 7th"))
        self.assertEqual(ChordInterval.min_7, ChordInterval.getInterval("minor 7th"))
        self.assertEqual(ChordInterval.halfdim_7, ChordInterval.getInterval("half diminished 7th"))
        self.assertEqual(ChordInterval.dim7, ChordInterval.getInterval("diminished 7th"))

        self.assertIsNone(ChordInterval.getInterval("blah"))

    def test_getAllChordTypes(self):
        expected = [ChordType(interval=(4, 4), name='augmented', annotations=['+']),
                    ChordType(interval=(3, 3, 3), name='diminished 7th', annotations=['&#x25CB;7']),
                    ChordType(interval=(3, 3), name='diminished', annotations=['&#176;']),
                    ChordType(interval=(4, 3, 3), name='dominant 7th', annotations=["7"]),
                    ChordType(interval=(3, 3, 4), name='half diminished 7th', annotations=['&emptyv;7']),
                    ChordType(interval=(4, 3), name='major', annotations=['']),
                    ChordType(interval=(4, 3, 4), name='major 7th', annotations=['M7', '&Delta;7']),
                    ChordType(interval=(3, 4, 3), name='minor 7th', annotations=['m7']),
                    ChordType(interval=(3, 4), name='minor', annotations=['m']),
                    ChordType(interval=(3, 4, 4), name='minor major 7th', annotations=['minMaj7'])]
        self.assertEqual(expected, ChordInterval.getAllChordTypes())


class TestMusicTheory(unittest.TestCase):
    def test_NOTES(self):
        self.assertEqual(12, len(NOTES))

    def test_notesFromString(self):
        self.assertEqual(['E', 'G#', 'B'], notesFromString("EG#B"))
        self.assertEqual(['B', 'D#', 'F#'], notesFromString("B, D# F#"))

    def test_getChordNotes(self):
        self.assertEqual(['E', 'G#', 'B'], getChordNotes("E", ChordInterval.major))
        self.assertEqual(['B', 'D#', 'F#'], getChordNotes("B", ChordInterval.major))
        self.assertEqual(['A#', 'D', 'F'], getChordNotes("A#", ChordInterval.major))
        self.assertEqual(['E', 'G', 'A#'], getChordNotes("E", ChordInterval.diminished))
        self.assertEqual(['A', 'C', 'E'], getChordNotes("A", ChordInterval.minor))

        self.assertEqual(NOTES, getChordNotes("C", ChordType(tuple(11 * [1]), "just all notes!", ['test'])))


if __name__ == '__main__':
    unittest.main()
