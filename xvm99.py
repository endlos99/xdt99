#!/usr/bin/env python3

# xvm99: A volume manager for nanoPEB/CF7A flash cards
#
# Copyright (c) 2015-2023 Ralph Benzinger <xdt99@endlos.net>
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
import os.path
import re
import argparse
import xdm99 as xdm
from xcommon import Util, CommandProcessor, RContainer, Warnings, Console


VERSION = '3.5.2'

CONFIG = 'XVM99_CONFIG'


# Multi-disk volumes

class Volumes:
    """nanoPEB/CF7A disk image volumes"""

    SECTORS_PER_VOLUME = 1600
    BYTES_PER_DISK = SECTORS_PER_VOLUME * xdm.Disk.BYTES_PER_SECTOR
    BYTES_PER_VOLUME = 2 * BYTES_PER_DISK

    def __init__(self, device):
        self.device = device

    def get_volume(self, vol_no, keepsize=False):
        """get disk image from volume device"""
        with open(self.device, 'rb') as f:
            f.seek((vol_no - 1) * self.BYTES_PER_VOLUME)
            data = f.read(self.BYTES_PER_VOLUME)
        image = data[::2]  # only every second byte is used
        return xdm.Disk.trim_sectors(image) if keepsize else image

    def write_volume(self, vol_no, image, keepsize=False, console=None):
        """write disk image to volume device"""
        size = len(image) * 2
        if size > self.BYTES_PER_VOLUME:
            raise ValueError('Disk image too large')
        if not keepsize:
            # use CF disk geometry and maximum sector count
            disk = xdm.Disk(image, console)
            disk.set_geometry(cf=True)
            disk.resize_disk(Volumes.SECTORS_PER_VOLUME)
            image = disk.get_image()
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

    @staticmethod
    def parse_volume_range(vol_range):
        volumes = []
        for vr in vol_range.split(','):
            m = re.match(r'(\d+)(?:-(\d+))?$', vr)
            if m is None:
                raise xdm.ContainerError('Invalid volumes: ' + vr)
            try:
                start = int(m.group(1))
                end = start if m.group(2) is None else int(m.group(2))
            except (ValueError, TypeError):
                raise xdm.ContainerError('Invalid volumes: ' + vr)
            volumes.extend(range(start, end + 1))
        return volumes


# Command line processing

class RVolume:
    """output container wrapper for xvm99"""

    def __init__(self, volume, container):
        self.volume = volume
        self.container = container

    def iscontainer(self):
        return self.container.iscontainer


class Xvm99Console(Console):
    """collects errors and warnings"""

    def __init__(self, colors=None):
        super().__init__('xvm99', None, colors=colors)

    def error(self, message):
        """record error message"""
        super().error(None, 'Error: ' + message)


class Xvm99Processor(CommandProcessor):

    def __init__(self):
        super().__init__((xdm.ContainerError, xdm.FileError))
        self.device = None
        self.xdm_opts = None
        self.xdm_console = None
        self.default_opts = None
        self.volumes = []

    def parse(self):
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
            self.default_opts = os.environ[CONFIG].split()
        except KeyError:
            self.default_opts = []
        self.opts, self.xdm_opts = args.parse_known_args(self.default_opts + sys.argv[1:])
        
    def run(self):
        self.console = Xvm99Console(colors=self.opts.color)
        self.xdm_console = xdm.Xdm99Console(Warnings(setall=True), colors=self.opts.color)
        self.device = Volumes(self.opts.device)
        self.volumes = Volumes.parse_volume_range(self.opts.volumes)

    def prepare(self):
        if self.opts.writevol:
            self.write()
        elif self.opts.readvol:
            self.read()
        elif not self.opts.init and not self.xdm_opts:
            self.info()
        else:
            self.delegate()

    def write(self):
        data = Util.readdata(self.opts.writevol)
        for volume in self.volumes:
            self.device.write_volume(volume, data, keepsize=self.opts.keepsize, console=self.xdm_console)

    def read(self):
        for volume in self.volumes:
            image = self.device.get_volume(volume, not self.opts.keepsize)
            suffix = '_' + str(volume) if len(self.volumes) > 1 else ''
            self.result.append(RContainer(image, 'tmp', suffix=suffix, output=self.opts.readvol))  # 'tmp' overwritten

    def info(self):
        self.result.append(RContainer(self.device.get_info(self.volumes), '-', istext=True))

    def delegate(self):
        """delegate file operations to xdm99"""
        del (sys.argv[2])  # remove volume specifier from command line passed to xdm99
        xdm_processor = xdm.Xdm99Processor()  # single instance will accumulate results
        for volume in self.volumes:
            if self.opts.init:
                image = bytes(1)  # dummy disk image
            else:
                image = self.device.get_volume(volume, keepsize=self.opts.keepsize)
                if not xdm.Disk.is_formatted(image):
                    self.console.error(f'Volume {volume} not formatted')
                    self.rc = 1
                    continue
            results, _ = xdm_processor.main(image, self.default_opts)
            # repackage as RVolume to store volume number
            for result in results:
                if result.iscontainer:
                    self.result.append(RVolume(volume, result))
                else:
                    self.result.append(result)
        self.console.merge(xdm_processor.console)

    def output(self):
        try:
            # disks written to device already handled in write()
            for item in self.result:
                if isinstance(item, RVolume):
                    # for delegated volume changes
                    self.device.write_volume(item.volume, item.container.data, keepsize=True, console=self.console)
                else:
                    item.write(self.opts.output, self.opts.encoding)
        except IOError as e:
            sys.exit(self.console.colstr(str(e)))
        self.console.print()


if __name__ == '__main__':
    status = Xvm99Processor().main()
    sys.exit(status)
