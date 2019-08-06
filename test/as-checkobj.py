#!/usr/bin/env python

import os

from config import Dirs, Disks, Files
from utils import (xas, xdm, check_files_eq, check_obj_code_eq,
                   check_image_files_eq, read_stderr, get_source_markers,
                   check_errors)


### Main test

def runtest():
    """check cross-generated output against native reference files"""

    # object code
    for inp_file, opts, ref_file, compr_file in [
            ("asdirs.asm", [], "ASDIRS-O", "ASDIRS-C"),
            ("asorgs.asm", [], "ASORGS-O", "ASORGS-C"),
            ("asopcs.asm", [], "ASOPCS-O", "ASOPCS-C"),
            ("asexprs.asm", [], "ASEXPRS-O", "ASEXPRS-C"),
            ("asbss.asm", [], "ASBSS-O", "ASBSS-C"),
            ("asregs.asm", ["-R"], "ASREGS-O", "ASREGS-C"),
            ("ashello.asm", ["-R"], "ASHELLO-O", "ASHELLO-C"),
            ("ascopy.asm", [], "ASCOPY-O", None),
            ("ascopyn.asm", [], "ASCOPYN-O", None),
            ("assize1.asm", [], "ASSIZE1-O", "ASSIZE1-C"),
            ("assize2.asm", [], "ASSIZE2-O", None),
            ("assize3.asm", [], "ASSIZE3-O", None),
            ("assize4.asm", [], "ASSIZE4-O", None),
            ("astisym.asm", [], "ASTISYM-O", "ASTISYM-C"),
            ("asimg1.asm", [], "ASIMG1-O", "ASIMG1-C"),
            ("asimg2.asm", [], "ASIMG2-O", None),
            ("asimg3.asm", [], "ASIMG3-OX", None),
            #("asreloc.asm", [], "ASRELOC-O", None),
            ("asxorg.asm", [], "ASXORG-O", None),
            ("ascart.asm", ["-R"], "ASCART-O", "ASCART-C")
            ]:
        source = os.path.join(Dirs.sources, inp_file)
        xdm(Disks.asmsrcs, "-e", ref_file, "-o", Files.reference)
        xas(*[source] + opts + ["-o", Files.output])
        check_obj_code_eq(Files.output, Files.reference)
        xas(*[source] + opts + ["--strict", "-o", Files.output])
        check_obj_code_eq(Files.output, Files.reference)
        if compr_file:
            # compressed object code
            xas(*[source] + opts + ["-C", "-o", Files.output])
            xdm(Disks.asmsrcs, "-e", compr_file, "-o", Files.reference)
            check_obj_code_eq(Files.output, Files.reference)

    # image files
    for inp_file, opts, ref_file in [
            ("ashello.asm", ["-R"], "ASHELLO-I"),
            ("astisym.asm", [], "ASTISYM-I"),
          ##  ("asimg1.asm", [], "ASIMG1-I"),  #TODO: junk in padding?
            ("asimg2.asm", [], "ASIMG2-I")
            #("asimg3.asm", [], "ASIMG3-I")
            ]:
        source = os.path.join(Dirs.sources, inp_file)
        xas(*[source] + opts + ["-i", "-o", Files.output])
        xdm(Disks.asmsrcs, "-e", ref_file, "-o", Files.reference)
        check_image_files_eq(Files.output, Files.reference)

    for inp_file, reffiles in [
            ("aslimg.asm", ["ASLIMG-I", "ASLIMG-J", "ASLIMG-K"]),
            ("assimg.asm", ["ASSIMG-I", "ASSIMG-J", "ASSIMG-K", "ASSIMG-L"]),
            ("asreloc.asm", ["ASRELOC-I"])
            ]:
        source = os.path.join(Dirs.sources, inp_file)
        xas(source, "-R", "-i", "-w", "-o", Files.output)
        for i, ref_file in enumerate(reffiles):
            xdm(Disks.asmimgs, "-e", ref_file, "-o", Files.reference)
            check_files_eq("Image file",
                           Files.outputff[i], Files.reference, fmt="P")

    # JMP instruction
    source = os.path.join(Dirs.sources, "asjmp.asm")
    with open(Files.error, "w") as ferr:
        xas(source, "-o", Files.output, stderr=ferr, rc=1)
    xaserrors = read_stderr(Files.error)
    referrors = get_source_markers(source, r";ERROR(:....)?")
    check_errors(referrors, xaserrors)

    # cleanup
    for i in range(4):
        os.remove(Files.outputff[i])
    os.remove(Files.reference)


if __name__ == "__main__":
    runtest()
    print("OK")
