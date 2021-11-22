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

CHORD_SUFFIXES = r"(\+|0|6|6\/9|7|7b5|7sus4|9|sus2|sus4|add9)?"
CHORD_ENGLISH = re.compile(r"[A-G]#?m?" + CHORD_SUFFIXES)
CHORD_GERMAN = re.compile(r"([AaEe]s?|[CDcdF-hf-h](is)?)" + CHORD_SUFFIXES)

Chord = namedtuple("Chord", ["name", "scheme", "prefix", "suffix"], defaults=["", ""])
Chord.__doc__ = """
                A tuple representing a chord. 
                An instrument can have multiple chords with the same name as long as their diagram schemes are different

                """


class Chord(Chord):
    def __len__(self):
        return len(self.scheme)

    def fret(self, istring):
        """
        Unpacks the i-th item from the scheme and returns the fret that should be pressed
        """
        c = self.scheme[istring]
        if isinstance(c, int):
            return c
        return c[0]

    def finger(self, istring):
        """
        Unpacks the i-th item from the scheme and returns the finger that should be used to press the string
        """
        c = self.scheme[istring]
        if isinstance(c, int):
            return None
        elif len(c) < 1:
            return None
        return c[1]

    @property
    def toString(self):
        """
        Convert the chord name to a string that could be used as a valid file name (or at the core of the file name)
        """
        n = self.name  # for short

        m_eng = CHORD_ENGLISH.fullmatch(n)
        if m_eng:
            output = n[0]

            i = 0
            if "#" in n:
                output += "_sharp"
                i = 1
            try:
                if n[1 + i] == "m":
                    output += "_minor"
                else:
                    output += "_major"
            except IndexError:
                output += "_major"

            suffix = m_eng.group(1)
            if suffix:
                output += "_" + suffix

            return output.replace("/", "by").replace("+", "plus")

        m_ger = CHORD_GERMAN.fullmatch(n)
        if m_ger:
            output = n[0].upper()
            try:
                if n[1] == "s" or n[1:3] == "is":
                    output += "_sharp"
            except IndexError:
                pass
            if output[0] == n[0]:
                output += "_major"
            else:
                output += "_minor"

            suffix = m_ger.group(3)
            if suffix:
                output += "_" + suffix

            return output.replace("/", "by").replace("+", "plus")

        else:
            raise ValueError("{} matches neither English nor German naming convention".format(self.name))
