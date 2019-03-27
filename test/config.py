import os.path


### Executables

#xasPy = ["../xas99.py"]
xasPy = ["python.exe", "..\\xas99.py"]

#xdaPy = ["../xda99.py"]
xdaPy = ["python.exe", "..\\xda99.py"]

#xgaPy = ["../xga99.py"]
xgaPy = ["python.exe", "..\\xga99.py"]

#xdgPy = ["../xdg99.py"]
xdgPy = ["python.exe", "..\\xdg99.py"]

#xdmPy = ["../xdm99.py"]
xdmPy = ["python.exe", "..\\xdm99.py"]

xhmPy = ["../xhm99.py"]
#xhmPy = ["python.exe", "..\\xhm99.py"]

xvmPy = ["../xvm99.py"]
#xvmPy = ["python.exe", "..\\xvm99.py"]

xbasPy = ["../xbas99.py"]
#xbasPy = ["python.exe", "..\\xbas99.py"]


### Paths

class Dirs:
    # disk images
    disks = "disk"
    # reference files
    refs = "files"
    # HFE images and files
    hfe = "hfe"
    # assembler sources
    sources = "asm"
    # GPL sources
    gplsources = "gpl"
    # BASIC sources
    basic = "basic"
    # scratch directory
    tmp = "tmp"


class Disks:
    # empty disks
    blank = os.path.join(Dirs.disks, "blankSSSD.dsk")
    blankDD = os.path.join(Dirs.disks, "blankDSDD.dsk")
    # records generated in Extended Basic
    recsdis = os.path.join(Dirs.disks, "recsdis.dsk")
    recsint = os.path.join(Dirs.disks, "recsint.dsk")
    frag = os.path.join(Dirs.disks, "frag.dsk")
    # generated test records to be read in Extended Basic
    recsgen = os.path.join(Dirs.disks, "recsgen.dsk")
    # assembler sources
    asmsrcs = os.path.join(Dirs.disks, "asmsrcs.dsk")
    # asm sources generated from disassembled random data
    asmdump1 = os.path.join(Dirs.disks, "asmdump1.dsk")
    asmdump2 = os.path.join(Dirs.disks, "asmdump2.dsk")
    asmdumpRand = os.path.join(Dirs.disks, "asmdumpr.dsk")
    # reference image files
    asmimgs = os.path.join(Dirs.disks, "asmimgs.dsk")
    tisssd = os.path.join(Dirs.disks, "tisssd.dsk")
    tidsdd = os.path.join(Dirs.disks, "tidsdd.dsk")
    tidssd80 = os.path.join(Dirs.disks, "tidssd80.hd")
    # GPL sources
    gplsrcs = os.path.join(Dirs.disks, "gplsrcs.dsk")
    # BASIC sources
    basic1 = os.path.join(Dirs.disks, "basic1.dsk")
    basic2 = os.path.join(Dirs.disks, "basic2.dsk")
    # disk images with errors
    bad = os.path.join(Dirs.disks, "bad1.dsk")
    # scratch disks
    work = os.path.join(Dirs.tmp, "work.dsk")
    tifiles = os.path.join(Dirs.tmp, "tifiles.dsk")
    # HFE work disk
    hfe = os.path.join(Dirs.hfe, "hfedisk_dsk.hfe.gz")
    # simulated CF volume
    volumes = os.path.join(Dirs.tmp, "volumes.dev")


class Files:
    # various filenames
    input = os.path.join(Dirs.tmp, "input")
    output = os.path.join(Dirs.tmp, "output")
    outputff = [
        os.path.join(Dirs.tmp, "output"),
        os.path.join(Dirs.tmp, "outpuu"),
        os.path.join(Dirs.tmp, "outpuv"),
        os.path.join(Dirs.tmp, "outpuw"),
        os.path.join(Dirs.tmp, "outpux")
        ]
    error = os.path.join(Dirs.tmp, "error")
    reference = os.path.join(Dirs.tmp, "ref")
    tifile = os.path.join(Dirs.tmp, "tifile")


class Masks:
    # mask extended header, dates, and unsed blocks in FIAD files
    TIFile = [(0x1b, 0x80)]
    v9t9 = [(0x14, 0x1000000)]
