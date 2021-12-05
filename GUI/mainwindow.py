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
from PyQt5.QtCore import Qt

from GUI.fretboard_model import FretboardDelegate

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.tableView.setShowGrid(False)
        self.tableView.setItemDelegate(FretboardDelegate(self.tableView))

    def adjustSizes(self):
        model = self.tableView.model()
        w = 0
        ncol = model.columnCount()
        for i in range(ncol):
            w = max(w, self.tableView.sizeHintForColumn(i))
        for i in range(ncol):
            self.tableView.setColumnWidth(i, w)
