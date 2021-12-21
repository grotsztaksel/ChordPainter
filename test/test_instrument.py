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

    def test_fromData(self):
        data = {
                   "name": "Guitar",
                   "strings": "EBGDAE",
                   "tuning": [{"name": "Drop D", "strings": "EBGDAD"},
                              {"name": "Open D", "strings": "DADF#AD"}],
                   "nfrets": 20,
                   "dotsOnFrets": [3, 5, 7, 9, 12, 15, 17]
               }
        i = Instrument.fromData(data)
        self.assertEqual("Guitar", i.name)
        self.assertEqual(["E", "B", "G", "D", "A", "E"], i.strings)
        self.assertEqual(20, i.nfrets)
        self.assertEqual([3, 5, 7, 9, 12, 15, 17], i.dotsOnFrets)

        self.assertEqual(["E", "B", "G", "D", "A", "E"], i.tuning[0][1])


if __name__ == '__main__':
    unittest.main()
