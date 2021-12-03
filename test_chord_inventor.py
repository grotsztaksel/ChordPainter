# -*- coding: utf-8 -*-
"""
Created on 03.12.2021 22:32 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-12-03'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import unittest
from banjo import Banjo_5string
from guitar import Guitar
from chord_inventor import ChordInventor, Interval, NOTES
from chord import Chord


class TestChordInventor(unittest.TestCase):
    def test_buildChords_guitar_major(self):
        g = Guitar()
        inv = ChordInventor(g)
        # ToDo: Add asserts
        chords = {note: inv.buildChords(note, Interval.major) for note in NOTES}
        for note, chord in chords.items():
            for c in chord:
                self.assertIn(c, g.chords)

        # ToDo: Check more chords
        self.assertIn(Chord("D", (None, 0, 0, 2, 3, 2)), chords["D"])
        self.assertIn(Chord("D", (5, 5, 7, 7, 7, 5)), chords["D"])

        self.assertIn(Chord("E", (0, 2, 2, 1, 0, 0)), chords["E"])

        self.assertIn(Chord("G", (2, 3, 0, 0, 0, 2)), chords["G"])

    def test_buildChords_guitar_minor(self):
        g = Guitar()
        inv = ChordInventor(g)
        # ToDo: Add asserts
        chords = {note.lower(): inv.buildChords(note, Interval.minor) for note in NOTES}
        for note, chord in chords.items():
            for c in chord:
                self.assertIn(c, g.chords)

        # ToDo: Check more chords
        self.assertIn(Chord("e", (0, 2, 2, 0, 0, 0)), chords['e'])

    def test_figureOutStrings(self):
        g = Guitar()
        inv = ChordInventor(g)

        e = ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#',
             'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']
        B = ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#',
             'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G']
        G = ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#',
             'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#']
        D = ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#',
             'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#']
        A = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
             'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', "F"]
        E = ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#',
             'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']

        self.assertEqual([e, B, G, D, A, E], inv.notes)

        b = Banjo_5string()
        inv = ChordInventor(b)

        D = ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#',
             'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']
        B = ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#',
             'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A']
        G = ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#',
             'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F']
        D2 = ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#',
              'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']
        G2 = [None, None, None, None, None,
              'G', 'G#', 'A', 'A#', 'B', 'C', 'C#',
              'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']

        self.assertEqual([D, B, G, D2, G2], inv.notes)


if __name__ == '__main__':
    unittest.main()
