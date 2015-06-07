#!/usr/bin/env python

import os
import gzip

from config import Dirs, Files
from utils import xas, error


### Setup

prolog = """
         AORG >A000
SFIRST
SLOAD    
"""

epilog = """
SLAST    END
"""


### Utility functions

def processSource(source):
    lines = [processLine(line) for line in source]
    return prolog + "".join(lines) + epilog


def processLine(line):
    mnemonic = line[10:13] if line[13] == " " else line[10:14]
    if mnemonic in ["LST", "MPYS", "DIVS"]:
        data = [">" + v for v in line[58:].split()]
        return "L" + line[:4] + " DATA " + ",".join(data) + "\n"
    else:
        return "L" + line[:4] + "  " + line[5:]


### Check function

def checkImageFilesEq(name, origPath, imagePaths):
    with open(origPath, "rb") as f:
        orig = f.read()[6:]
    with open(imagePaths[0], "rb") as f1, open(imagePaths[1], "rb") as f2, \
         open(imagePaths[2], "rb") as f3:
        image = f1.read()[6:] + f2.read()[6:] + f3.read()[6:]
    if not len(orig) <= len(image) <= len(orig) + 4:
        error("Image dumps", "Incorrect image length: " + name)
    if orig != image[:len(orig)]:
        error("Image dumps", "Image mismatch: " + name)


### Main test

def runtest():
    """check cross-generated images files from disassembled data blobs"""

    # disassembled image files
    for n in [
            "IMGRAND00", "IMGRAND01", "IMGRAND02", "IMGRAND03",
            "IMGRAND04", "IMGRAND05", "IMGRAND06", "IMGRAND07",
            "IMGRAND08", "IMGRAND09", "IMGRAND10", "IMGRAND11",
            "IMGRAND12", "IMGRAND13", "IMGRAND14", "IMGRAND15",
            "IMGRAND16", "IMGRAND17", "IMGRAND18", "IMGRAND19",
            "IMGRAND20", "IMGRAND21",
            "IMG000000", "IMG000AA9", "IMG001552", "IMG001FFB",
            "IMG002AA4", "IMG00354D", "IMG003FF6", "IMG004A9F",
            "IMG005548", "IMG005FF1", "IMG006A9A", "IMG007543",
            "IMG007FEC", "IMG008A95", "IMG00953E", "IMG009FE7",
            "IMG00AA90", "IMG00B539", "IMG00BFE2", "IMG00CA8B",
            "IMG00D534", "IMG00DFDD", "IMG00EA86", "IMG00F52F",
            "IMG00FFD8"
            ]:
        archive = os.path.join(Dirs.sources, n + ".dis.gz")
        with gzip.open(archive, "rb") as fin, open(Files.input, "w") as fout:
            srccode = processSource(fin.readlines())
            fout.write(srccode)
        xas(Files.input, "-i", "-R", "-o", Files.output)
        checkImageFilesEq(n, os.path.join(Dirs.sources, n + ".img"),
                          Files.outputff)

    # cleanup
    os.remove(Files.input)
    os.remove(Files.output)
    for fn in Files.outputff:
        try:
            os.remove(fn)
        except:
            pass


if __name__ == "__main__":
    runtest()
    print "OK"
