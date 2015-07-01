#!/usr/bin/env python

# xvm99: A volume manager for nanoPEB/CF7A flash cards
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
import re
import xdm99

VERSION = "1.4.0"


### Multi-disk volumes

class Volumes:
    """nanoPEB/CF7A disk image volumes"""

    sectorsPerVolume = 1600
    bytesPerDisk = sectorsPerVolume * xdm99.Disk.bytesPerSector
    bytesPerVolume = 2 * bytesPerDisk

    def __init__(self, device):
        self.device = device
        # NOTE: cannot determine device size reliably in Windows
        #with open(device, "rb") as d:
        #    d.seek(0, SEEK_END)
        #    self.size = d.tell()
        #self.volumeCount = xdm99.used(self.size, self.bytesPerVolume)
        
    def getVolume(self, volno, trim=False):
        """get disk image from volume device"""
        with open(self.device, "rb") as f:
            f.seek((volno - 1) * self.bytesPerVolume)
            data = f.read(self.bytesPerVolume)
        image = data[::2]
        return xdm99.Disk.trimSectors(image) if trim else image

    def writeVolume(self, volno, image, resize=None):
        """write disk image to volume device"""
        size = len(image) * 2
        if size > self.bytesPerVolume:
            raise ValueError("Disk image too large")
        if resize:
            image = xdm99.Disk.extendSectors(image, resize)
        data = "\x00".join(image) + "\x00" * (self.bytesPerVolume - size + 1)
        with open(self.device, "r+b") as d:
            d.seek((volno - 1) * self.bytesPerVolume)
            d.write(data)

    def getInfo(self, volumes, extended=True):
        """get short disk info for individual volumes"""
        info = []
        with open(self.device, "rb") as d:
            for v in volumes:
                try:
                    d.seek((v - 1) * self.bytesPerVolume)
                    s0 = d.read(xdm99.Disk.bytesPerSector * 2 if extended else
                                0x10 * 2)
                    if (s0[0x0D * 2] == "D" and s0[0x0E * 2] == "S" and
                        s0[0x0F * 2] == "K"):
                        if extended:
                            total = ord(s0[0x0A * 2]) << 8 | ord(s0[0x0B * 2])
                            used = 0
                            for j in xrange(xdm99.used(total, 8)):
                                used += bin(ord(s0[(0x38 + j) * 2])).count("1")
                            info.append("[%4d]  %-10s:  %4d used  %4d free\n" % (
                                v, s0[:0x0A * 2:2], used, total - used))
                        else:
                            info.append("[%4d]  %-10s" % (v, s0[:0x0A * 2:2]))
                    else:
                        info.append("[%4d]  (not a valid disk image)\n" % v)
                except IndexError:
                    info.append("[%4d]  (invalid volume)\n" % v)
        return "".join(info)


### Command line processing

def main():
    import argparse
    import glob
    import os

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
        description="xvm99: nanoPEB/CF7A disk volume manipulation tool")
    args.add_argument(
        "device", type=str,
        help="nanoPEB/CF7A flash cart device")
    args.add_argument(
        "volumes", type=str,
        help="volume number or range")
    cmd = args.add_mutually_exclusive_group()
    # volume management
    cmd.add_argument(
        "-r", "--read-volume", dest="readvol", metavar="<output file>",
        help="read volume")
    cmd.add_argument(
        "-w", "--write-volume", dest="writevol", metavar="<disk image>",
        help="write volume")
    args.add_argument(
        "--keep-size", action="store_true", dest="keepsize",
        help="don't resize image when writing to volume")
    # disk image commands for xdm
    cmd.add_argument(
        "-i", "--info", action="store_true", dest="info",
        help="show image infomation")
    cmd.add_argument(
        "-p", "--print", dest="print_", nargs="+", metavar="<name>",
        help="print file from image")
    cmd.add_argument(
        "-e", "--extract", dest="extract", nargs="+", metavar="<name>",
        help="extract files from image")
    args.add_argument(
        "-t", "--tifile", action="store_true", dest="astif",
        help="use TIFile file format for extracted files")
    cmd.add_argument(
        "-a", "--add", action=GlobStore, dest="add", nargs="+",
        metavar="<file>", help="add files to image or update existing files")
    args.add_argument(
        "-f", "--format", dest="format", metavar="<format>",
        help="set TI file format (DIS/VARnnn, DIS/FIXnnn, INT/VARnnn, " + \
             "INT/FIXnnn, PROGRAM) for data to add")
    args.add_argument(
        "-n", "--name", dest="name", metavar="<name>",
        help="set TI file name for data to add")
    cmd.add_argument(
        "-d", "--delete", dest="delete", nargs="+", metavar="<name>",
        help="delete files from image")
    cmd.add_argument(
        "-c", "--check", action="store_true", dest="checkonly",
        help="check disk image integrity only")
    cmd.add_argument(
        "-R", "--repair", action="store_true", dest="repair",
        help="attempt to repair disk image")
    # general options
    args.add_argument(
        "-o", "--output", dest="output", metavar="<file>",
        help="set output file name")
    args.add_argument(
        "-q", "--quiet", action="store_true", dest="quiet",
        help="suppress all warnings")
    opts = args.parse_args()

    # setup
    device = Volumes(opts.device)
    fmt = opts.format or "PROGRAM"
    tiname = lambda x: (opts.name or
                        os.path.splitext(os.path.basename(x))[0][:10].upper())

    # get range
    volumes = []
    parts = opts.volumes.split(",")
    try:
        for p in parts:
            (r1, r2) = re.match("(\d+)(?:-(\d+))?$", p).group(1, 2)
            volumes.extend(range(int(r1),
                                 (int(r2) if r2 else int(r1)) + 1))
    except AttributeError:
        sys.exit("Invalid volume range: " + opts.volumes)

    # process device
    rc, result = 0, []
    try:
        # volume operations
        if opts.writevol:
            with open(opts.writevol, "rb") as f:
                data = f.read()
            resize = None if opts.keepsize else Volumes.sectorsPerVolume
            for v in volumes:
                device.writeVolume(v, data, resize)
        elif opts.readvol:
            for v in volumes:
                image = device.getVolume(v, not opts.keepsize)
                suffix = "_" + str(v) if len(volumes) > 1 else ""
                with open(opts.readvol + suffix, "wb") as f:
                    f.write(image)
        # disk operations
        elif opts.info:
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                sys.stdout.write("[" + str(v) + "]" + disk.getInfo())
                sys.stdout.write("-" * 76 + "\n")
                sys.stdout.write(disk.getCatalog())
        elif opts.print_:
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                files = disk.globFiles(opts.print_)
                contents = [disk.getFile(name).getContents()
                            for name in files]
                sys.stdout.write("".join(contents))
        elif opts.extract:
            if opts.output and len(opts.extract) > 1:
                sys.exit(
                    "Error: Cannot use -o when extracting multiple files")
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                files = disk.globFiles(opts.extract)
                suffix = "_" + str(v) if len(volumes) > 1 else ""
                if opts.astif:
                    result.extend([(disk.getTifilesFile(name),
                                    name.lower() + suffix + ".tfi", "wb")
                                   for name in files])
                else:
                    result.extend([(disk.getFile(name).getContents(),
                                    name.lower() + suffix,
                                    "w" if fmt[0] == "D" else "wb")
                                   for name in files])
        elif opts.add:
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                n, c = opts.name, 0
                for name in opts.add:
                    if name == "-":
                        name = "STDIN"
                        data = sys.stdin.read()
                    else:
                        with open(name, "r" if fmt[0] == "D" and
                                        not opts.astif else "rb") as fin:
                            data = fin.read()
                    if opts.astif:
                        disk.addFile(xdm99.File(tifimage=data))
                    else:
                        n = (xdm99.sseq(opts.name, c) if opts.name else
                             tiname(name))
                        disk.addFile(xdm99.File(name=n, fmt=fmt, data=data))
                        c += 1
                device.writeVolume(v, disk.getImage())
        elif opts.delete:
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                files = disk.globFiles(opts.delete)
                for name in files:
                    disk.removeFile(name)
                device.writeVolume(v, disk.getImage())
        elif opts.checkonly:
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                if not opts.quiet:
                    sys.stderr.write(disk.getWarnings())
                rc += 1 if disk.warnings else 0
        elif opts.repair:
            for v in volumes:
                image = device.getVolume(v)
                disk = xdm99.Disk(image)
                disk.fixDisk()
                device.writeVolume(v, disk.getImage())
        # default volume info operation
        else:
            sys.stdout.write(device.getInfo(volumes))
    except (IOError, xdm99.DiskError, xdm99.FileError) as e:
        sys.exit("Error: " + str(e))

    # write result
    for data, name, mode in result:
        outname = opts.output or name
        if outname == "-":
            sys.stdout.write(data)
        else:
            try:
                with open(outname, mode) as fout:
                    fout.write(data)
            except IOError as e:
                    sys.exit("Error: " + str(e))

    # return status
    return rc

if __name__ == "__main__":
    status = main()
    sys.exit(status)
