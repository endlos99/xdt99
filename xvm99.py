#!/usr/bin/env python

# xvm99: A volume manager for nanoPEB/CF7A flash cards
#
# Copyright (c) 2015-2020 Ralph Benzinger <xdt99@endlos.net>
#
# This program is part of the TI 99 Cross-Development Tools (xdt99).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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


VERSION = '3.0.0'


# Multi-disk volumes

class Volumes:
    """nanoPEB/CF7A disk image volumes"""

    SECTORS_PER_VOLUME = 1600
    BYTES_PER_DISK = SECTORS_PER_VOLUME * xdm99.Disk.BYTES_PER_SECTOR
    BYTES_PER_VOLUME = 2 * BYTES_PER_DISK

    def __init__(self, device):
        self.device = device

    def get_volume(self, vol_no, trim=False):
        """get disk image from volume device"""
        with open(self.device, 'rb') as f:
            f.seek((vol_no - 1) * self.BYTES_PER_VOLUME)
            data = f.read(self.BYTES_PER_VOLUME)
        image = data[::2]  # only every second byte is used
        return xdm99.Disk.trim_sectors(image) if trim else image

    def write_volume(self, vol_no, image, resize=None):
        """write disk image to volume device"""
        size = len(image) * 2
        if size > self.BYTES_PER_VOLUME:
            raise ValueError('Disk image too large')
        if resize:
            image = xdm99.Disk.extend_sectors(image, resize)
        data = b''.join(bytes((b, 0)) for b in image) + bytes(self.BYTES_PER_VOLUME - size)
        with open(self.device, 'r+b') as d:
            d.seek((vol_no - 1) * self.BYTES_PER_VOLUME)
            d.write(data)

    def get_info(self, volumes, extended=True):
        """get short disk info for individual volumes"""
        info = []
        with open(self.device, 'rb') as d:
            if not volumes:
                # show all volumes
                d.seek(0, 2)  # go to end of device
                device_size = d.tell()
                volumes = list(range(1, (device_size + self.BYTES_PER_VOLUME - 1) // self.BYTES_PER_VOLUME + 1))
            for volume in volumes:
                try:
                    d.seek((volume - 1) * self.BYTES_PER_VOLUME)
                    sector_0 = d.read(xdm99.Disk.BYTES_PER_SECTOR * 2 if extended else 0x10 * 2)
                    if sector_0[0x0d * 2:0x10 * 2:2] == b'DSK':
                        try:
                            name = sector_0[:0x0a * 2:2].decode()
                        except UnicodeDecodeError:
                            name = ''.join(chr(b) if 0x20 <= b < 0x7f else '.' for b in sector_0[:0x0a * 2:2])
                        if extended:
                            total = (sector_0[0x0a * 2] << 8) | sector_0[0x0b * 2]
                            used = 0
                            for j in range(xdm99.used(total, 8)):
                                used += bin(sector_0[(0x38 + j) * 2]).count('1')
                            info.append(f'[{volume:4d}]  {name:10s}:  {used:4d} used  {total-used:4d} free\n')
                        else:
                            info.append(f'[{volume:4d}]  {name:10s}')
                    else:
                        info.append(f'[{volume:4d}]  (not a valid disk image)\n')
                except IndexError:
                    info.append(f'[{volume:4d}]  (invalid volume)\n')
        return ''.join(info)


# Command line processing

def main():
    import argparse
    import glob
    import os

    class GlobStore(argparse.Action):
        """argparse globbing for Windows platforms"""

        def __call__(self, parser, namespace, values, option_string=None):
            if os.name == 'nt':
                names = [glob.glob(name) if '*' in name or '?' in name else [name] for name in values]
                values = [name for globs in names for name in globs]
            setattr(namespace, self.dest, values)

    args = argparse.ArgumentParser(description='xvm99: nanoPEB/CF7+ disk volume manipulation tool, v' + VERSION)
    args.add_argument('device', type=str,
                      help='nanoPEB/CF7A flash cart device')
    args.add_argument('volumes', type=str, nargs='?',
                      help='volume number or range')
    cmd = args.add_mutually_exclusive_group()
    # volume management
    cmd.add_argument('-r', '--read-volume', dest='readvol', metavar='<output file>',
                     help='read volume')
    cmd.add_argument('-w', '--write-volume', dest='writevol', metavar='<disk image>',
                     help='write volume')
    args.add_argument('--keep-size', action='store_true', dest='keepsize',
                      help="don't resize image when writing to volume")
    # disk image commands for xdm
    cmd.add_argument('-i', '--info', action='store_true', dest='info',
                     help='show image information')
    cmd.add_argument('-p', '--print', dest='print_', nargs='+', metavar='<name>',
                     help='print file from image')
    cmd.add_argument('-e', '--extract', dest='extract', nargs='+', metavar='<name>',
                     help='extract files from image')
    args.add_argument('-t', '--tifile', action='store_true', dest='astif',
                      help='use TIFile file format for extracted files')
    cmd.add_argument('-a', '--add', action=GlobStore, dest='add', nargs='+',
                     metavar='<file>', help='add files to image or update existing files')
    args.add_argument('-f', '--format', dest='format', metavar='<format>',
                      help='set TI file format (D/V n, D/F n, I/V n, I/F n, PROGRAM) for data to add')
    args.add_argument('-n', '--name', dest='name', metavar='<name>',
                      help='set TI file name for data to add')
    cmd.add_argument('-d', '--delete', dest='delete', nargs='+', metavar='<name>',
                     help='delete files from image')
    cmd.add_argument('-c', '--check', action='store_true', dest='checkonly',
                     help='check disk image integrity only')
    cmd.add_argument('-R', '--repair', action='store_true', dest='repair',
                     help='attempt to repair disk image')
    # general options
    args.add_argument('-o', '--output', dest='output', metavar='<file>',
                      help='set output file name')
    args.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                      help='suppress all warnings')
    opts = args.parse_args()

    if (opts.readvol or opts.writevol or opts.info or opts.print_ or opts.add or opts.extract or opts.delete or
            opts.checkonly or opts.repair) and not opts.volumes:
        args.error('Missing volume number of range')

    # setup
    device = Volumes(opts.device)
    fmt = opts.format or 'PROGRAM'
    tiname = lambda x: (opts.name or os.path.splitext(os.path.basename(x))[0][:10].upper())

    # get range
    volumes = []
    if opts.volumes:
        parts = opts.volumes.split(',')
        try:
            for p in parts:
                range_start, range_end = re.match('(\d+)(?:-(\d+))?$', p).group(1, 2)
                volumes.extend(range(int(range_start), (int(range_end) if range_end else int(range_start)) + 1))
        except AttributeError:
            sys.exit('Invalid volume range: ' + opts.volumes)

    # process device
    rc = 0
    result = []
    try:
        # volume operations
        if opts.writevol:
            with open(opts.writevol, 'rb') as f:
                data = f.read()
            resize = None if opts.keepsize else Volumes.SECTORS_PER_VOLUME
            for volume in volumes:
                device.write_volume(volume, data, resize)
        elif opts.readvol:
            for volume in volumes:
                image = device.get_volume(volume, not opts.keepsize)
                suffix = '_' + str(volume) if len(volumes) > 1 else ''
                with open(opts.readvol + suffix, 'wb') as f:
                    f.write(image)
        # disk operations
        elif opts.info:
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                sys.stdout.write(f'[{volume:d}]' + disk.get_info())
                sys.stdout.write('-' * 76 + '\n')
                sys.stdout.write(disk.get_catalog())
        elif opts.print_:
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                files = disk.glob_files(opts.print_)
                contents = [disk.get_file(name).get_contents() for name in files]
                sys.stdout.write(''.join(contents))
        elif opts.extract:
            if opts.output and len(opts.extract) > 1:
                sys.exit('Error: Cannot use -o when extracting multiple files')
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                files = disk.glob_files(opts.extract)
                suffix = '_' + str(volume) if len(volumes) > 1 else ''
                if opts.astif:
                    result.extend((disk.get_tifiles_file(name), name.lower() + suffix + '.tfi', 'wb')
                                  for name in files)
                else:
                    result.extend((disk.get_file(name).get_contents(), name.lower() + suffix, 'wb')
                                  for name in files)
        elif opts.add:
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                count = 0
                for name in opts.add:
                    if name == '-':
                        name = 'STDIN'
                        data = sys.stdin.read()
                    else:
                        with open(name, 'rb') as fin:
                            data = fin.read()
                    if opts.astif:
                        disk.add_file(xdm99.File().from_tif_image(data))
                    else:
                        filename = xdm99.sseq(opts.name, count) if opts.name else tiname(name)
                        disk.add_file(xdm99.File().new(name=filename, format_=fmt, data=data))
                        count += 1
                device.write_volume(volume, disk.image)
        elif opts.delete:
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                files = disk.glob_files(opts.delete)
                for name in files:
                    disk.remove_file(name)
                device.write_volume(volume, disk.image)
        elif opts.checkonly:
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                if not opts.quiet:
                    sys.stderr.write(disk.get_warnings())
                if disk.warnings:
                    rc += 1
        elif opts.repair:
            for volume in volumes:
                image = device.get_volume(volume)
                disk = xdm99.Disk(image)
                disk.fix_disk()
                device.write_volume(volume, disk.image)
        # default volume info operation
        else:
            sys.stdout.write(device.get_info(volumes))
    except (IOError, xdm99.DiskError, xdm99.FileError) as e:
        sys.exit(f'Error: {e}')

    # write result
    for data, name, mode in result:
        outname = opts.output or name
        if outname == '-':
            sys.stdout.write(data)
        else:
            try:
                with open(outname, mode) as fout:
                    fout.write(data)
            except IOError as e:
                    sys.exit('Error: ' + str(e))

    # return status
    return rc


if __name__ == '__main__':
    status = main()
    sys.exit(status)
