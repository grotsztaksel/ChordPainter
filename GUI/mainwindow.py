# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 22:13 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['MainWindow']
__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QRect, QMargins
from PyQt5.QtGui import QImage, QPainter, QRegion
from PyQt5.QtWidgets import QFileDialog, QRadioButton, QButtonGroup, QStyle

from GUI.fretboard_model import FretboardDelegate
from music_theory import NOTES

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.saveButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.setNoteButtons()
        self.tableView.setShowGrid(False)
        self.tableView.setItemDelegate(FretboardDelegate(self.tableView))

        hmin = self.tableView.verticalHeader().defaultSectionSize()
        self.tableView.verticalHeader().setDefaultSectionSize(max(hmin, 45))

        self.saveButton.clicked.connect(self.onSaveButtonClicked)

    def setNoteButtons(self):
        """
        Set up the radiobuttons for selecting chord root notes
        """
        self.chordRootButtons = QButtonGroup(self)
        iafter = 1
        for i, note in enumerate(NOTES):
            btn = QRadioButton(self)
            btn.setObjectName(note)
            btn.setText(note)
            self.chordRootButtons.addButton(btn, i)
            self.chordsLayout.insertWidget(iafter + i, btn)

    def adjustSizes(self):
        model = self.tableView.model()
        w = 0
        ncol = model.columnCount()
        for i in range(ncol):
            w = max(w, self.tableView.sizeHintForColumn(i))
        self.tableView.horizontalHeader().setDefaultSectionSize(w)

    @pyqtSlot()
    def onSaveButtonClicked(self):
        filename = QFileDialog.getSaveFileName(self, "Save fretboard", filter="*.png;; *.bmp;; *.jpg")
        if not filename:
            return
        self.saveFretboard(filename[0])

    def saveFretboard(self, fileName):

        model = self.tableView.model()
        topLeftIndex = model.index(0, 0)
        bottomRightIndex = model.index(model.rowCount() - 1, model.columnCount() - 1)
        bottomRightRect = self.tableView.visualRect(bottomRightIndex).marginsAdded(
            QMargins(0,
                     0,
                     self.tableView.verticalHeader().width(),
                     self.tableView.horizontalHeader().height()))
        bottomRight = bottomRightRect.bottomRight()
        rect = QRect(self.tableView.rect().topLeft(),
                     bottomRight)
        srcReg = QRegion(rect)
        self.tableView.scrollTo(topLeftIndex)
        # Keep the QImage and QPainter to prevent garbage collector from destroying them and getting memory errors on
        # Qt side
        self.img = QImage(rect.size(), QImage.Format_RGB32)
        self.p = QPainter(self.img)
        self.tableView.render(self.p, sourceRegion=srcReg)

        if self.img.save(fileName):
            print("Saved ", fileName)
