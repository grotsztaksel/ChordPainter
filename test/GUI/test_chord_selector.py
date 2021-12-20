#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['TestChordSelector']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-14'

import unittest

from GUI import ChordSelector
from test.GUI.gui_test_app import app


class TestChordSelector(unittest.TestCase):

    def setUp(self) -> None:
        self.widget = ChordSelector()
        app.processEvents()

    def tearDown(self) -> None:
        self.widget.deleteLater()

    def test_clear(self):
        self.widget.chordRootButtons.button(1).setChecked(True)
        self.assertTrue(self.widget.chordRootButtons.exclusive())
        self.widget.clear()
        for btn in self.widget.chordRootButtons.buttons():
            self.assertFalse(btn.isChecked())
        self.assertTrue(self.widget.chordRootButtons.exclusive())


if __name__ == '__main__':
    unittest.main()
