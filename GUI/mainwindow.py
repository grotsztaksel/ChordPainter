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
from PyQt5.QtCore import Qt, pyqtSlot, QRect, QMargins, QPoint, QObject, QEvent
from PyQt5.QtGui import QImage, QPainter, QRegion
from PyQt5.QtWidgets import QFileDialog, QRadioButton, QButtonGroup, QStyle, QTableView, QToolButton, QSizePolicy

from GUI.fretboard_model import FretboardDelegate
from music_theory import NOTES

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)

        self.saveButton = QToolButton(self)
        self.saveButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.saveButton.setMaximumSize(self.saveButton.sizeHint())
        self.saveButton.hide()

        self.setNoteButtons()
        self.fretboardView.setShowGrid(False)
        self.fretboardView.setItemDelegate(FretboardDelegate(self.fretboardView))

        self.fretboardView.installEventFilter(self)

        hmin = self.fretboardView.verticalHeader().defaultSectionSize()
        self.fretboardView.verticalHeader().setDefaultSectionSize(max(hmin, 45))

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
        model = self.fretboardView.model()
        w = 0
        ncol = model.columnCount()
        for i in range(ncol):
            w = max(w, self.fretboardView.sizeHintForColumn(i))
        self.fretboardView.horizontalHeader().setDefaultSectionSize(w)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        """
        Show or hide buttons over widgets
        """
        if object == self.fretboardView and event.type() == QEvent.Enter:
            point = self.fretboardView.rect().bottomRight() \
                    - QPoint(self.saveButton.width(), self.saveButton.height()) \
                    - QPoint(20, 20)
            self.saveButton.move(self.fretboardView.mapToParent(point))
            self.saveButton.show()
            return True
        elif object == self.fretboardView and event.type() == QEvent.Leave:
            self.saveButton.hide()
            return True

        return super().eventFilter(object, event)

    @pyqtSlot()
    def onSaveButtonClicked(self):
        filename = QFileDialog.getSaveFileName(self, "Save fretboard", filter="*.png;; *.bmp;; *.jpg")
        if not filename:
            return
        self.saveFretboard(filename[0])

    def saveFretboard(self, fileName):
        """
        Save the content of the fretboard view. Use a temporary widget so that it can be arbitrarily resized to
        encompass the entire fretboard. Otherwise would not be able to render the parts that are clipped from
        the scroll area
        """
        model = self.fretboardView.model()
        tmpView = QTableView()
        tmpView.verticalHeader().setDefaultSectionSize(self.fretboardView.verticalHeader().defaultSectionSize())
        tmpView.horizontalHeader().setDefaultSectionSize(self.fretboardView.horizontalHeader().defaultSectionSize())
        tmpView.setModel(model)
        tmpView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tmpView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tmpView.setItemDelegate(self.fretboardView.itemDelegate())
        tmpView.setShowGrid(self.fretboardView.showGrid())

        topLeftIndex = model.index(0, 0)
        bottomRightIndex = model.index(model.rowCount() - 1, model.columnCount() - 1)
        bottomRightRect = tmpView.visualRect(bottomRightIndex).marginsAdded(
            QMargins(0,
                     0,
                     tmpView.verticalHeader().width(),
                     tmpView.horizontalHeader().height()))
        bottomRight = bottomRightRect.bottomRight()
        rect = QRect(tmpView.rect().topLeft(),
                     bottomRight)
        srcReg = QRegion(rect)
        tmpView.scrollTo(topLeftIndex)
        tmpView.setFixedSize(rect.size())
        tmpView.show()
        # Keep the QImage and QPainter to prevent garbage collector from destroying them and getting memory errors on
        # Qt side
        self.img = QImage(rect.size(), QImage.Format_RGB32)
        self.p = QPainter(self.img)
        tmpView.render(self.p, sourceRegion=srcReg)

        if self.img.save(fileName):
            print("Saved ", fileName)

        tmpView.deleteLater()
