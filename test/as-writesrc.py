#!/usr/bin/env python

import os
import shutil

from config import Dirs, Disks
from utils import xdm


def writesrc():
    # create disk
    if not os.path.isfile(Disks.asmsrcs):
        shutil.copyfile(Disks.blankDD, Disks.asmsrcs)
    # create source files
    for name in [
            "ASHELLO", "ASDIRS", "ASBSS", "ASORGS", "ASOPCS", "ASEXPRS",
            "ASREGS", "ASSIZE1", "ASSIZE2", "ASSIZE3", "ASSIZE4",
            "ASCOPY", "ASCOPY1", "ASCOPY2", "ASCOPY3", "ASCOPY4",
            "ASCOPYN-TI", "ASIMG1", "ASIMG2", "ASIMG3", "ASTISYM",
            "ASCART", "ASXEXT", "ASXEXT0-TI", "ASXEXT1-TI", "ASXEXT2-TI",
            "ASERRS"
            ]:
        source = os.path.join(Dirs.sources, name.lower() + ".asm")
        xdm(Disks.asmsrcs, "-a", source, "-n", name, "-f", "DIS/VAR80")


if __name__ == "__main__":
    writesrc()
