#!/usr/bin/env python

# How to update the gplsrcs.dsk_id:
# - replace source file DIS/VAR 80 (no ext)
# - start ti99 gpl gplsrcs.dsk_id
# - enter source name, then -O, then -L, options G3
# - start DSK2.LINK
# - enter -O, -P, options G3


import os

from config import Dirs, Disks, Files
from utils import xga, xdm, check_files_eq, check_gbc_files_eq


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    # object code
    for infile, opts, reffile in (
            ["gaops.gpl", [], "GAOPS-Q"],
            ["gainst.gpl", [], "GAINST-Q"],
            ["gabranch.gpl", [], "GABRANCH-Q", ],
            ["gamove.gpl", [], "GAMOVE-Q"],
            ["gafmt.gpl", [], "GAFMT-Q"],
            ["gadirs.gpl", [], "GADIRS-Q"],
            ["gacopy.gpl", [], "GACOPY-Q"],
            ["gaexts.gpl", [], "GAEXTS-Q"],
            ["gapass.gpl", [], "GAPASS-Q"]
            ):
        source = os.path.join(Dirs.gplsources, infile)
        xdm(Disks.gplsrcs, "-e", reffile, "-o", Files.reference)
        xga(*[source] + opts + ["-w", "-o", Files.output])
        check_gbc_files_eq(infile, Files.output, Files.reference)

    # cart generation
    for name in ["gacart", "gahello"]:
        source = os.path.join(Dirs.gplsources, name + ".gpl")
        ref = os.path.join(Dirs.refs, name + ".rpk")
        xga(source, "-c", "-o", Files.output)
        check_files_eq("GPL cart", Files.output, ref, "P", mask=((0x8, 0x1e), (0x188, 0xfff)))

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print("OK")
