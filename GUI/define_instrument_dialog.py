#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['DefineInstrumentDialog']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-20'

import json
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal

from music_theory import notesFromString

Ui_DefineInstrumentDialog, QDialog = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "define_instrument_dialog.ui"))


class DefineInstrumentDialog(QDialog, Ui_DefineInstrumentDialog):
    emitInstrumentDefinition = pyqtSignal(str)

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)

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
