#!/usr/bin/env python
# -*- encoding: utf-8 -*-




__all__ = ['NoteListValidator']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-20'

import re
import typing

from PyQt5.QtGui import QValidator

from music_theory import NOTEre


class NoteListValidator(QValidator):
    """Validator that allows only writing notes, commas and spaces"""

    commare = re.compile(" *, *")  # Regex for commas and separators in the string

    def validate(self, input: str, pos: int) -> typing.Tuple['QValidator.State', str, int]:
        s = input.strip()
        if s == "":
            return QValidator.Acceptable, input, pos

        substrings = NOTEre.split(s)
        noteExpected = False
        for fragment in substrings:
            if fragment == "":
                continue
            noteExpected = not noteExpected
            if noteExpected:
                regex = NOTEre
            else:
                regex = NoteListValidator.commare
            if not regex.fullmatch(fragment):
                return QValidator.Invalid, input, pos

        if noteExpected:
            return QValidator.Acceptable, input.upper(), pos
        else:
            return QValidator.Intermediate, input.upper(), pos
