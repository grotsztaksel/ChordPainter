# -*- coding: utf-8 -*-
"""
Created on 12.10.2021 21:54

@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__authors__ = ['Piotr Gradkowski <grotsztaksel@o2.pl>']
__date__ = '2021-10-12'

import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from chord import Chord
from chord_painter import ChordPainter
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Using a QApplication appears to mitigate the crash that would otherwise occur upon constructing a QPixmap.
    #
    size = QSize(141, 320)
    crd = Chord("c", ((2, 1), 0, (2, 2), (2, 3)))
    painter = ChordPainter(crd, size)
    painter.strings.draw()
    painter.frets.draw()
    painter.frets.drawDot(3)
    painter.symbols.drawFinger(0, 3)
    painter.symbols.drawOpenString(3)
    painter.symbols.drawMuteString(2)
    painter.symbols.drawFinger(3, 1, 3)
    painter.firstFretVisible = 3
    painter.frets.drawFretNumber()
    painter.p.end()
    px = painter.pixmap
    mw = MainWindow(None, px)
    mw.exec()

    sys.exit(app.exit())
