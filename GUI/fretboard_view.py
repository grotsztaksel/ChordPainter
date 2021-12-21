#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['FretboardView']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-21'

from PyQt5.QtCore import Qt, pyqtSlot, QPoint, QEvent, QMargins, QRect
from PyQt5.QtGui import QImage, QPainter, QRegion
from PyQt5.QtWidgets import QTableView, QToolButton, QStyle, QFileDialog

from GUI.fretboard_model import FretboardDelegate


class FretboardView(QTableView):
    """
    Special view implementing required extra behavior
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setShowGrid(False)
        self.setItemDelegate(FretboardDelegate(self))
        self.setMouseTracking(True)

        self.installEventFilter(self)


        hmin = self.verticalHeader().defaultSectionSize()
        self.verticalHeader().setDefaultSectionSize(max(hmin, 45))

        self._setupSaveButton()

    def _setupSaveButton(self):
        self.saveFretboardButton = QToolButton(self)
        self.saveFretboardButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.saveFretboardButton.clicked.connect(self.onSaveFretboardClicked)
        self.saveFretboardButton.setMaximumSize(self.saveFretboardButton.sizeHint())
        self.saveFretboardButton.hide()

    def enterEvent(self, a0: QEvent) -> None:
        point = self.rect().bottomRight() \
                - QPoint(self.saveFretboardButton.width(), self.saveFretboardButton.height()) \
                - QPoint(20, 20)
        self.saveFretboardButton.move(point)
        self.saveFretboardButton.show()

    def leaveEvent(self, a0: QEvent) -> None:
        self.saveFretboardButton.hide()

    @pyqtSlot()
    def onSaveFretboardClicked(self):
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
        model = self.model()
        tmpView = FretboardView()
        tmpView.setModel(model)
        tmpView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tmpView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

    def adjustSizes(self):
        model = self.model()
        if model is None:
            return
        w = 0
        ncol = model.columnCount()
        for i in range(ncol):
            w = max(w, self.sizeHintForColumn(i))
        self.horizontalHeader().setDefaultSectionSize(w)
        self.setMinimumWidth(self.sizeHint().width())
