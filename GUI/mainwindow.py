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
from PyQt5.QtCore import Qt, pyqtSlot, QRect, QPoint, QObject, QEvent, QModelIndex
from PyQt5.QtWidgets import QStyle, QToolButton, QLineEdit

import Instruments
from GUI.define_instrument_dialog import DefineInstrumentDialog
from GUI.fretboard_model import FretboardModel
from Instruments.instrument import Instrument

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.model = None

        self.saveChordButton = QToolButton(self)
        self.saveChordButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveChordButton.clicked.connect(self.onSaveChordClicked)
        self.saveChordButton.setMaximumSize(self.saveChordButton.sizeHint())
        self.saveChordButton.hide()

        self.chordPicWidget.installEventFilter(self)

        self.jdata = None
        self.jfile = os.path.join(os.path.dirname(Instruments.instrument.__file__), "instruments.json")
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

        self.saveAllButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveAllButton.clicked.connect(self._saveData)
        self.onInstrumentSelected(self.instrumentComboBox.currentIndex())
        self.fretboardView.adjustSizes()

    def _readData(self):

        with open(self.jfile, 'r') as f:
            data = f.read()
        self.jdata = json.loads(data)

    def setModel(self, model):
        if self.model is not None:
            self.model.deleteLater()
        self.model = model
        self.fretboardView.setModel(model)
        self.chordSelector.chordSelected.connect(model.setCurrentChord)
        self.model.dataChanged.connect(self.checkTuning)

        # Show the same chord on the new instrument
        self.chordSelector.emitChord()

    def _saveData(self):
        """
        Save all instruments to a JSON file
        """
        i = self.instrumentComboBox.currentIndex()
        instr = self.model.instrument
        if len(self.jdata["instrument"]) > i:
            jinstr = self.jdata["instrument"][i]
        else:
            self.jdata["instrument"].append({})
            jinstr = self.jdata["instrument"][-1]
        jinstr["name"] = instr.name
        jinstr["strings"] = "".join(instr.tuning[0][1])
        jinstr["nfrets"] = instr.nfrets
        jinstr["dotsOnFrets"] = instr.dotsOnFrets
        if any(instr.rootfrets):
            jinstr["rootfrets"] = instr.rootfrets

        if len(instr.tuning) > 1:
            l = []
            jinstr["tuning"] = l
            for t in instr.tuning[1:]:
                name = t[0]
                strings = t[1]
                d = {"strings": "".join(strings)}
                if name is not None:
                    d["name"] = name
                l.append(d)

        with open(self.jfile, 'w') as f:
            f.write(json.dumps(self.jdata, indent=2))

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

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        """
        Show or hide buttons over widgets
        """
        if object == self.chordPicWidget and event.type() == QEvent.Enter:
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
    def onSaveChordClicked(self):
        pass
