# -*- coding: utf-8 -*-
"""
Created on 12.10.2021 21:54

@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__authors__ = ['Piotr Gradkowski <grotsztaksel@o2.pl>']
__date__ = '2021-10-12'

import os
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication

from chord import Chord
from chord_painter import ChordPainter



def main():
    # Use a breakpoint in the code line below to debug your script.


    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Using a QApplicaion appears to mitigate the crasch that would otherwise occur opun constructing a QPixmap.
    #
    size = QSize(480, 640)
    crd = Chord("c", ((2, 1), 0, (2, 2), (2, 3)))
    painter = ChordPainter(crd, size)
    painter.drawStrings()
    painter.drawFrets()
    painter.p.end()
    px = painter.pixmap
    px.save("example.png", "PNG")
    sys.exit(app.exit())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
