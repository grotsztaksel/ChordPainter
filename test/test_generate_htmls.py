#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['TestGenerateHtmls']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2022-01-16'

import unittest
import os

from music_theory import ChordInterval
from tools.generate_htmls import writeHtml


class TestGenerateHtmls(unittest.TestCase):
    def test_writeHtml(self):
        instrument = "banjo"
        root = "C"
        chordType = ChordInterval.minor
        htmName = os.path.join(os.path.dirname(__file__), "banjo_C_minor.xhtml")
        refName = os.path.join(os.path.dirname(__file__), "test_ref_banjo_C_minor.xhtml")


        if os.path.isfile(htmName):
            os.remove(htmName)
        images = [
            "banjo_openG___C_minor.png",
            "banjo_doubleC_C_minor.png"
        ]
        writeHtml(instrument, root, chordType, htmName, images)

        self.assertTrue(os.path.isfile(htmName))
        with open(htmName, 'r') as f:
            actual = f.read()
        with open(refName, 'r') as r:
            expected = r.read()
        os.remove(htmName)


        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
