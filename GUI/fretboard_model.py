# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 21:28 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['FretboardModel']
__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import typing

from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QSize, QRect, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QStyledItemDelegate, QWidget, QSpinBox

from Instruments.instrument import Instrument
from chord_inventor import ChordInventor
from music_theory import NOTES, ChordInterval, getChordNotes


class FretboardModel(QAbstractItemModel):
    """
    Table model used to present notes on strings of a stringed instrument
    """

    def __init__(self, parent, instrument: Instrument):
        super().__init__(parent)
        self.instrument = instrument
        self.chordInventor = ChordInventor(self.instrument)
        self.editable = True
        self.currentChord = []

    def hasIndex(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> bool:
        if parent.isValid():
            return False
        return row < self.rowCount(parent) and column < self.columnCount(parent)

    def parent(self, index: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.instrument.nfrets + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.instrument.strings)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return section
            elif orientation == Qt.Horizontal:
                return len(self.instrument.strings) - section

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Allow editing open string notes. Do not allow selecting cells before the root fret
        """
        fret = index.row()
        string = self.stringFromIndex(index)
        if fret < self.instrument.rootfrets[string]:
            return Qt.NoItemFlags
        elif fret == self.instrument.rootfrets[string] and self.editable:
            return super(FretboardModel, self).flags(index) | Qt.ItemIsEditable
        else:
            return Qt.NoItemFlags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.DisplayRole or role == Qt.EditRole:
            return self.instrument.getNote(self.stringFromIndex(index), index.row())
        elif role == Qt.BackgroundRole and self.data(index, Qt.DisplayRole) in self.currentChord:
            if self.data(index, Qt.DisplayRole) == self.currentChord[0]:
                # Root note
                return QBrush(Qt.black)
            return QBrush(Qt.darkGray)
        elif role == Qt.ForegroundRole and self.data(index, Qt.DisplayRole) in self.currentChord:
            return QPen(Qt.white)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.EditRole) -> bool:
        if role != Qt.EditRole:
            return False
        if not self.editable:
            return False
        string = self.stringFromIndex(index)
        self.instrument.strings[string] = value
        return True

    def stringFromIndex(self, index):
        return len(self.instrument.strings) - index.column() - 1

    @pyqtSlot(str, str)
    def setCurrentChord(self, chordRoot, chordType):
        intvl = ChordInterval.getInterval(chordType)
        if intvl is None:
            self.currentChord = []
        else:
            self.currentChord = getChordNotes(chordRoot, intvl)
        topLeft = self.index(0, 0)
        bottomRight = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(topLeft, bottomRight)


class RootNoteSpinBox(QSpinBox):
    """Special spinbox to edit notes"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(-1)
        self.setMaximum(len(NOTES) + 1)
        self.setValue(0)

    def textFromValue(self, v: int) -> str:
        return NOTES[v % len(NOTES)]

    def valueFromText(self, text: str) -> int:
        return NOTES.index(text)

    def stepBy(self, step):
        if self.value() == 0 and step == -1:
            self.setValue(self.maximum())
        elif self.value() == self.maximum() - 1 and step == 1:
            self.setValue(0)
        super(RootNoteSpinBox, self).stepBy(step)


class FretboardDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fretPen = QPen()
        self.fretPen.setStyle(Qt.SolidLine)
        self.fretPen.setWidth(2)
        self.fretPen.setColor(Qt.black)

        self.rootFretPen = QPen(self.fretPen)
        self.rootFretPen.setWidth(6)

        self.stringPen = QPen()
        self.stringPen.setColor(Qt.black)
        self.stringPen.setWidth(1)
        self.stringPen.setStyle(Qt.SolidLine)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        return RootNoteSpinBox(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        editor.setValue(NOTES.index(index.data(Qt.EditRole)))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        model.setData(index, editor.textFromValue(editor.value()), Qt.EditRole)

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        fret = index.row()
        string = index.model().stringFromIndex(index)
        drawString = False
        painter.setRenderHint(QPainter.Antialiasing)

        if fret >= index.model().instrument.rootfrets[string]:
            painter.setPen(self.rootFretPen)
            if fret > index.model().instrument.rootfrets[string]:
                painter.setPen(self.fretPen)
                drawString = True
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        h = painter.font().pointSize() + 10
        rect = QRect(option.rect.center(), QSize(h, h))
        rect.moveCenter(option.rect.center())

        if drawString:
            painter.setPen(self.stringPen)
            c = rect.center().x()
            painter.drawLine(QPoint(c, option.rect.top()), QPoint(c, rect.top()))
            painter.drawLine(QPoint(c, rect.bottom()), QPoint(c, option.rect.bottom()))

        note = index.data(Qt.DisplayRole)

        pen = index.data(Qt.ForegroundRole)
        brush = index.data(Qt.BackgroundRole)

        if pen is None:
            pen = QPen()
            pen.setColor(Qt.black)
            pen.setWidth(1)

        painter.setPen(pen)

        if brush is None:
            brush = QBrush(Qt.NoBrush)

        painter.setBrush(brush)

        if note in index.model().currentChord:
            painter.drawEllipse(rect)
        painter.drawText(rect, Qt.AlignCenter, note)
