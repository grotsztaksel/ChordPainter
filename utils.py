# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 17:16 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

General purpose utilities
"""

__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import QRect, QSize


def square(rect: QRect, maximize=False) -> QRect:
    """
    Return a square with the center in the center the same as the input rectangle. With the size adjusted to match
    the largest (maximize = True) or smallest (maximize = False) side of the input rect
    """
    c = rect.center()
    rect = QRect(rect)
    w = rect.width()
    h = rect.height()
    if maximize:
        s = max(w, h)
    else:
        s = min(w, h)
    rect.setSize(QSize(s, s))
    rect.moveCenter(c)
    return rect
