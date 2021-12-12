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
from PyQt5.QtWidgets import QFileDialog

from GUI.fretboard_model import FretboardDelegate

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.tableView.setShowGrid(False)
        self.tableView.setItemDelegate(FretboardDelegate(self.tableView))

        hmin = self.tableView.verticalHeader().defaultSectionSize()
        self.tableView.verticalHeader().setDefaultSectionSize(max(hmin, 45))

        self.saveButton.clicked.connect(self.onSaveButtonClicked)

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
        print ("Survived saveFretBoard")

    def saveFretboard(self, fileName):

        model = self.tableView.model()
        topLeft = model.index(0, 0)
        bottomRight = model.index(model.rowCount() - 1, model.columnCount() - 1)
        rect = QRect.united(self.tableView.visualRect(topLeft), self.tableView.visualRect(bottomRight)).marginsAdded(
            QMargins(0, 0, self.tableView.horizontalOffset(), self.tableView.verticalOffset()))
        srcReg = QRegion(rect)
        img = QImage(rect.size(), QImage.Format_RGB32)
        p = QPainter(img)
        self.tableView.render(p, sourceRegion=srcReg)

        if img.save(fileName):
            print("Saved ", fileName)
