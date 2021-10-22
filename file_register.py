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

    def __init__(self, suffix_index=1):
        self.files = {}
        self.suffix = suffix_index

    def getUniqueName(self, filename):
        """
        Returns name that does not collide with ones already created in the process
        """

        fileName = os.path.abspath(filename)
        dir, fname = os.path.split(fileName)

        if os.extsep in fname:
            lfileName = fileName.rsplit(os.extsep, 1)
            fname = lfileName[0]
            ext = os.extsep + lfileName[1]
        else:
            ext = ""

        num_suffix = self.suffix - 1
        file = fname + ext
        while self.isRegistered(file):
            num_suffix += 1
            file = fname + "_" + str(num_suffix) + ext

        return file

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
        return file in self.files
