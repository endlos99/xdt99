#!/usr/bin/env python

import random
import os
import shutil

from config import Dirs, Disks
from utils import xdm, chrw


# Setup

IMAGE_SIZE = 0x4000
IMAGES_PER_DISK = (90 * 4 * 1024) // (IMAGE_SIZE + 256)  # DS/DD


# Utility functions

def write_image(disk, data, name):
    """write raw data as image file to disk"""
    image = (bytes(1) + chrw(IMAGE_SIZE) + chrw(0xa000) + data +
             (chrw(0x1000) * ((IMAGE_SIZE - len(data) - 6) / 2)))
    path = os.path.join(Dirs.sources, name + '.img')
    with open(path, 'wb') as f:
        f.write(image)
    xdm(disk, '-a', path, '-n', name)


# Main generators

def generate():
    """generate disk images with pseudo memory images for disassembly"""
    generate_exhaustive_images()
    generate_random_images()


def generate_random_images():
    """generate random data"""
    shutil.copyfile(Disks.blankDD, Disks.asmdumpRand)
    for i in range(IMAGES_PER_DISK):
        data = ''.join(
            [chr(random.randint(0, 255)) for _ in range(IMAGE_SIZE - 6)])
        name = f'IMGRAND{i:02d}'
        write_image(Disks.asmdumpRand, data, name)


def generate_exhaustive_images():
    """generate all 65536 instruction words + 2x NOP for args/resync"""
    shutil.copyfile(Disks.blankDD, Disks.asmdump1)
    shutil.copyfile(Disks.blankDD, Disks.asmdump2)
    words_per_image = (IMAGE_SIZE - 6) / 6
    for i, a in enumerate(range(0, 0x10000, words_per_image)):
        disk = Disks.asmdump1 if i < IMAGES_PER_DISK else Disks.asmdump2
        data = (chrw(0x1000) + chrw(0x1000)).join(
            [chrw(w) for w in range(a, min(a + words_per_image, 0x10000))])
        write_image(disk, data, f'IMG{a:06X}')


if __name__ == '__main__':
    generate()
