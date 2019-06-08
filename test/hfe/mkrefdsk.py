#!/usr/bin/env python

#  create reference pseudo-disks

from subprocess import call


def chrw(word):
    """word chr"""
    return chr(word >> 8) + chr(word & 0xFF)


def xdm(*args):
    call(["../../xdm99.py"] + list(args))


xdm("w.dsk_id", "-X", "SSSD")
with open("w.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rsssd.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                    for s in xrange(1, 360)])
    fout.write(header + side0)


xdm("w.dsk_id", "-X", "DSSD")
with open("w.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rdssd.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                     for s in xrange(1, 360)])
    side1 = "".join(["".join([chr(i) for i in xrange(255, 1, -1)]) + chrw(s)
                     for s in xrange(360, 720)])
    fout.write(header + side0 + side1)


xdm("w.dsk_id", "-X", "SSDD")
with open("w.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rssdd.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                     for s in xrange(1, 720)])
    fout.write(header + side0)


xdm("w.dsk_id", "-X", "DSDD")
with open("w.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rdsdd.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                     for s in xrange(1, 720)])
    side1 = "".join(["".join([chr(i) for i in xrange(255, 1, -1)]) + chrw(s)
                     for s in xrange(720, 1440)])
    fout.write(header + side0 + side1)


xdm("w.dsk_id", "-X", "SSSD80T")
with open("w.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rsssd80t.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                     for s in xrange(1, 720)])
    fout.write(header + side0)


xdm("w.dsk_id", "-X", "DSSD80T")
with open("w.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rdssd80t.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                     for s in xrange(1, 720)])
    side1 = "".join(["".join([chr(i) for i in xrange(255, 1, -1)]) + chrw(s)
                     for s in xrange(720, 1440)])
    fout.write(header + side0 + side1)


#xdm("w.dsk_id", "-X", "DSDD")
with open("tiit80t.dsk_id", "rb") as fin:
    header = fin.read(256)

with open("rdsdd80t.dsk_id", "wb") as fout:
    side0 = "".join(["".join([chr(i) for i in xrange(1, 255)]) + chrw(s)
                     for s in xrange(1, 1440)])
    side1 = "".join(["".join([chr(i) for i in xrange(255, 1, -1)]) + chrw(s)
                     for s in xrange(1440, 2880)])
    fout.write(header + side0 + side1)
