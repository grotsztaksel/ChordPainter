# -*- coding: utf-8 -*-
"""
Created on 17.10.2021 15:27 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['MainWindow']
__date__ = '2021-10-17'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QBrush
from PyQt5.QtWidgets import QDialog


class MainWindow(QDialog):
    def __init__(self, parent, pixmap):
        super().__init__(parent, Qt.Dialog)
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowContextHelpButtonHint)
        self.setFixedSize(pixmap.size() + QSize(1, 1))

        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))

        self.setPalette(palette)

    def keyPressEvent(self, event) -> None:
        """
        Press just any key to close the window
        """
        self.close()
