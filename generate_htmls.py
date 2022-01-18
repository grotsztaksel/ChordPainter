# -*- coding: utf-8 -*-
"""
Created on 06.12.2021 21:29 12
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-12-06'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os

try:
    # Enable importing modules from PATH environmental variable (Python 3.8+ on Windows)
    _dllDirs = [os.add_dll_directory(d) for d in
                os.environ["PATH"].split(";") +
                [os.path.abspath(os.path.join(os.path.dirname(__file__), ""))] +
                [os.getcwd()] if
                os.path.isdir(d)]
except AttributeError:
    pass

import logging
import sys
from copy import copy

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from Instruments.banjo import Banjo_5string
from Instruments.guitar import Guitar
from Instruments.ukulele import Ukulele
from fretboard_painter import FretboardPainter
from music_theory import NOTES, ChordInterval, ChordType, getChordNotes

htmdir = os.path.join(os.path.dirname(__file__), "", "HTML")
template_file = os.path.join(htmdir, "chord_page_template.xhtml")
imgdir = os.path.join(os.path.dirname(__file__), "", "img")

with open(template_file, 'r') as tf:
    TEMPLATE = tf.read()

use_types = [ChordInterval.major,
             ChordInterval.minor,
             ChordInterval.diminished,
             ChordInterval.dominant_7,
             ChordInterval.min_7]


def main():
    logfile = "generate_htmls.log"
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[
                            logging.FileHandler(logfile, 'w', 'utf-8'),
                            logging.StreamHandler(sys.stdout)
                        ]
                        )
    print("Logging information to {}".format(os.path.abspath(os.path.join(os.getcwd(), logfile))))

    generateAllHtmls()


def generateAllHtmls():
    for instrument in ['banjo', 'guitar']:
        for root in NOTES:
            for chordType in use_types:
                images = []
                if instrument == 'banjo':
                    ins = Banjo_5string()
                    images.append(paintFretboard(ins, root, chordType, "/".join([".", "img", "banjo_openG__"])))
                    ins.strings = list("DCGCG")
                    images.append(paintFretboard(ins, root, chordType, "/".join([".", "img", "banjo_doubleC"])))
                elif instrument == "guitar":
                    ins = Guitar()
                    images.append(paintFretboard(ins, root, chordType, "/".join([".", "img", "guitar"])))
                    ins = Ukulele()
                    images.append(paintFretboard(ins, root, chordType, "/".join([".", "img", "ukulele"])))
                else:
                    raise ValueError(f"{instrument}: Don't know what to do!")

                htm = "{}_{}_{}.xhtml".format(instrument, root, chordType.name.replace(" ", "_"))
                writeHtml(instrument, root, chordType, htm, images)


def writeHtml(instrument, root, chordType: ChordType, htmFullPath, images):
    htm = copy(TEMPLATE)
    htm = htm.replace("${instrument}", instrument)
    htm = htm.replace("${chordroot}", root)
    htm = htm.replace("#_", "_sharp_")
    htm = htm.replace("${chordtype}", chordType.name)
    htmName = os.path.basename(htmFullPath.replace("#", "_sharp"))
    majorname = htmName.replace(chordType.name.replace(" ", "_"), "major")
    # Highlight the chord root and remove the hyperlink. Do that only once
    htm = htm.replace(f'<p><a href="./{majorname}">{root}</a></p>',
                      f'<p class="highlight">{root}</p>', 1)

    # Highlight the currently selected chord type and remove self-hyperlink in the htm file
    htm = htm.replace(f'<p><a href="./{htmName}">{root}{chordType.annotations[-1]}</a></p>',
                      f'<p class="highlight">{root}{chordType.annotations[-1]}</p>')

    # Build the list of images:
    imgnodes = []
    for img in images:
        imgnodes.append('<img src="{}" alt="Diagram not found"/>'.format(img))
        logging.debug("Adding image:                    {}".format(img))
        logging.debug("Adding <img/> with src={}".format(imgnodes[-1].strip()))
    htm = htm.replace("${images}", "\n        ".join(imgnodes))

    with open(htmFullPath.replace("#", "_sharp"), 'w') as h:
        h.write(htm)
    logging.info("Wrote file   {}".format(os.path.abspath(htmFullPath.replace("#", "_sharp"))))


def paintFretboard(instrument, root, chordType, imgName):
    if isinstance(instrument, Ukulele):
        size = QSize(160, 920)
    else:
        size = QSize(200, 920)
    painter = FretboardPainter(size, instrument)
    painter.setChordNotes(getChordNotes(root, chordType))
    painter.draw()
    painter.p.end()
    px = painter.pixmap
    filename = "{}_{}_{}.png".format(imgName, root.replace("#", "_sharp"), chordType.name.replace(" ", "_"))
    px.save(filename)
    logging.info("Saved image: {}".format(os.path.abspath(filename)))
    return filename


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Using a QApplication appears to mitigate the crash that would otherwise occur upon constructing a QPixmap.
    #

    main()
