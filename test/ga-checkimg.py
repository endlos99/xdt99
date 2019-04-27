#!/usr/bin/env python

# How to update the gplsrcs.dsk_id:
# - replace source file DIS/VAR 80 (no ext)
# - start ti99 gpl gplsrcs.dsk_id
# - enter source name, then -O, then -L, options G3
# - start DSK2.LINK
# - enter -O, -P, options G3


import os

from config import Dirs, Disks, Files
from utils import xga, xdm, error, check_files_eq, check_gbc_files_eq


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    # object code
    for infile, opts, reffile in [
            ("gaops.gpl", [], "GAOPS-Q"),
            ("gainst.gpl", [], "GAINST-Q"),
            ("gabranch.gpl", [], "GABRANCH-Q", ),
            ("gamove.gpl", [], "GAMOVE-Q"),
            ("gafmt.gpl", ["-s", "rag"], "GAFMT-Q"),
            ("gadirs.gpl", [], "GADIRS-Q"),
            ("gacopy.gpl", [], "GACOPY-Q"),
            ("gaexts.gpl", [], "GAEXTS-Q"),
            ("gapass.gpl", [], "GAPASS-Q")
            ]:
        source = os.path.join(Dirs.gplsources, infile)
        xdm(Disks.gplsrcs, "-e", reffile, "-o", Files.reference)
        xga(*[source] + opts + ["-o", Files.output])
        check_gbc_files_eq(infile, Files.output, Files.reference)

    # cart generation
    for name in ["gacart", "gahello"]:
        source = os.path.join(Dirs.gplsources, name + ".gpl")
        ref = os.path.join(Dirs.refs, name + ".rpk")
        xga(source, "-c", "-o", Files.output)
        check_files_eq("GPL cart", Files.output, ref, "P",
                     mask=((0x8, 0x1e), (0x188, 0xfff)))

    # error messages
    for s in ["gaerrs0.gpl", "gaerrs1.gpl"]:
        source = os.path.join(Dirs.gplsources, s)
        with open(source, "r") as fin:
            expect = [lino + 1 for lino, line in enumerate(fin) if "* ERROR" in line]
        with open(Files.error, "w") as ferr:
            xga(source, "-o", Files.output, stderr=ferr, rc=1)
        with open(Files.error, "r") as fin:
            try:
                found = [int(line[:4]) for line in fin if line[0] != "*"]
            except ValueError:
                error("Error messages", "Unexpected error message")
        if found != expect:
            error("Error messages",
                  "Error mismatch, extra: " + str([x for x in found if x not in expect]) +
                  " missing: " + str([x for x in expect if x not in found]))

    # cleanup
    os.remove(Files.output)
    os.remove(Files.reference)
    os.remove(Files.error)


if __name__ == "__main__":
    runtest()
    print "OK"
