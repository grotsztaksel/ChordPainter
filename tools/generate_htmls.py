# -*- coding: utf-8 -*-
"""
Created on 06.12.2021 21:29 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-12-06'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os

from music_theory import NOTES, ChordInterval

htmdir = os.path.join(os.path.dirname(__file__), "..", "HTML")
template_file = os.path.join(htmdir, "chord_page_template.xhtml")
imgdir = os.path.join(os.path.dirname(__file__), "..", "img")


with open(template_file, 'r') as tf:
    template = tf.read()

# for note in NOTES:
#     for chordType in ChordInterval.getAllChordTypes__():
#