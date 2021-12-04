# -*- coding: utf-8 -*-
"""
Created on 14.10.2021 22:38 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['Guitar']
__date__ = '2021-10-14'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from Instruments.instrument import Instrument


class Guitar(Instrument):
    def __init__(self):
        super().__init__()
        self.name = "Guitar"
        self.strings = list("EHGDAE")
        self.nfrets = 20
        self.rootfrets = len(self.strings) * [0]

        self.dotsOnFrets = [3, 5, 7, 9, 12, 15, 17]
        self.defineChord("E", (0, 2, 2, 1, 0, 0))
        self.defineChord("e", (0, 2, 2, 0, 0, 0))
        self.defineChord("D", (
            None,  # Mute the first string
            0,  # Leave the second string open
            0,  # Leave the third string open
            (2, 1),  # Press 4th string on 2nd fret with 1st finger
            (3, 3),  # Press 5th string on 3rd fret with 3rd finger
            (2, 2)  # Press 6th string on 2nd fret with 2nd finger
        ))

        # ... etc.
