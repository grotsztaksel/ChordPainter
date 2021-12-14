#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['TestChordInterval']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-14'

import unittest

from music_theory import ChordInterval


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


if __name__ == '__main__':
    unittest.main()
