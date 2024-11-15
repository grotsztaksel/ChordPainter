#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['ChordSelector']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-12'

import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QButtonGroup, QRadioButton, QGridLayout, QAbstractButton, QWidget

from music_theory import NOTES, ChordInterval, getChordNotes, notesFromString

Ui_ChordSelector, QWidget = uic.loadUiType(os.path.join(os.path.dirname(__file__), "chord_selector.ui"))


class ChordSelector(QWidget, Ui_ChordSelector):
    chordSelected = pyqtSignal(str, str)

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.chordRootButtons = QButtonGroup(self)
        self.grid = QGridLayout(self)
        self.verticalLayout.insertLayout(1, self.grid)

        self.clearButton.clicked.connect(self.clear)
        self.chordSelected.connect(self._updateNotes)
        self._setupRadioButtons()

        self._setupComboBox()

        self.chordNotesEdit.editingFinished.connect(self.updateChordFromText)

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

    @pyqtSlot()
    def updateChordFromText(self):
        """
        When the line editor content was edited manually, try recognizing the chord and adjusting the widget's state
        """
        notes = set(notesFromString(self.chordNotesEdit.text()))
        for ctype in ChordInterval.getAllChordTypes():
            for note in NOTES:
                chord = set(getChordNotes(note, ctype))
                if chord == notes:
                    self.setChord(note, ctype)
                    return

        # Nothing was found. Uncheck all buttons
        self.blockSignals(True)
        self.clear()
        self.blockSignals(False)

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

    def emitChord(self):
        btn = self.chordRootButtons.checkedButton()
        if btn is None:
            return
        chordType = self.chordTypeComboBox.currentText()
        self.chordSelected.emit(btn.text(), chordType)

    @pyqtSlot()
    def clear(self):
        self.chordRootButtons.blockSignals(True)
        self.chordRootButtons.setExclusive(False)
        for button in self.chordRootButtons.buttons():
            button.setChecked(False)
        self.chordRootButtons.setExclusive(True)
        self.chordRootButtons.blockSignals(False)

        self.chordSelected.emit("", "")

    def setChord(self, root, ctype):
        self.chordRootButtons.button(NOTES.index(root)).setChecked(True)
        self.chordTypeComboBox.setCurrentText(ctype.name)
