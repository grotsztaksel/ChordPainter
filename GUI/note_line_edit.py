#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['NoteLineEdit']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-20'

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLineEdit

from GUI.note_list_validator import NoteListValidator
from music_theory import notesFromString


class NoteLineEdit(QLineEdit):
    """Line text editor specialized in handling lists of notes"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValidator(NoteListValidator(self))
        self.editingFinished.connect(self.adjustChordNotesEdit)

    @pyqtSlot()
    def adjustChordNotesEdit(self):
        """Adjust the content of the Chord Notes line editor - apply nice formatting"""
        self.setText(", ".join(notesFromString(self.text())))
