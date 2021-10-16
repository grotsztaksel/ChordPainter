# -*- coding: utf-8 -*-
"""
Created on 16.10.2021 17:40 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['Chord']
__date__ = '2021-10-16'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from collections import namedtuple
import re

Chord = namedtuple("Chord", ["name", "scheme"])
Chord.__doc__ = """
                A tuple representing a chord. 
                An instrument can have multiple chords with the same name as long as their diagram schemes are different
                """
Chord.__len__ = len(Chord.scheme)

CHORD_PATTERN = re.compile(
    r"([A-Ha-h]|(A-H)(maj|m)?)(\+|0|6|6/9|7|7b5|7sus4|9|sus2|sus4|add9)"  # This can probably get better
)
