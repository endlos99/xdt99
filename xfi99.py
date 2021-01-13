#!/usr/bin/env python

# xfi99: A file identification tool for TI-related files
#
# Copyright (c) 2015 Ralph Benzinger <xdt99@endlos.net>
#
# This program is part of the TI 99 Cross-Development Tools (xdt99).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import sys

VERSION = "0.0.x"


### Utility functions

def ordw(word):
    """word ord"""
    return ord(word[0]) << 8 | ord(word[1])


def ordwR(word):
    """reverse word ord"""
    return ord(word[1]) << 8 | ord(word[0])


def used(n, m):
    """integer division rounding up"""
    return (n + m - 1) / m


def isHex(data):
    """check if hexadecimal number"""
    return all([c in "0123456789ABCDEF" for c in data])


def isText(data):
    """check if ASCII text"""
    return all([c in "\r\n" or 32 <= ord(c) <= 127 for c in data])


### File identification functions

def isDiskImage(data):
    totals = ordw(data[0x0a:0x0c])
    if (data[0x0d:0x10] == "DSK") and (
            1 <= totals <= 1600) and (
            len(data) == totals * 256):
        useds = sum([bin(ord(data[0x38 + i])).count("1")
                     for i in xrange(used(totals, 8))])
        return "%d sectors, %d used" % (totals, useds)


def isTifilesImage(data):
    return data[:0x08] == "\x07TIFILES"


def isAssemblyObjectCode(data):
    if data[0] == "0" and (
            isHex(data[1:5]) and int(data[1:5], 16) < len(data)) and (
            data[76:80] == "0001" and isText(data)):
        return "Uncompressed\nProgram name: %-s" % data[6:14]
    elif data[0] == "\x01" and (
            data[76:80] == "0001" and ordw(data[2:4]) < len(data)):
        return "Compressed\nProgram name: %-s" % data[6:14]


def isAssemblyMemoryImage(data):
    if (data[:2] == "\xff\xff" or data[:2] == "\x00\x00") and (
            ordw(data[2:4]) == len(data)):
        return "Load address: >%04X%s" % (
            ordw(data[4:6]),
            ", has additional chunks" if data[0] == "\xff" else "")


def isGplByteCode(data):
    if data[:6] == "\xaa\x01\x00\x00\x00\x00":
        offset = ordw(data[6:8]) + 4
        len = ord(data[offset])
        return "Program name: %s\nGROM address: >%04X" % (
            data[offset + 1:offset + 1 + len],
            0)



### File identification

class FileError(Exception):
    pass


class File:
    """sector-based TI disk image file"""

    identifiers = [
        ("TI disk image (sector-based)", isDiskImage),
        ("TIFILES file container", isTifilesImage),
        ("Assembly object code (E/A3)", isAssemblyObjectCode),
        ("Assembly memory image (E/A5)", isAssemblyMemoryImage),
        ("GPL byte code", isGplByteCode),
        ("Text", isText)
        ]

    def __init__(self, filename):
        with open(filename, "rb") as fin:
            self.header = fin.read(1024 * 1024)

    @staticmethod
    def list_():
        return "".join([t + "\n" for t, _ in File.identifiers])

    def identify(self):
        """determine file type"""
        for type_, idfunc in File.identifiers:
            try:
                res = idfunc(self.header)
                if res == True:
                    return type_
                elif res:
                    return type_ + "\n" + res
            except IndexError:
                pass
        return "Unknown data"


### Main wrapper

def main():
    import os
    import argparse
    import glob

    class GlobStore(argparse.Action):
        """argparse globbing for Windows platforms"""

        def __call__(self, parser, namespace, values, option_string=None):
            if os.name == "nt":
                names = [glob.glob(fn) if "*" in fn or "?" in fn else [fn]
                         for fn in values]
                values = [f for n in names for f in n]
            setattr(namespace, self.dest, values)

    args = argparse.ArgumentParser(
        version=VERSION,
        description="xfi99: File identification tool")
    args.add_argument(
        "filename", nargs="*", type=str,
        help="file to identify")
    # general options
    args.add_argument(
        "-l", "--list", action="store_true", dest="list_",
        help="list known file types")
    opts = args.parse_args()

    # process files
    rc = 0
    if opts.list_:
        sys.stdout.write(File.list_())
    else:
        for fn in opts.filename:
            try:
                f = File(fn)
                sys.stdout.write(os.path.basename(fn) + ": " + f.identify())
            except (IOError, FileError) as e:
                rc = 1
                sys.stderr.write("Error: " + str(e))

    # return status
    return rc

if __name__ == "__main__":
    status = main()
    sys.exit(status)
