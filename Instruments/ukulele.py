# -*- coding: utf-8 -*-
"""
Created on 05.12.2021 18:39 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['Ukulele']
__date__ = '2021-12-05'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]


from Instruments.instrument import Instrument


class Ukulele(Instrument):
    def __init__(self):
        super().__init__()
        self.name = "Ukulele"
        self.strings = list("AECG")
        self.nfrets = 12
        self.rootfrets = len(self.strings) * [0]
        self.dotsOnFrets = [3, 5, 7, 10]