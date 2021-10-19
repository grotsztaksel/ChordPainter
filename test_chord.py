# -*- coding: utf-8 -*-
"""
Created on 19.10.2021 22:05 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-10-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import unittest

from chord import Chord


class TestChord(unittest.TestCase):
    def test_toString(self):
        # Place "0" instead of the chord scheme. It's shorter here and doesn't matter for the toString()
        self.assertEqual("D_major", Chord("D", 0).toString)
        self.assertEqual("D_minor", Chord("Dm", 0).toString)
        self.assertEqual("D_sharp_minor", Chord("D#m", 0).toString)
        self.assertEqual("D_major_7", Chord("D7", 0).toString)
        self.assertEqual("D_minor_7", Chord("d7", 0).toString)
        self.assertEqual("D_sharp_minor_7", Chord("dis7", 0).toString)
        self.assertEqual("A_sharp_minor_6by9", Chord("as6/9", 0).toString)


if __name__ == '__main__':
    unittest.main()
