# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 21:50 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Test module for instrument class
"""

__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import unittest

from Instruments.instrument import Instrument


class TestInstrument(unittest.TestCase):
    def test_getNote(self):
        instrument = Instrument()
        instrument.strings = list("DBGDG")
        instrument.rootfrets = [0, 0, 0, 0, 5]

        self.assertEqual("A", instrument.getNote(4, 7))
        self.assertEqual("G", instrument.getNote(4, 5))
        self.assertEqual("D", instrument.getNote(0, 0))
        self.assertEqual("F", instrument.getNote(0, 15))
        self.assertIsNone(instrument.getNote(4, 2))


if __name__ == '__main__':
    unittest.main()
