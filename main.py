# -*- coding: utf-8 -*-
"""
Created on 12.10.2021 21:54

@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__authors__ = ['Piotr Gradkowski <grotsztaksel@o2.pl>']
__date__ = '2021-10-12'

import os
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from banjo import Banjo_5string as Banjo
from chord_painter import ChordPainter
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Using a QApplication appears to mitigate the crash that would otherwise occur upon constructing a QPixmap.
    #
    size = QSize(141, 320)
    banjo = Banjo()

    targetDir = os.path.join(os.getcwd(), "images")
    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)

    for chord in banjo.chords:

        painter = ChordPainter(chord, size, banjo)
        painter.drawEmpty()
        painter.drawChord()
        painter.p.end()
        px = painter.pixmap

        filenum = 0
        ext = ".png"
        fileName = chord.toString + chord.suffix
        targetFileName = fileName + ext
        while os.path.isfile(os.path.join(targetDir, targetFileName)):
            filenum += 1
            targetFileName = fileName + "_" + str(filenum) + ext

        px.save(os.path.join(targetDir, targetFileName))
        mw = MainWindow(None, px)
        mw.setWindowTitle(chord.name)
        # mw.exec()

    sys.exit(app.exit())
