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
from copy import copy

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QRect, QMargins, QPoint, QObject, QEvent, QModelIndex
from PyQt5.QtGui import QImage, QPainter, QRegion
from PyQt5.QtWidgets import QFileDialog, QStyle, QTableView, QToolButton, QLineEdit

import Instruments
from GUI.define_instrument_dialog import DefineInstrumentDialog
from GUI.fretboard_model import FretboardDelegate, FretboardModel
from Instruments.instrument import Instrument

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.model = None

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
        self.instrumentComboBox.insertSeparator(self.instrumentComboBox.count())
        self.instrumentComboBox.addItem("new...")
        self.instrumentComboBox.activated.connect(self.onInstrumentSelected)
        self.tuningComboBox.currentIndexChanged.connect(self.onTuningSelected)

        self.saveTuningButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveTuningButton.clicked.connect(self.onSaveTuningClicked)
        self.saveTuningButton.setEnabled(False)

        self.tuningNameEditor = QLineEdit(self)
        self.tuningNameEditor.hide()
        self.tuningNameEditor.returnPressed.connect(self.saveTuning)
        self.tuningNameEditor.editingFinished.connect(lambda: self.tuningNameEditor.hide())

        self.onInstrumentSelected(self.instrumentComboBox.currentIndex())
        self.adjustSizes()

    def _readData(self):
        jfile = os.path.join(os.path.dirname(Instruments.instrument.__file__), "instruments.json")
        with open(jfile, 'r') as f:
            data = f.read()
        self.jdata = json.loads(data)

    def setModel(self, model):
        if self.model is not None:
            self.chordSelector.disconnect()
            self.model.deleteLater()
        self.model = model
        self.fretboardView.setModel(model)
        self.chordSelector.chordSelected.connect(model.setCurrentChord)
        self.model.dataChanged.connect(self.checkTuning)

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
        if i >= len(self.jdata["instrument"]):
            return self.onNewInstrumentClicked()

        newInstrument = Instrument.fromData(self.jdata["instrument"][i])
        newModel = FretboardModel(self, newInstrument)
        self.setModel(newModel)
        self.tuningComboBox.clear()
        for t in self.model.instrument.tuning:
            notes = ", ".join(t[1])
            name = t[0]
            if name is None:
                self.tuningComboBox.addItem(notes)
            else:
                self.tuningComboBox.addItem(f"{name} ({notes})")

    @pyqtSlot(int)
    def onTuningSelected(self, i):
        tuning = self.model.instrument.tuning[i]

        row = 0
        for string, note in enumerate(reversed(tuning[1])):
            index = self.model.index(row, string)
            self.model.setData(index, note, Qt.EditRole)

        index_from = self.model.index(row, 0)
        index_to = self.model.index(row, len(tuning[1]) - 1)
        self.model.dataChanged.emit(index_from, index_to)

    @pyqtSlot()
    def onSaveTuningClicked(self):
        """
        Show a line editor allowing to enter the new tuning name. 
        If a name is not selected, the tuning is saved without name
        """
        name = ", ".join(self.model.instrument.strings)
        self.tuningNameEditor.setGeometry(
            QRect.united(self.tuningComboBox.geometry(), self.saveTuningButton.geometry()))
        # self.tuningNameEditor.move(self.tuningComboBox.mapTo(self, self.tuningComboBox.geometry().topLeft()))
        self.tuningNameEditor.show()
        self.tuningNameEditor.setText(name)
        self.tuningNameEditor.selectAll()
        self.tuningNameEditor.setFocus(Qt.OtherFocusReason)

    @pyqtSlot()
    def saveTuning(self):
        name = self.tuningNameEditor.text()
        s = copy(self.model.instrument.strings)
        if name == ", ".join(s):
            name = None

        self.model.instrument.tuning.append((name, s))
        self.tuningComboBox.addItem(f"{name} ({', '.join(s)})")
        self.tuningNameEditor.hide()

    @pyqtSlot(QModelIndex, QModelIndex)
    def checkTuning(self, tlIndex=QModelIndex(), brIndex=QModelIndex()):
        """
        Checks if the currently (manually) set tuning can be found in the list of tunings.
        If yes, select it from the combo box. If not, offer the option to save the new custom tuning
        """
        if tlIndex.row() != 0 and brIndex.row() != 0:
            return
        tuningIsKnown = False
        for i, t in enumerate(self.model.instrument.tuning):
            if t[1] == self.model.instrument.strings:
                tuningIsKnown = True
                break

        self.saveTuningButton.setEnabled(not tuningIsKnown)

        if tuningIsKnown:
            self.tuningComboBox.blockSignals(True)
            self.tuningComboBox.setCurrentIndex(i)
            self.tuningComboBox.blockSignals(False)

    @pyqtSlot(str)
    def addInstrument(self, instr):
        """Add a new instrument definition to the database"""
        newInstr = json.loads(instr)
        self.jdata["instrument"].append(newInstr)
        self.instrumentComboBox.insertItem(self.instrumentComboBox.count() - 2, newInstr["name"])
        self.instrumentComboBox.setCurrentIndex(self.instrumentComboBox.count() - 1)

    @pyqtSlot()
    def onNewInstrumentClicked(self):
        """Show dialog to define a new instrument"""
        dialog = DefineInstrumentDialog(self)
        dialog.emitInstrumentDefinition.connect(self.addInstrument)
        dialog.exec()

    def adjustSizes(self):
        model = self.model
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
        model = self.model
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
