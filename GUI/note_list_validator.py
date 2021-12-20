#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['NoteListValidator']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-20'

import re
import typing

from PyQt5.QtGui import QValidator

from music_theory import NOTEre, notesFromString


class NoteListValidator(QValidator):
    """Validator that allows only writing notes, commas and spaces"""

    commare = re.compile(" *, *")  # Regex for commas and separators in the string

    def validate(self, input: str, pos: int) -> typing.Tuple['QValidator.State', str, int]:
        s = input.strip()
        if s == "":
            return QValidator.Acceptable, input, pos

        substrings = NOTEre.split(s)
        previousWasNote = False
        for fragment in substrings:
            if fragment == "":
                continue
            if NOTEre.fullmatch(fragment):
                previousWasNote = True
                continue
            elif previousWasNote and NoteListValidator.commare.fullmatch(fragment):
                previousWasNote = False
            else:
                return QValidator.Invalid, input, pos

        if previousWasNote:
            return QValidator.Acceptable, input.upper(), pos
        else:
            return QValidator.Intermediate, input.upper(), pos
