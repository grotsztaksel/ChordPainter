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

from GUI.fretboard_model import FretboardModel
from GUI.mainwindow import MainWindow
from Instruments.banjo import Banjo_5string as Banjo
from Instruments.guitar import Guitar
from Instruments.ukulele import Ukulele
from file_register import FileRegister


class Interval(object):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Using a QApplication appears to mitigate the crash that would otherwise occur upon constructing a QPixmap.
    #
    size = QSize(160, 920)
    banjo = Banjo()
    guitar = Guitar()
    uke = Ukulele()
    targetDir = os.path.join(os.getcwd(), "img")
    # targetDir = r'C:\Users\piotr\Documents\Songs XML\SeparateFiles\img'

    filereg = FileRegister()

    # chordTypes = ChordInterval.getAllChordTypes()


    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)


    # painter = FretboardPainter(size, banjo)
    # px = painter.pixmap
    mw = MainWindow(None)
    model = FretboardModel(mw, banjo)
    mw.fretboardView.setModel(model)
    mw.setWindowTitle("ChordPainter")
    mw.adjustSizes()
    mw.show()
    # for chord in banjo.chords:
    #     painter = ChordPainter(chord, size, banjo)
    #     painter.drawEmpty()
    #     painter.drawChord()
    #     painter.p.end()
    #     px = painter.pixmap
    #
    #     filesSaved = []
    #     filenum = 0
    #     ext = ".png"
    #     fileName = chord.prefix + chord.toString + chord.suffix + ext
    #
    #     pngName = filereg.getUniqueName(os.path.join(targetDir, fileName))
    #     px.save(pngName)
    #     print("Saved ", pngName)
    #     filereg.register(pngName)


    sys.exit(app.exec_())
