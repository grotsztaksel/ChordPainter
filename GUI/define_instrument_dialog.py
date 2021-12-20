#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['DefineInstrumentDialog']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-20'

import json
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialogButtonBox

from .note_list_validator import NoteListValidator
from music_theory import notesFromString

Ui_DefineInstrumentDialog, QDialog = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "define_instrument_dialog.ui"))


class DefineInstrumentDialog(QDialog, Ui_DefineInstrumentDialog):
    emitInstrumentDefinition = pyqtSignal(str)

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.tuningLineEdit.setValidator(NoteListValidator(self.tuningLineEdit))
        self.tuningLineEdit.textChanged.connect(self._updateStringCounter)
        self.tuningLineEdit.textChanged.connect(self.updateOKbutton)
        self.instrumentName.textChanged.connect(self.updateOKbutton)

        self.updateOKbutton()

    @pyqtSlot()
    def updateOKbutton(self):
        """Update the enabling state of the OK button, depending on whether the new instrument can or cannot be saved"""
        button = self.buttonBox.button(QDialogButtonBox.Ok)

        if not self.instrumentName.text():
            button.setEnabled(False)
            return
        if not notesFromString(self.tuningLineEdit.text()):
            button.setEnabled(False)
            return

        button.setEnabled(True)

    def accept(self):
        newInstrument = {
            "name": self.instrumentName.text(),
            "strings": notesFromString(self.tuningLineEdit.text()),
            "nfrets": self.nfretsSpinBox.value()
        }
        dottxt = self.dotsOnFretsEditor.text()
        if dottxt:
            try:
                newInstrument["dotsOnFrets"] = [int(dot) for dot in dottxt.split(",")]
            except ValueError:
                pass

        self.emitInstrumentDefinition.emit(json.dumps(newInstrument))
        super().accept()

    @pyqtSlot(str)
    def _updateStringCounter(self, text):
        l = len(notesFromString(text))
        if l == 1:
            s = ""
        else:
            s = "s"
        self.nstrings.setText(f"{str(l)} string{s}")
