#!/usr/bin/env python3

# xvm99: A volume manager for nanoPEB/CF7A flash cards
#
# Copyright (c) 2015-2022 Ralph Benzinger <xdt99@endlos.net>
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
import platform
import os.path
import re
import xdm99 as xdm


VERSION = '3.5.0'

CONFIG = 'XVM99_CONFIG'


# utility functions

class Util:

    @staticmethod
    def tiname(filename):
        return os.path.splitext(os.path.basename(filename))[0][:10].upper()

    @staticmethod
    def nint(s):
        """None-aware int"""
        return None if s is None else int(s)

    @staticmethod
    def readdata(name, mode='rb'):
        """read data from file or STDIN"""
        if name == '-':
            if 'b' in mode:
                return sys.stdin.buffer.read()
            else:
                return sys.stdin.read()
        else:
            with open(name, mode) as f:
                return f.read()

    @staticmethod
    def writedata(filename, data, encoding=None):
        """write data to file or STDOUT"""
        if encoding is None:
            if filename == '-':
                sys.stdout.buffer.write(data)
            else:
                with open(filename, 'wb') as f:
                    f.write(data)
        else:
            try:
                if filename == '-':
                    sys.stdout.write(data.decode(encoding))
                else:
                    with open(filename, 'w') as f:
                        f.write(data.decode(encoding))
            except UnicodeDecodeError:
                sys.exit('Bad encoding: ' + encoding)


# Multi-disk volumes

class Volumes:
    """nanoPEB/CF7A disk image volumes"""

    SECTORS_PER_VOLUME = 1600
    BYTES_PER_DISK = SECTORS_PER_VOLUME * xdm.Disk.BYTES_PER_SECTOR
    BYTES_PER_VOLUME = 2 * BYTES_PER_DISK

    def __init__(self, device):
        self.device = device

    def get_volume(self, vol_no, trim=False):
        """get disk image from volume device"""
        with open(self.device, 'rb') as f:
            f.seek((vol_no - 1) * self.BYTES_PER_VOLUME)
            data = f.read(self.BYTES_PER_VOLUME)
        image = data[::2]  # only every second byte is used
        return xdm.Disk.trim_sectors(image) if trim else image

    def write_volume(self, vol_no, image, resize=None):
        """write disk image to volume device"""
        size = len(image) * 2
        if size > self.BYTES_PER_VOLUME:
            raise ValueError('Disk image too large')
        if resize:
            image = xdm.Disk.extend_sectors(image, resize)
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
                    sector_0 = d.read(xdm.Disk.BYTES_PER_SECTOR * 2 if extended else 0x10 * 2)
                    if sector_0[0x0d * 2:0x10 * 2:2] == b'DSK':
                        try:
                            name = sector_0[:0x0a * 2:2].decode()
                        except UnicodeDecodeError:
                            name = ''.join(chr(b) if 0x20 <= b < 0x7f else '.' for b in sector_0[:0x0a * 2:2])
                        if extended:
                            total = (sector_0[0x0a * 2] << 8) | sector_0[0x0b * 2]
                            used = 0
                            for j in range(xdm.Util.used(total, 8)):
                                used += bin(sector_0[(0x38 + j) * 2]).count('1')
                            info.append(f'[{volume:4d}]  {name:10s}:  {used:4d} used  {total-used:4d} free\n')
                        else:
                            info.append(f'[{volume:4d}]  {name:10s}')
                    else:
                        info.append(f'[{volume:4d}]  (not a valid disk image)\n')
                except IndexError:
                    info.append(f'[{volume:4d}]  (invalid volume)\n')
        return ''.join(info)


class Console:
    """collects errors and warnings"""

    def __init__(self, colors=None):
        if colors is None:
            self.colors = platform.system() in ('Linux', 'Darwin')  # no auto color on Windows
        else:
            self.colors = colors == 'on'

    def error(self, message):
        """record error message"""
        sys.stderr.write(self.color(message, severity=2) + '\n')

    def color(self, message, severity=0):
        if not self.colors:
            return message
        elif severity == 1:
            return '\x1b[33m' + message + '\x1b[0m'  # yellow
        elif severity == 2:
            return '\x1b[31m' + message + '\x1b[0m'  # red
        else:
            return message


# Command line processing

class Processor:
    """execute supplied commands"""

    def __init__(self, console):
        self.console = console

    def process_command(self, opts, env_opts, device, no_extra_opts=False):
        """device manipulation"""
        result = []
        volumes = []

        # get volume range
        for vol_range in opts.volumes.split(','):
            m = re.match(r'(\d+)(?:-(\d+))?$', vol_range)
            if m is None:
                self.console.error('Invalid volume range: ' + opts.volumes)
                return 1, ()
            start = Util.nint(m.group(1))
            end = Util.nint(m.group(2))
            volumes.extend([*range(start or 0, (end or start) + 1)])

        # volume operations
        if opts.writevol:
            data = Util.readdata(opts.writevol)
            resize = None if opts.keepsize else Volumes.SECTORS_PER_VOLUME
            for volume in volumes:
                device.write_volume(volume, data, resize)
            return 0, ()
        elif opts.readvol:
            for volume in volumes:
                image = device.get_volume(volume, not opts.keepsize)
                suffix = '_' + str(volume) if len(volumes) > 1 else ''
                Util.writedata(opts.readvol + suffix, image)
            return 0, ()
        elif not opts.init and no_extra_opts:
            sys.stdout.write(device.get_info(volumes))
            return 0, ()

        # file operations, delegate to xdm99, but remove volume spec so that xdm99 can parse command line
        del (sys.argv[2])
        for volume in volumes:
            if opts.init:
                image = bytes(1)
            else:
                image = device.get_volume(volume, not opts.keepsize)
                if not xdm.Disk.is_formatted(image):
                    return 1, ()
            vol_result = xdm.main(image, env_opts)
            for data, name, is_container in vol_result:
                if is_container:
                    result.append((data, volume, True))
                else:
                    result.append((data, name, False))
        return 0, result


# Command line processing

def main():
    import argparse

    args = argparse.ArgumentParser(
        description='xvm99: nanoPEB/CF7+ disk volume manipulation tool, v' + VERSION,
        epilog='Additionally, most xdm99 options can be used.')
    args.add_argument('device', type=str,
                      help='nanoPEB/CF7A flash cart device')
    args.add_argument('volumes', type=str,
                      help='volume number or range, volume numbers starting with 1')
    cmd = args.add_mutually_exclusive_group()

    # volume management
    cmd.add_argument('-r', '--read-volume', dest='readvol', metavar='<output file>',
                     help='read volume')
    cmd.add_argument('-w', '--write-volume', dest='writevol', metavar='<disk image>',
                     help='write volume')

    # general options
    args.add_argument('-X', '--initialize', dest='init', metavar='<size>',
                      help='initialize volume (CF or sector count or disk geometry xSxDxT)')
    args.add_argument('--keep-size', action='store_true', dest='keepsize',
                      help="don't resize image when writing to volume")
    args.add_argument('-c', '--encoding', dest='encoding', nargs='?', const='utf-8', metavar='<encoding>',
                      help='set encoding for DISPLAY files')
    args.add_argument('--color', action='store', dest='color', choices=['off', 'on'],
                      help='enable or disable color output')
    args.add_argument('-o', '--output', dest='output', metavar='<file>',
                      help='set output file name')

    try:
        default_opts = os.environ[CONFIG].split()
    except KeyError:
        default_opts = []
    opts, xdm_opts = args.parse_known_args(default_opts + sys.argv[1:])

    # setup
    device = Volumes(opts.device)
    console = Console(colors=opts.color)
    processor = Processor(console)

    # process device
    try:
        rc, result = processor.process_command(opts, default_opts, device, no_extra_opts=not xdm_opts)
    except (IOError, xdm.ContainerError, xdm.FileError) as e:
        console.error('Error: ' + str(e))
        sys.exit(1)

    # write result
    try:
        # only one of container, disk is provided
        for data, name_or_volume, is_volume in result:
            if is_volume:
                device.write_volume(name_or_volume, data)
            else:
                outname = opts.output or name_or_volume
                Util.writedata(outname, data, encoding=opts.encoding)
    except IOError as e:
        console.error('Error: ' + str(e))
        sys.exit(1)

    # return status
    return rc


if __name__ == '__main__':
    status = main()
    sys.exit(status)
