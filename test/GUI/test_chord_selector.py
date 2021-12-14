#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['TestChordSelector']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-14'

import unittest

from PyQt5.QtGui import QValidator

from GUI.chord_selector import NoteListValidator


class TestChordSelector(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


class TestNoteListValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = NoteListValidator()

    def tearDown(self) -> None:
        self.validator.deleteLater()
        self.validator = None

    def test_validate(self):
        self.assertEqual((QValidator.Acceptable, "A", 1), self.validator.validate("A", 1))
        self.assertEqual((QValidator.Acceptable, "A,C", 3), self.validator.validate("A,C", 3))
        self.assertEqual((QValidator.Acceptable, "A, C#", 1), self.validator.validate("A, C#", 1))
        self.assertEqual((QValidator.Acceptable, "A , C#", -1), self.validator.validate("A , C#", -1))

        self.assertEqual((QValidator.Intermediate, "A , C#,", 2), self.validator.validate("A , C#,", 2))
        self.assertEqual((QValidator.Intermediate, "A , C# ,  C, ", 54), self.validator.validate("A , C# ,  C, ", 54))

        self.assertEqual((QValidator.Invalid, "A major", 0), self.validator.validate("A major", 0))
        self.assertEqual((QValidator.Invalid, "K#", 32), self.validator.validate("K#", 32))

        if __name__ == '__main__':
            unittest.main()
