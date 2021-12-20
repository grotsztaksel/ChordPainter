#!/usr/bin/env python
# -*- encoding: utf-8 -*-


__all__ = ['app']
__authors__ = ['Piotr Gradkowski <Piotr.Gradkowski@dlr.de>']
__date__ = '2021-12-20'

import sys

from PyQt5.QtWidgets import QApplication

# An app object is required so that the widgets can be created in the tests
app = QApplication(sys.argv)
