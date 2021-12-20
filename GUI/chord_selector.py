#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['ChordSelector']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-12'

import os
import re
import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QButtonGroup, QRadioButton, QGridLayout, QAbstractButton

from music_theory import NOTES, ChordInterval, getChordNotes, NOTEre

Ui_ChordSelector, QWidget = uic.loadUiType(os.path.join(os.path.dirname(__file__), "chord_selector.ui"))


class ChordSelector(QWidget, Ui_ChordSelector):
    chordSelected = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.chordRootButtons = QButtonGroup(self)
        self.grid = QGridLayout(self)
        self.verticalLayout.insertLayout(1, self.grid)

        self.clearButton.clicked.connect(self.clear)
        self.chordSelected.connect(self._updateNotes)
        self._setupRadioButtons()

        self._setupComboBox()
        self.chordNotesEdit.setValidator(NoteListValidator(self.chordNotesEdit))

    def _setupComboBox(self):
        chordTypes = [c.name for c in ChordInterval.getAllChordTypes()]
        self.chordTypeComboBox.addItems(chordTypes)
        self.chordTypeComboBox.setCurrentIndex(chordTypes.index("major"))
        self.chordTypeComboBox.currentTextChanged.connect(self.onChordTypeSelected)

    def _setupRadioButtons(self):
        col = 0
        row = 0
        maxRows = 4
        for i, note in enumerate(NOTES):
            if row == maxRows:
                row = 0
                col += 1

            btn = QRadioButton(self)
            btn.setObjectName(note)
            btn.setText(note)
            self.grid.addWidget(btn, row, col)
            self.chordRootButtons.addButton(btn, i)
            row += 1
        self.chordRootButtons.buttonToggled.connect(self.onButtonToggled)

    @pyqtSlot(str, str)
    def _updateNotes(self, chordRoot, chordType):
        """
        Update the content of own line editor
        """
        intvl = ChordInterval.getInterval(chordType)
        if intvl is None:
            currentChord = []
        else:
            currentChord = getChordNotes(chordRoot, intvl)

        self.chordNotesEdit.setText(', '.join(currentChord))

    @pyqtSlot(QAbstractButton, bool)
    def onButtonToggled(self, button, checked):
        if not checked:
            return

        root = button.text()
        chordType = self.chordTypeComboBox.currentText()
        self.chordSelected.emit(root, chordType)

    @pyqtSlot(str)
    def onChordTypeSelected(self, chordType):
        btn = self.chordRootButtons.checkedButton()
        if btn is None:
            return

        self.chordSelected.emit(btn.text(), chordType)

    @pyqtSlot()
    def clear(self):
        self.chordRootButtons.blockSignals(True)
        for button in self.chordRootButtons.buttons():
            button.setChecked(False)
        self.chordRootButtons.blockSignals(False)

        self.chordSelected.emit("", "")


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
            return QValidator.Acceptable, input, pos
        else:
            return QValidator.Intermediate, input, pos
