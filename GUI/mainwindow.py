# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 22:13 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['MainWindow']
__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import json
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QRect, QMargins, QPoint, QObject, QEvent
from PyQt5.QtGui import QImage, QPainter, QRegion
from PyQt5.QtWidgets import QFileDialog, QStyle, QTableView, QToolButton

import Instruments
from GUI.define_instrument_dialog import DefineInstrumentDialog
from GUI.fretboard_model import FretboardDelegate, FretboardModel
from Instruments.instrument import Instrument

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)

        self.newInstrumentButton.clicked.connect(self.onNewInstrumentClicked)

        self.saveFretboardButton = QToolButton(self)
        self.saveFretboardButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveFretboardButton.clicked.connect(self.onSaveFretboardClicked)
        self.saveFretboardButton.setMaximumSize(self.saveFretboardButton.sizeHint())
        self.saveFretboardButton.hide()

        self.saveChordButton = QToolButton(self)
        self.saveChordButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveChordButton.clicked.connect(self.onSaveChordClicked)
        self.saveChordButton.setMaximumSize(self.saveChordButton.sizeHint())
        self.saveChordButton.hide()

        self.fretboardView.setShowGrid(False)
        self.fretboardView.setItemDelegate(FretboardDelegate(self.fretboardView))

        self.fretboardView.installEventFilter(self)
        self.chordPicWidget.installEventFilter(self)

        hmin = self.fretboardView.verticalHeader().defaultSectionSize()
        self.fretboardView.verticalHeader().setDefaultSectionSize(max(hmin, 45))
        self.jdata = None
        self._readData()

        self.instrumentComboBox.addItems(self.getInstrumentList())
        self.instrumentComboBox.currentIndexChanged.connect(self.onInstrumentSelected)

        self.onInstrumentSelected(self.instrumentComboBox.currentIndex())
        self.adjustSizes()

    def _readData(self):
        jfile = os.path.join(os.path.dirname(Instruments.instrument.__file__), "instruments.json")
        with open(jfile, 'r') as f:
            data = f.read()
        self.jdata = json.loads(data)

    def setModel(self, model):
        if self.fretboardView.model() is not None:
            self.chordSelector.disconnect()
            self.fretboardView.model().deleteLater()
        self.fretboardView.setModel(model)
        self.chordSelector.chordSelected.connect(model.setCurrentChord)

        # Show the same chord on the new instrument
        self.chordSelector.emitChord()

    def getInstrumentList(self):
        """
        Return a list of names of instruments defined in the data
        """
        if self.jdata is None:
            return []

        return [instr["name"] for instr in self.jdata["instrument"]]

    @pyqtSlot(int)
    def onInstrumentSelected(self, i):
        newInstrument = Instrument.fromData(self.jdata["instrument"][i])
        newModel = FretboardModel(self, newInstrument)
        self.setModel(newModel)

    @pyqtSlot(str)
    def addInstrument(self, instr):
        """Add a new instrument definition to the database"""
        newInstr = json.loads(instr)
        self.jdata["instrument"].append(newInstr)
        self.instrumentComboBox.addItem(newInstr["name"])
        self.instrumentComboBox.setCurrentIndex(self.instrumentComboBox.count() - 1)

    @pyqtSlot()
    def onNewInstrumentClicked(self):
        """Show dialog to define a new instrument"""
        dialog = DefineInstrumentDialog(self)
        dialog.emitInstrumentDefinition.connect(self.addInstrument)
        dialog.exec()

    def adjustSizes(self):
        model = self.fretboardView.model()
        w = 0
        ncol = model.columnCount()
        for i in range(ncol):
            w = max(w, self.fretboardView.sizeHintForColumn(i))
        self.fretboardView.horizontalHeader().setDefaultSectionSize(w)
        self.fretboardView.setMinimumWidth(self.fretboardView.sizeHint().width())

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        """
        Show or hide buttons over widgets
        """
        if object == self.fretboardView and event.type() == QEvent.Enter:
            point = self.fretboardView.rect().bottomRight() \
                    - QPoint(self.saveFretboardButton.width(), self.saveFretboardButton.height()) \
                    - QPoint(20, 20)
            self.saveFretboardButton.move(self.fretboardView.mapToParent(point))
            self.saveFretboardButton.show()
            return True
        elif object == self.fretboardView and event.type() == QEvent.Leave:
            self.saveFretboardButton.hide()
            return True
        elif object == self.chordPicWidget and event.type() == QEvent.Enter:
            point = self.chordPicWidget.rect().bottomRight() \
                    - QPoint(self.saveChordButton.width(), self.saveChordButton.height()) \
                    - QPoint(20, 20)
            self.saveChordButton.move(self.chordPicWidget.mapTo(self, point))
            self.saveChordButton.show()
            return True
        elif object == self.chordPicWidget and event.type() == QEvent.Leave:
            self.saveChordButton.hide()
            return True

        return super().eventFilter(object, event)

    @pyqtSlot()
    def onSaveFretboardClicked(self):
        filename = QFileDialog.getSaveFileName(self, "Save fretboard", filter="*.png;; *.bmp;; *.jpg")
        if not filename:
            return
        self.saveFretboard(filename[0])

    @pyqtSlot()
    def onSaveChordClicked(self):
        pass

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
