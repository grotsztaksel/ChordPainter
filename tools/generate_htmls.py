# -*- coding: utf-8 -*-
"""
Created on 06.12.2021 21:29 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-12-06'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os
from copy import copy

from music_theory import NOTES, ChordInterval, ChordType

htmdir = os.path.join(os.path.dirname(__file__), "..", "HTML")
template_file = os.path.join(htmdir, "chord_page_template.xhtml")
imgdir = os.path.join(os.path.dirname(__file__), "..", "img")

with open(template_file, 'r') as tf:
    TEMPLATE = tf.read()

use_types = [ChordInterval.major,
             ChordInterval.minor,
             ChordInterval.diminished,
             ChordInterval.dominant_7,
             ChordInterval.min_7]


def writeHtml(instrument, root, chordType: ChordType, htmFullPath, images):
    htm = copy(TEMPLATE)
    htm = htm.replace("${instrument}", instrument)
    htm = htm.replace("${chordroot}", root)
    htm = htm.replace("${chordtype}", chordType.name)
    htmName = os.path.basename(htmFullPath)
    majorname = htmName.replace(chordType.name, "major")
    # Highlight the chord root and remove the hyperlink. Do that only once
    htm = htm.replace(f'<p><a href="./{majorname}">{root}</a></p>',
                      f'<p class="highlight">{root}</p>', 1)

    # Highlight the currently selected chord type and remove self-hyperlink in the htm file
    htm = htm.replace(f'<p><a href="./{htmName}">{root}{chordType.annotations[-1]}</a></p>',
                      f'<p class="highlight">{root}{chordType.annotations[-1]}</p>')

    # Build the list of images:
    imgnodes = []
    for img in images:
        imgnodes.append(f'<img src="./img/{img}" alt="Diagram not found"/>')
    htm = htm.replace("${images}", "\n        ".join(imgnodes))

    with open(htmFullPath, 'w') as h:
        h.write(htm)


def paintFretboard(root, chordType, imgName):
    pass

# for root in NOTES:
#     for chordType in use_types:
#         writeHtml(root, chordType)
#         paintFretboard(root, chordType)
