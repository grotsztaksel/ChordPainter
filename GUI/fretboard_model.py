# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 21:28 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['FretboardModel']
__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import typing

from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex

from Instruments.instrument import Instrument
from chord_inventor import ChordInventor


class FretboardModel(QAbstractItemModel):
    """
    Table model used to present notes on strings of a stringed instrument
    """

    def __init__(self, parent, instrument: Instrument):
        super().__init__(parent)
        self.instrument = instrument
        self.chordInventor = ChordInventor(self.instrument)
        self.editable = False

    def hasIndex(self, row: int, column: int, parent: QModelIndex = ...) -> bool:
        if parent.isValid():
            return False
        return row < self.rowCount(parent) and column < self.columnCount(parent)

    def parent(self, index: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.instrument.nfrets + 1

    def columnCount(self, parent: QModelIndex = ...) -> int:
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
        string = len(self.instrument.strings) - index.column() - 1
        if fret < self.instrument.rootfrets[string]:
            return Qt.NoItemFlags
        elif fret == self.instrument.rootfrets[string] and self.editable:
            return super(FretboardModel, self).flags(index) | Qt.ItemIsEditable
        else:
            return super(FretboardModel, self).flags(index)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.DisplayRole or role == Qt.EditRole:
            return self.instrument.getNote(len(self.instrument.strings) - index.column() - 1, index.row())
