#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['ChordSelector']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-12'

import os

from PyQt5 import uic
from PyQt5.QtWidgets import QButtonGroup, QRadioButton, QGridLayout

from music_theory import NOTES, ChordInterval

Ui_ChordSelector, QWidget = uic.loadUiType(os.path.join(os.path.dirname(__file__), "chord_selector.ui"))


class ChordSelector(QWidget, Ui_ChordSelector):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.chordRootButtons = QButtonGroup(self)
        self.grid = QGridLayout(self)
        self.verticalLayout.insertLayout(1, self.grid)

        self._setupRadioButtons()
        self._setupComboBox()

    def _setupComboBox(self):
        self.chordTypeComboBox.addItems([c.name for c in ChordInterval.getAllChordTypes__()])

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
