#!/usr/bin/env python

import sys
sys.path.append('..')  # what an ugly kludge, just to import xdm99 here ...

from xdm99 import Archive, BitStream
from config import Dirs, Disks, Files
from utils import xdm, error


# Check functions


# Main test

def runtest():
    """check handling of ARK archives"""
    
    # bitstreams
    bs = BitStream(b'\xab\xcd\xef', 3)
    bits = [b for b in bs]
    if bits != [5, 2, 7, 4, 6, 7, 5, 7]:
        error('bitstream', 'Bad bitstream bits (width 3)')

    bs = BitStream(b'\x12\x34\x56\x78\x90\xab\xcd\xef', 11)
    bits = [b for b in bs]
    if bits != [145, 1301, 1265, 266, 1510, 1980]:
        error('bitstream', 'Bad bitstream bits (width 11)')

    bs = BitStream(b'\x5a\x96\x0f', 1)
    bits = [b for b in bs]
    if bits != [0, 1, 0, 1,  1, 0, 1, 0,  1, 0, 0, 1,  0, 1, 1, 0,  0, 0, 0, 0,  1, 1, 1, 1]:
        error('bitstream', 'Bad bitstream bits (width 1)')

    # remove temporary files
    # os.remove(Files.output)
    # os.remove(Files.reference)


if __name__ == '__main__':
    runtest()
    print('OK')
