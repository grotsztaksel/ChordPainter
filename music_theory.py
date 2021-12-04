# -*- coding: utf-8 -*-
"""
Created on 04.12.2021 23:06 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Collection of general princoples from music theory
"""

__date__ = '2021-12-04'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


class ChordInterval(object):
    """
    Lists of intervals that define different kinds of chords
    """
    major = [4, 3]
    minor = [3, 4]
    diminished = [3, 3]
