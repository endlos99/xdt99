import os.path


### Executables

xasPy = ["../xas99.py"]
#xasPy = ["c:\\bin\\python2\\python.exe", "..\\xas99.py"]

xdmPy = ["../xdm99.py"]
#xdmPy = ["c:\\bin\\python2\\python.exe", "..\\xdm99.py"]

xvmPy = ["../xvm99.py"]
#xvmPy = ["c:\\bin\\python2\\python.exe", "..\\xvm99.py"]


### Paths

class Dirs:
    # disk images
    disks = "disk"
    # reference files
    refs = "ref"
    # assembler sources
    sources = "asm"
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
    # disk images with errors
    bad = os.path.join(Dirs.disks, "bad1.dsk")
    # scratch disks
    work = os.path.join(Dirs.tmp, "work.dsk")
    tifiles = os.path.join(Dirs.tmp, "tifiles.dsk")
    # simulated CF volume
    volumes = os.path.join(Dirs.tmp, "volumes.dev")


class Files:
    # various filenames
    input = os.path.join(Dirs.tmp, "input")
    output = os.path.join(Dirs.tmp, "output")
    error = os.path.join(Dirs.tmp, "error")
    reference = os.path.join(Dirs.tmp, "ref")
    tifile = os.path.join(Dirs.tmp, "tifile")


class Masks:
    # mask extended header, dates, and unsed blocks in TIFile files
    TIFile = [(0x1b, 0x80)]
