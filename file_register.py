# -*- coding: utf-8 -*-
"""
Created on 22.10.2021 20:35 10
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['FileRegister']
__date__ = '2021-10-22'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import hashlib
import os


class FileRegister(object):
    """
    Class that keeps information on just created files, including their filenames and hashes

    This class is used to recognize files that have just been created in the process
    (i.e. haven't been there before the process started)

    This allows overwriting older versions of files repeatedly created by the process, but choosing unique names
    for files created in the process
    """
    md5 = hashlib.md5()

    def __init__(self):
        self.files = {}

    def hash(self, file):
        with open(file, 'rb') as f:
            data = f.read()
            FileRegister.md5.update(data)
        return FileRegister.md5.hexdigest()

    def register(self, file):
        self.files[file] = self.hash(file)

    def isRegistered(self, file):
        if not os.path.isfile(file):
            return False
        if file not in self.files:
            return False
        return self.hash(file) == self.files[file]
