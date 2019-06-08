#!/usr/bin/env python

import random
import os
import shutil

from config import Dirs, Disks
from utils import xdm, chrw


### Setup

imageSize = 0x4000
imagesPerDisk = (90 * 4 * 1024) / (imageSize + 256)  # DS/DD


### Utility functions

def writeImage(disk, data, name):
    """write raw data as image file to disk"""
    image = chrw(0) + chrw(imageSize) + chrw(0xA000) + data + (
        chrw(0x1000) * ((imageSize - len(data) - 6) / 2))
    path = os.path.join(Dirs.sources, name + ".img")
    with open(path, "wb") as f:
        f.write(image)
    xdm(disk, "-a", path, "-n", name)


### Main generators

def generate():
    """generate disk images with pseudo memory images for disassembly"""
    genExhaustiveImages()
    genRandomImages()


def genRandomImages():
    """generate random data"""
    shutil.copyfile(Disks.blankDD, Disks.asmdumpRand)
    for i in xrange(imagesPerDisk):
        data = "".join(
            [chr(random.randint(0, 255)) for _ in xrange(imageSize - 6)])
        name = "IMGRAND%02d" % i
        writeImage(Disks.asmdumpRand, data, name)


def genExhaustiveImages():
    """generate all 65536 instruction words + 2x NOP for args/resync"""
    shutil.copyfile(Disks.blankDD, Disks.asmdump1)
    shutil.copyfile(Disks.blankDD, Disks.asmdump2)
    wordsPerImage = (imageSize - 6) / 6
    for i, a in enumerate(xrange(0, 0x10000, wordsPerImage)):
        disk = Disks.asmdump1 if i < imagesPerDisk else Disks.asmdump2
        data = (chrw(0x1000) + chrw(0x1000)).join(
            [chrw(w) for w in xrange(a, min(a + wordsPerImage, 0x10000))])
        name = "IMG%06X" % a
        writeImage(disk, data, name)


if __name__ == "__main__":
    generate()
