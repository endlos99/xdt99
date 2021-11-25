#!/usr/bin/env python3

# xdm99: A disk manager for TI disk images
#
# Copyright (c) 2015-2021 Ralph Benzinger <xdt99@endlos.net>
#
# This program is part of the TI 99 Cross-Development Tools (xdt99).
#
# xdt99 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import re
import datetime
import os
import platform


VERSION = '3.2.0'

CONFIG = 'XDM99_CONFIG'


# Utility functions

class Util:

    @staticmethod
    def ordn(bytes_):
        """convert byte sequence into value"""
        value = 0
        for b in bytes_:
            value = (value << 8) + b
        return value

    @staticmethod
    def chrn(value, size=2):
        """convert value into byte sequence"""
        return bytes(((value >> ((i - 1) * 8)) & 0xff) for i in range(size, 0, -1))

    @staticmethod
    def ordwR(word):
        """reverse word ord"""
        return word[1] << 8 | word[0]

    @staticmethod
    def bval(bytes_):
        """n-length ord"""
        return [b for b in bytes_]

    @staticmethod
    def pad(n, m):
        """return increment to next multiple of m"""
        return -n % m

    @staticmethod
    def used(n, m):
        """integer division rounding up"""
        return (n + m - 1) // m

    @staticmethod
    def upmod(n, mod):
        """modulo, but 1..mod"""
        return n % mod or mod

    @staticmethod
    def xint(s):
        """return hex or decimal value"""
        return int(s.lstrip('>'), 16 if s[:2] == '0x' or s[:1] == '>' else 10)

    @staticmethod
    def id_function(x):
        """identity function"""
        return x

    @staticmethod
    def tiname(s):
        """create TI filename from local filename"""
        return Util.to_ti(os.path.splitext(os.path.basename(s))[0][:10].upper())

    @staticmethod
    def to_pc(n):
        """escaoe TI filename for PC"""
        return None if n is None else n.replace('/', '.')

    @staticmethod
    def to_ti(n):
        """escape PC name for TI"""
        return None if n is None else n.replace('.', '/')

    @staticmethod
    def strinc(s):
        """create new string by increasing last char"""
        return s[:-1] + chr(ord(s[-1]) + 1)

    @staticmethod
    def chop(s, n):
        """generator that produces n-sized parts of s"""
        while True:
            part, s = s[:n], s[n:]
            if not part:
                break
            yield part

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

    @staticmethod
    def readdata(filename, data=None, encoding=None):
        """read data from file or STDIN (or return supplied data)"""
        if encoding is None:
            if filename == '-':
                return data or sys.stdin.buffer.read()
            else:
                with open(filename, 'rb') as f:
                    data = f.read()
                    return data
        else:
            try:
                if filename == '-':
                    return data or sys.stdin.read().encode(encoding)
                else:
                    with open(filename, 'r') as f:
                        data = f.read()
                    return data.encode(encoding)
            except UnicodeDecodeError:
                sys.exit('Bad encoding: ' + encoding)


# Sector-based disk image

class DiskError(Exception):
    pass


class Disk:
    """sector-based TI disk image file"""

    BYTES_PER_SECTOR = 256
    DEFAULT_SECTORS_PER_TRACK = 9
    DEFAULT_TRACKS = 40
    MAX_SECTORS = 1600
    BLANK_BYTE = b'\xe5'

    DISK_NAME_LEN = 0x0a
    TOTAL_SECTORS = 0x0a
    TOTAL_SECTORS_END = 0x0c
    SECTORS_PER_TRACK = 0x0c
    DSK_ID = 0x0d
    DSK_ID_END = 0x10
    DISK_PROTECTED = 0x10
    TRACKS_PER_SIDE = 0x11
    SIDES = 0x12
    DENSITY = 0x13
    ALLOC_BITMAP = 0x38
    RESERVED = 0x14
    DATA = 0x100

    def __init__(self, image, console=None):
        if len(image) < 2 * Disk.BYTES_PER_SECTOR:
            raise DiskError('Invalid disk image')
        self.image = image
        self.console = console or Console()
        self.catalog = {}
        self.read_sectors = []
        # meta data
        sector_0 = self.get_sector(0)
        if sector_0[0] == 0x00 and sector_0[21:23] == b'\x00\xfe':
            raise DiskError('Track dump images not supported')
        try:
            self.name = sector_0[:self.DISK_NAME_LEN].decode()
        except UnicodeDecodeError:
            self.name = 'INVALID   '
            self.console.warn('Disk name contains invalid Unicode', category=Console.CAT_IMAGE)
        self.total_sectors = Util.ordn(sector_0[Disk.TOTAL_SECTORS:Disk.TOTAL_SECTORS_END])
        self.sectors_per_track = sector_0[Disk.SECTORS_PER_TRACK]
        self.dsk_id = sector_0[Disk.DSK_ID:Disk.DSK_ID_END]
        self.protected = sector_0[Disk.DISK_PROTECTED]  # int, not boolean
        self.tracks_per_side = sector_0[Disk.TRACKS_PER_SIDE]
        self.sides = sector_0[Disk.SIDES]
        self.density = sector_0[Disk.DENSITY]
        self.alloc_bitmap = sector_0[Disk.ALLOC_BITMAP:]
        if self.dsk_id != b'DSK':
            self.console.warn('Disk image not initialized', category=Console.CAT_IMAGE)
        if len(self.image) < self.total_sectors * Disk.BYTES_PER_SECTOR:
            self.console.warn('Disk image truncated', category=Console.CAT_IMAGE)
        self.used_sectors = 0
        try:
            for i in range(Util.used(self.total_sectors, 8)):
                self.used_sectors += bin(self.alloc_bitmap[i]).count('1')
        except IndexError:
            self.console.warn('Allocation map corrupted', category=Console.CAT_ALLOC)
        self.check_geometry()
        self.init_catalog()
        self.check_allocation()

    def check_geometry(self):
        """check geometry against sector count"""
        if self.total_sectors != self.sides * self.tracks_per_side * self.sectors_per_track:
            self.console.warn('Sector count does not match disk geometry', category=Console.CAT_GEOMETRY)
        if self.total_sectors % 8 != 0:
            self.console.warn('Sector count is not multiple of 8', category=Console.CAT_GEOMETRY)

    def rename(self, name):
        """rename disk"""
        self.name = name
        if len(self.name.encode()) > Disk.DISK_NAME_LEN:
            raise DiskError('Encoded name is too long')
        self.image = self.name.encode() + b' ' * (Disk.DISK_NAME_LEN - len(self.name)) + self.image[Disk.DISK_NAME_LEN:]

    def init_catalog(self):
        """read all files from disk"""
        sector_1 = self.get_sector(1)
        sector_count = 0
        for i in range(0, Disk.BYTES_PER_SECTOR, 2):
            # get file descriptor
            fd_index = Util.ordn(sector_1[i:i + 2])
            if fd_index == 0:
                break
            try:
                fd_sector = self.get_sector(fd_index, b'FDR#%d' % fd_index)
            except IndexError:
                self.console.warn('File descriptor index corrupted')
                continue
            fd = FileDescriptor.create_from_fdr_sector(fd_sector)
            # get file contents
            data = self.read_file(fd)
            self.catalog[fd.name] = File(fd=fd, data=data, console=self.console)
            sector_count += fd.total_sectors + 1
        # consistency check
        if sector_count != self.used_sectors - 2:
            self.console.warn('Used sector mismatch: found {} file sectors, expected {}'.format(
                sector_count, self.used_sectors - 2))

    def read_file(self, fd):
        """read file contents based on FDR cluster data"""
        parts = []
        offset = -1
        for i in range(0, len(fd.clusters) - 2, 3):
            start = fd.clusters[i] | (fd.clusters[i + 1] & 0x0f) << 8
            if start == 0:
                break
            prev_offset = offset
            offset = fd.clusters[i + 1] >> 4 | fd.clusters[i + 2] << 4
            for j in range(offset - prev_offset):
                try:
                    parts.append(self.get_sector(start + j, fd.name))
                except IndexError:
                    self.console.warn(f'{fd.name:s}: File contents corrupted')
                    fd.error = True
                    continue
        data = b''.join(parts)
        return data

    def glob_files(self, patterns):
        """return listing of filenames matching glob pattern"""
        wildcards = [pattern for pattern in patterns if re.search(r'[?*]', pattern)]
        glob_re = '|'.join(re.escape(p).replace(r'\*', '.*').replace(r'\?', '.')
                           for p in wildcards) + '$'
        matches = [name for name in self.catalog if re.match(glob_re, name)]
        plains = [pattern for pattern in patterns if pattern not in wildcards]
        return matches + plains

    def rebuild_disk(self):
        """rebuild disk metadata after changes to file catalog"""
        required_sectors = sum(self.catalog[n].fd.total_sectors for n in self.catalog)
        # preferred start at sector >22
        first_free = next_free_sector = min(max(2 + len(self.catalog), 0x22), self.total_sectors - required_sectors)
        if first_free < 2 + len(self.catalog):
            raise DiskError('Disk full, lacking {} sectors'.format(2 + len(self.catalog) - first_free))
        sector_1 = b''
        index = 2
        for idx, file_ in sorted(self.catalog.items()):
            # put file data into single cluster
            data = file_.data + bytes(Util.pad(len(file_.data), Disk.BYTES_PER_SECTOR))
            for i in range(file_.fd.total_sectors):
                self.set_sector(next_free_sector + i, data[Disk.BYTES_PER_SECTOR * i:Disk.BYTES_PER_SECTOR * (i + 1)])
            # build file descriptor
            if file_.fd.total_sectors > 0:
                start = next_free_sector
                offset = file_.fd.total_sectors - 1
            else:
                start = offset = 0
            file_.fd.clusters = (bytes((start & 0xff, start >> 8 | (offset & 0xf) << 4, offset >> 4)) +
                                 bytes(Disk.BYTES_PER_SECTOR - 0x1c - 3))
            self.set_sector(index, file_.fd.get_disk_or_v9t9_header())
            # update FDR index in sector 1
            sector_1 += Util.chrn(index)
            next_free_sector += file_.fd.total_sectors
            index += 1
        sector_1 += bytes(Disk.BYTES_PER_SECTOR - len(sector_1))
        self.set_sector(1, sector_1)
        # update allocation bitmap in sector 0 (used: 0..i-1, ff..nf-1)
        assert 0 < index <= first_free <= next_free_sector
        mask = int('1' * (next_free_sector - first_free) +
                   '0' * (first_free - index) + '1' * index, 2)  # bitmap as bits, parsed into (very large) int
        bytes_ = []
        for i in range(self.total_sectors // 8):
            bytes_.append(bytes((mask & 0xff,)))  # byte-ize int from the tail
            mask >>= 8
        self.alloc_bitmap = b''.join(bytes_) + b'\xff' * (Disk.BYTES_PER_SECTOR - Disk.ALLOC_BITMAP - len(bytes_))
        sector_0 = self.get_sector(0)
        self.set_sector(0, sector_0[:self.ALLOC_BITMAP] + self.alloc_bitmap)

    @staticmethod
    def extend_sectors(image, new_size):
        """increase total number of sectors and clear alloc map (for xvm99)"""
        current = Util.ordn(image[Disk.TOTAL_SECTORS:Disk.TOTAL_SECTORS_END])
        if not current <= new_size <= Disk.MAX_SECTORS:
            raise DiskError(f'Invalid size {new_size:d} for sector increase')
        if current % 8 != 0:
            raise DiskError('Sector count must be multiple of 8')
        bitmap = (image[Disk.ALLOC_BITMAP:Disk.ALLOC_BITMAP + current // 8] +
                  b'\xff' * (Disk.BYTES_PER_SECTOR - Disk.ALLOC_BITMAP - current // 8))
        return (image[:Disk.DISK_NAME_LEN] + Util.chrn(new_size) + image[Disk.SECTORS_PER_TRACK:Disk.ALLOC_BITMAP] +
                bitmap + image[Disk.DATA:])

    @staticmethod
    def trim_sectors(image):
        """shrink image to actually existing sectors"""
        total_sectors = Util.ordn(image[Disk.TOTAL_SECTORS:Disk.TOTAL_SECTORS_END])
        return image[:total_sectors * Disk.BYTES_PER_SECTOR]

    def get_sector(self, sector_no, context=None):
        """retrieve sector from image"""
        if sector_no > 0 and sector_no >= self.total_sectors:
            if sector_no < len(self.image) // Disk.BYTES_PER_SECTOR:
                self.console.warn('Total sectors not set properly')
            else:
                raise IndexError('Invalid sector number')
        if context:
            self.read_sectors.append((sector_no, context))
        offset = sector_no * Disk.BYTES_PER_SECTOR
        return self.image[offset:offset + Disk.BYTES_PER_SECTOR]

    def set_sector(self, sector_no, data):
        """write sector to image"""
        if sector_no > self.total_sectors:
            raise IndexError('Invalid sector number')
        if len(data) != Disk.BYTES_PER_SECTOR:
            raise ValueError(f'Invalid data for sector {sector_no:d}: found {len(data):d} bytes, ' +
                             f'expected {Disk.BYTES_PER_SECTOR:d}')
        offset = sector_no * Disk.BYTES_PER_SECTOR
        self.image = self.image[:offset] + data + self.image[offset + Disk.BYTES_PER_SECTOR:]

    def get_file(self, name):
        """get File object from disk catalog"""
        try:
            return self.catalog[name]
        except KeyError:
            raise DiskError(f'File {name} not found')

    def add_file(self, file_):
        """add or update File object in image"""
        self.catalog[file_.fd.name] = file_
        self.rebuild_disk()

    def remove_file(self, name):
        """remove file from image"""
        try:
            del self.catalog[name]
            self.rebuild_disk()
        except KeyError:
            raise DiskError(f'File {name} not found')

    def rename_files(self, names):
        """rename files in image"""
        # rename dry-run
        try:
            for old, new in names:
                if old not in self.catalog:
                    raise DiskError(f'File {old} not found')
                if new in self.catalog:
                    raise DiskError(f'File {new} already exists')
        except ValueError:
            raise DiskError('Bad renaming argument')
        # actual renaming
        for old, new in names:
            self.catalog[old].fd.name = new
            self.catalog[new] = self.catalog[old]
            del self.catalog[old]
        self.rebuild_disk()

    def protect_file(self, name):
        """toggle protection for given file"""
        try:
            file_ = self.catalog[name]
        except KeyError:
            raise DiskError(f'File {name} not found')
        file_.fd.toggle_protection()
        self.rebuild_disk()

    def check_allocation(self):
        """check sector allocation for consistency"""
        reads = {n: [] for n in range(self.total_sectors)}
        allocated = []
        for i in range(Util.used(self.total_sectors, 8)):
            try:
                b = self.alloc_bitmap[i]
            except IndexError:
                break
            for bit in range(8):
                allocated.append(b & (1 << bit) != 0)
        # unallocated sectors
        for sector_no, context in self.read_sectors:
            reads[sector_no].append(context)
            if context and not allocated[sector_no]:
                self.console.warn(f'{context}: Used sector {sector_no} not allocated')
                if file_ := self.catalog.get(context):
                    file_.fd.error = True
        # sectors allocated to multiple files
        for sector_no, files in reads.items():
            if len(files) <= 1:
                continue
            self.console.warn(f"Sector {sector_no} claimed by multiple files: {'/'.join(files)}")
            for name in files:
                if file_ := self.catalog.get(name):
                    file_.fd.error = True

    def resize_disk(self, new_size):
        """resize image to given sector count"""
        if not 2 < new_size <= Disk.MAX_SECTORS:
            raise DiskError(f'Invalid disk size, expected between 2 and {Disk.MAX_SECTORS} sectors')
        if self.total_sectors % 8 != 0 or new_size % 8 != 0:
            raise DiskError('Disk size must be multiple of 8 sectors')
        old_size = self.total_sectors
        self.total_sectors = new_size
        self.used_sectors = 0
        self.rebuild_disk()
        self.image = (self.image[:Disk.DISK_NAME_LEN] + Util.chrn(new_size) +
                      self.image[Disk.SECTORS_PER_TRACK:new_size * self.BYTES_PER_SECTOR] +
                      self.BLANK_BYTE * ((new_size - old_size) * self.BYTES_PER_SECTOR))

    def set_geometry(self, sides, density, tracks):
        """override geometry of disk image"""
        if sides:
            self.sides = sides
        if density:
            self.density = density
        if tracks:
            self.tracks_per_side = tracks
        self.sectors_per_track = Disk.DEFAULT_SECTORS_PER_TRACK * self.density
        self.image = (self.image[:Disk.SECTORS_PER_TRACK] + bytes((self.sectors_per_track,)) +
                      self.image[Disk.DSK_ID:Disk.TRACKS_PER_SIDE] +
                      bytes((self.tracks_per_side, self.sides, self.density)) + self.image[Disk.RESERVED:])
        self.console.clear_warnings(Console.CAT_GEOMETRY)
        self.check_geometry()

    def fix_disk(self):
        """rebuild disk with non-erroneous files"""
        for name, file_ in self.catalog.items():
            if file_.fd.error:
                del self.catalog[name]
        self.rebuild_disk()

    def get_tifiles_file(self, name):
        """get file in TIFILES format from disk catalog"""
        file_ = self.get_file(name)
        return file_.get_as_tifiles()

    def get_sdd99_file(self, name, loadtype=0):
        """get file in SDD99 format from disk catalog"""
        file_ = self.get_file(name)
        return file_.get_as_sdd99(loadtype=loadtype)

    def get_v9t9_file(self, name):
        """get file in v9t9 format from disk catalog"""
        file_ = self.get_file(name)
        return file_.get_as_v9t9()

    def get_info(self):
        """return information about disk image"""
        return '{:10s}: {:c}   {:d} used  {:d} free   {:d} KB  {:d}S/{:d}D {:d}T  {:d} S/T\n'.format(
                self.name,
                self.protected,
                self.used_sectors,
                self.total_sectors - self.used_sectors,
                self.total_sectors * Disk.BYTES_PER_SECTOR // 1024,
                self.sides,
                self.density,
                self.tracks_per_side,
                self.sectors_per_track)

    def get_catalog(self):
        """return formatted disk catalog"""
        return ''.join(self.catalog[n].fd.get_info() for n in sorted(self.catalog))

    @staticmethod
    def blank_image(geometry, name):
        """return initialized disk image"""
        sectors, layout = Disk.parse_geometry(geometry, need_sectors=True)
        if layout:
            sides, density, tracks = layout
        else:
            sides = 2 if 360 <= (sectors - 1) % 720 else 1
            density = 2 if 720 < sectors <= 1440 else 1  # favor DSSD over SSDD
            tracks = Disk.DEFAULT_TRACKS
        if not 2 < sectors <= Disk.MAX_SECTORS or sectors % 8 != 0 or not (sides and density):
            raise DiskError('Invalid disk size')
        sector_0 = (b'%-10b%2b%cDSK ' % (name.encode()[:10],
                                         Util.chrn(sectors),
                                         Disk.DEFAULT_SECTORS_PER_TRACK * density) +  # header
                    bytes((tracks or Disk.DEFAULT_TRACKS, sides, density)) +
                    bytes(0x24) +  # reserved
                    b'\x03' + bytes(sectors // 8 - 1) +  # allocation map
                    b'\xff' * (Disk.BYTES_PER_SECTOR - sectors // 8 - Disk.ALLOC_BITMAP))
        return (sector_0 +
                bytes(Disk.BYTES_PER_SECTOR) +  # blank sector 1
                Disk.BLANK_BYTE * ((sectors - 2) * Disk.BYTES_PER_SECTOR))  # sectors 2 and up

    @staticmethod
    def parse_geometry(geometry, need_sectors=False):
        """get disk size and layout from geometry string"""
        if geometry.upper() == 'CF':
            return 1600, (1, 1, Disk.DEFAULT_TRACKS)
        try:
            sectors = Util.xint(geometry)
            return sectors, None
        except ValueError:
            pass
        sides = density = tracks = None
        geometry_parts = re.split(r'(\d+|[SD])([SDT])', geometry.upper())
        if ''.join(geometry_parts[::3]) not in ('', '/'):
            raise DiskError('Invalid disk geometry ' + geometry)
        try:
            for spec, part in zip(geometry_parts[1::3], geometry_parts[2::3]):
                val = 1 if spec == 'S' else 2 if spec == 'D' else int(spec)
                if part == 'S' and sides is None:
                    sides = val
                elif part == 'D' and density is None:
                    density = val
                elif part == 'T' and tracks is None:
                    tracks = val
                else:
                    raise DiskError('Invalid disk geometry: ' + geometry)
        except (IndexError, ValueError):
            raise DiskError('Invalid disk geometry: ' + geometry)
        try:
            sectors = sides * (tracks or Disk.DEFAULT_TRACKS) * Disk.DEFAULT_SECTORS_PER_TRACK * density
        except TypeError:
            if need_sectors:
                raise DiskError('Unspecified disk geometry: ' + geometry)
            else:
                sectors = None
        return sectors, (sides, density, tracks)


# Files

class FileError(Exception):
    pass


class FileDescriptor:
    """file meta data descriptor based on TI disk image format"""

    DISPLAY = 0x00
    PROGRAM = 0x01
    INTERNAL = 0x02
    UNKNOWN = 0x03
    FIXED = 0x00
    VARIABLE = 0x80
    PROTECTED = 0x08

    FILE_NAME_LEN = 0x0a
    FLAGS = 0x0c
    RECORDS_PER_SECTOR = 0x0d
    TOTAL_SECTORS = 0x0e
    TOTAL_SECTORS_END = 0x10
    EOF_OFFSET = 0x10
    RECORD_LEN = 0x11
    LV3_RECORDS_LOW = 0x12
    LV3_RECORDS_HIGH = 0x13
    FILE_CLUSTER = 0x1c
    CREATED = 0x14
    CREATED_END = 0x18
    MODIFIED = 0x18
    MODIFIED_END = 0x1c

    TIF_TOTAL_SECTORS = 0x08
    TIF_TOTAL_SECTORS_END = 0x0a
    TIF_FLAGS = 0x0a
    TIF_RECORDS_PER_SECTOR = 0x0b
    TIF_EOF_OFFSET = 0x0c
    TIF_RECORD_LEN = 0x0d
    TIF_LV3_RECORDS_LOW = 0x0e
    TIF_LV3_RECORDS_HIGH = 0x0f
    TIF_FILE_NAME = 0x10
    TIF_CREATED = 0x1e
    TIF_CREATED_END = 0x22
    TIF_MODIFIED = 0x22
    TIF_MODIFIED_END = 0x26

    def __init__(self, flags=0, format_=None, records_per_sector=0, total_sectors=0, eof_offset=0, record_len=0,
                 lv3_records=0, name=None, created=None, modified=None, clusters=None, hostfn=None):
        self.error = False
        self.type = None
        self.mode = None
        self.protected = False
        self.name = name
        self.flags = flags
        self.format = format_  # display format
        self.total_sectors = total_sectors
        self.eof_offset = eof_offset
        self.lv3_records = lv3_records
        self.size = 0
        self.records_per_sector = records_per_sector
        self.record_len = record_len
        self.created = created  # time and date
        self.modified = modified
        self.clusters = clusters
        self.hostfn = hostfn
        # compute dependent values
        self.type = (FileDescriptor.DISPLAY, FileDescriptor.PROGRAM,
                     FileDescriptor.INTERNAL, FileDescriptor.UNKNOWN)[self.flags & 0x03]
        self.mode = FileDescriptor.VARIABLE if self.flags & 0x80 else FileDescriptor.FIXED
        self.format = ('DIS/', 'PROGRAM', 'INT/', 'unknown')[self.flags & 0x03]
        if self.type in (FileDescriptor.DISPLAY, FileDescriptor.INTERNAL):
            self.format += ('VAR ' if self.mode == FileDescriptor.VARIABLE else 'FIX ') + str(self.record_len)
        self.protected = self.flags & 0x08
        self.size = self.get_filesize()

    @staticmethod
    def create(name, format_):
        """create new empty file descriptor"""
        m_fmt = re.match(r'([PDIB])[ROGAMISNT]*(?:/?([VF])[ARIX]*\s*(\d+))?', format_.upper())
        if not m_fmt:
            raise FileError('Unknown file format: ' + format_)
        # build flags for specified format
        fmt_type = m_fmt.group(1)
        if fmt_type == 'P':  # P, D, or I
            flags = FileDescriptor.PROGRAM
            record_len = records_per_sector = 0
        else:
            fmt_mode = m_fmt.group(2)  # F or V
            flags = ((FileDescriptor.INTERNAL if fmt_type == 'I' else FileDescriptor.DISPLAY) |
                     (FileDescriptor.FIXED if fmt_mode == 'F' else FileDescriptor.VARIABLE))
            fmt_len = m_fmt.group(3)
            record_len = int(fmt_len) if fmt_len else 80
            records_per_sector = ((Disk.BYTES_PER_SECTOR if fmt_mode == 'F' else Disk.BYTES_PER_SECTOR - 2) //
                                  record_len) % Disk.BYTES_PER_SECTOR  # mod for DF1
        created = modified = FileDescriptor.encode_date(datetime.datetime.now())
        return FileDescriptor(name=name, format_=format_, flags=flags, record_len=record_len,
                              records_per_sector=records_per_sector, created=created, modified=modified)

    @staticmethod
    def create_from_fdr_sector(sector):
        """create file descriptor from FDR sector"""
        if len(sector) < 0x20:
            raise FileError('Invalid file descriptor')
        try:
            name = sector[:FileDescriptor.FILE_NAME_LEN].decode().rstrip()
        except UnicodeDecodeError:
            raise FileError('Invalid Unicode filename')
        flags = sector[FileDescriptor.FLAGS]
        records_per_sector = sector[FileDescriptor.RECORDS_PER_SECTOR]
        total_sectors = Util.ordn(sector[FileDescriptor.TOTAL_SECTORS:FileDescriptor.TOTAL_SECTORS_END])
        eof_offset = sector[FileDescriptor.EOF_OFFSET]
        record_len = sector[FileDescriptor.RECORD_LEN]
        created = sector[FileDescriptor.CREATED:FileDescriptor.CREATED_END]  # time, date
        modified = sector[FileDescriptor.MODIFIED:FileDescriptor.MODIFIED_END]
        clusters = sector[FileDescriptor.FILE_CLUSTER:]
        lv3_records = ((sector[FileDescriptor.LV3_RECORDS_HIGH] << 8) |
                       sector[FileDescriptor.LV3_RECORDS_LOW])  # only correct for FIXED files
        return FileDescriptor(name=name, flags=flags, records_per_sector=records_per_sector,
                              total_sectors=total_sectors, eof_offset=eof_offset, record_len=record_len,
                              created=created, modified=modified, clusters=clusters, lv3_records=lv3_records)

    @staticmethod
    def create_from_tif_header(header, hostfn=None):
        """create file descriptor from TIFILES header"""
        if len(header) < 0x26 or not File.is_tifiles(header):
            raise FileError('Invalid TIFILES header')
        total_sectors = Util.ordn(header[FileDescriptor.TIF_TOTAL_SECTORS:FileDescriptor.TIF_TOTAL_SECTORS_END])
        flags = header[FileDescriptor.TIF_FLAGS] & 0x83
        records_per_sector = header[FileDescriptor.TIF_RECORDS_PER_SECTOR]
        eof_offset = header[FileDescriptor.TIF_EOF_OFFSET]
        record_len = header[FileDescriptor.TIF_RECORD_LEN]
        lv3_records = ((header[FileDescriptor.TIF_LV3_RECORDS_HIGH] << 8) |
                       header[FileDescriptor.TIF_LV3_RECORDS_LOW])  # only correct for FIXED files
        if header[0x10] == 0x00:
            # short TIFILES: use file properties
            name = Util.tiname(hostfn)
            dt = datetime.datetime.fromtimestamp(os.path.getctime(hostfn))
            created = FileDescriptor.encode_date(dt)
            dt = datetime.datetime.fromtimestamp(os.path.getmtime(hostfn))
            modified = FileDescriptor.encode_date(dt)
        else:
            # long TIFILES: use header data
            name = header[FileDescriptor.TIF_FILE_NAME:
                          FileDescriptor.TIF_FILE_NAME + FileDescriptor.FILE_NAME_LEN].decode().rstrip()
            created = header[FileDescriptor.TIF_CREATED:FileDescriptor.TIF_CREATED_END]
            modified = header[FileDescriptor.TIF_MODIFIED:FileDescriptor.TIF_MODIFIED_END]
        return FileDescriptor(name=name, flags=flags, records_per_sector=records_per_sector, eof_offset=eof_offset,
                              total_sectors=total_sectors, record_len=record_len, lv3_records=lv3_records,
                              created=created, modified=modified)

    def get_filesize(self):
        """returns file size, excluding FDR (supports SDD99 extension)"""
        return (self.total_sectors * Disk.BYTES_PER_SECTOR -
                Util.pad(self.eof_offset, Disk.BYTES_PER_SECTOR))  # excludes FDR

    def toggle_protection(self):
        self.protected = not self.protected
        self.flags ^= FileDescriptor.PROTECTED

    @staticmethod
    def encode_date(dt):
        """convert datetime object into FDR date and time word"""
        date = (dt.year % 100) << 9 | dt.month << 5 | dt.day
        time = dt.hour << 11 | dt.minute << 5 | dt.second // 2
        return Util.chrn(time) + Util.chrn(date)

    @staticmethod
    def decode_date(qword):
        """extract date and time information from header data"""
        time = Util.ordn(qword[0:2])
        date = Util.ordn(qword[2:4])
        try:
            return datetime.datetime(
                    (date >> 9) + (1900 if date >> 9 >= 70 else 2000),  # 1970 is cut-off year for 1900s
                    date >> 5 & 0x0f,
                    date & 0x1f,
                    time >> 11,
                    time >> 5 & 0x3f,
                    (time & 0x0f) * 2)
        except ValueError:
            return None

    def get_disk_or_v9t9_header(self, v9t9=False):
        """return FDR as disk image sector"""
        if self.total_sectors == 0xffff:
            raise FileError('File too large for disk/v9t9 (max. 16 MB)')
        records = self.total_sectors if self.mode == FileDescriptor.VARIABLE else self.lv3_records  # per definition
        return (b'%-10b' % self.name.encode()[:10] +
                bytes((0, 0,
                       self.flags,
                       self.records_per_sector,
                       self.total_sectors >> 8, self.total_sectors & 0xff,
                       self.eof_offset,
                       self.record_len,
                       records & 0xff, records >> 8,
                       *Util.bval(self.created + self.modified))) +
                (bytes(100) if v9t9 else self.clusters))

    def get_tifiles_header(self, sdd99_loadtype=None):
        """return FDR as TIFILES header"""
        if sdd99_loadtype is None:
            if self.total_sectors > 0xffff:
                raise FileError('File too large for TIFILES format (max. 16 MB)')
            suffix = b' ' * 88
        else:
            suffix = (b' ' * 8 +
                      b'SDD99\x01' +
                      bytes((sdd99_loadtype, 0, (self.total_sectors >> 24) & 0xff, (self.total_sectors >> 16) & 0xff)) +
                      Util.chrn(self.lv3_records, 2) +
                      b' ' * 0x44)
        records = self.total_sectors if self.mode == FileDescriptor.VARIABLE else self.lv3_records  # per definition
        return (b'\x07TIFILES' +
                bytes((self.total_sectors >> 8, self.total_sectors & 0xff,
                       self.flags,
                       self.records_per_sector,
                       self.eof_offset,
                       self.record_len,
                       records & 0xff, (records >> 8) & 0xff)) +
                b'%-10b' % self.name.encode()[:10] +
                bytes((0, 0, 0xff, 0xff, *Util.bval(self.created + self.modified), 0, 0)) +
                suffix)

    def get_info(self):
        """return information about file"""
        date_str = FileDescriptor.decode_date(self.modified)
        return '{:10s} {:4d}  {:11s} {:6d} B {:>8s}  {:1s}  {:>19s} {:s}  {:1s}\n'.format(
            self.name,
            self.total_sectors + 1,
            self.format,
            self.size,
            '{:3d} recs'.format(self.lv3_records) if self.type != FileDescriptor.PROGRAM else '',
            'P' if self.protected else '',
            '' if date_str is None else str(date_str),
            ('' if self.modified == self.created == bytes(4) or date_str is None else
                'C' if self.modified == self.created else 'M'),
            'ERR' if self.error else '')


class File:
    """main file object with FDR metadata and sector contents"""

    HEADER_LEN = 0x80

    def __init__(self, fd=None, records=None, data=None, console=None):
        self.console = console or Console()
        self.fd = fd
        self.records = records
        self.data = data
        if fd is None or data is None:
            self.fd = self.data = None
        else:
            if records is None:
                self.records = self.unpack_records(fd, data)

    @staticmethod
    def create_new(name, format_, data, console=None):
        """create plain file"""
        fd = FileDescriptor.create(name, format_)
        records = File.split_contents(fd, data)
        data_ = File.pack_records(fd, records, console=console)  # repack, also sets file size information
        return File(fd=fd, records=records, data=data_, console=console)

    @staticmethod
    def create_from_tif_image(image, hostfn=None, console=None):
        """create TIFILES file"""
        if not File.is_tifiles(image):
            raise FileError('Invalid TIFILES image')
        fd = FileDescriptor.create_from_tif_header(image[:File.HEADER_LEN], hostfn=hostfn)
        data = image[File.HEADER_LEN:]
        records = File.unpack_records(fd, data)
        return File(fd=fd, data=data, records=records, console=console)

    @staticmethod
    def create_from_v9t9_image(image, console=None):
        """create v9t9 file"""
        if not File.is_v9t9(image):
            raise FileError('Invalid v9t9 image')
        fd = FileDescriptor.create_from_fdr_sector(image[:File.HEADER_LEN])
        data = image[File.HEADER_LEN:]
        records = File.unpack_records(fd, data)
        return File(fd=fd, data=data, records=records, console=console)

    @staticmethod
    def split_contents(fd, data):
        """split blob into records"""
        if fd.type == FileDescriptor.PROGRAM:
            return data
        elif fd.mode == FileDescriptor.FIXED:
            reclen = fd.record_len
            return [data[i:i + reclen] for i in range(0, len(data), reclen)]
        elif fd.type == FileDescriptor.DISPLAY:
            return data.splitlines()
        else:
            records = []
            i = 0
            while i < len(data):
                reclen = data[i] + 1
                records.append(data[i + 1:i + reclen])  # remove record length
                i += reclen
            return records

    @staticmethod
    def unpack_records(fd, data):
        """extract list of records from sector image (-e)"""
        records = []
        if fd.type == FileDescriptor.PROGRAM:
            records = data[:fd.eof_offset - Disk.BYTES_PER_SECTOR] if fd.eof_offset else data
            fd.lv3_records = 0
        elif fd.mode == FileDescriptor.FIXED:
            records_per_sector = fd.records_per_sector or Disk.BYTES_PER_SECTOR
            record_count = recs_added_to_sector = sector = 0
            while record_count < fd.lv3_records:
                if recs_added_to_sector >= records_per_sector:
                    sector += 1
                    recs_added_to_sector = 0
                    continue
                idx = sector * Disk.BYTES_PER_SECTOR + recs_added_to_sector * fd.record_len
                records.append(data[idx:idx + fd.record_len])
                record_count += 1
                recs_added_to_sector += 1
            fd.lv3_records = record_count
        else:  # VARIABLE
            record_count = offset_in_sector = sector = 0
            while sector < fd.total_sectors:
                idx = sector * Disk.BYTES_PER_SECTOR + offset_in_sector
                record_len = data[idx] if idx < len(data) else -1
                if (record_len == 0xff and offset_in_sector > 0) or record_len == -1:
                    sector += 1
                    offset_in_sector = 0
                    continue
                records.append(data[idx + 1:idx + 1 + record_len])  # store w/o record length
                record_count += 1
                if record_len == 0xff and offset_in_sector == 0:  # DIS/VAR255
                    sector += 1
                else:
                    offset_in_sector += record_len + 1
            fd.lv3_records = record_count
        return records

    @staticmethod
    def pack_records(fd, records, console=None):
        """create sector image from listing of records (-a), sets size information"""
        parts = []
        record_count = sectors = offset_in_sector = 0
        if fd.type == FileDescriptor.PROGRAM:
            data = records
            fd.eof_offset = len(data) % Disk.BYTES_PER_SECTOR
            sectors = Util.used(len(data), Disk.BYTES_PER_SECTOR)
            fd.lv3_records = 0
        elif fd.mode == FileDescriptor.FIXED:
            for record in records:
                if len(record) > fd.record_len:
                    if console:
                        console.warn(f'Record #{record_count} too long, truncating {len(record) - fd.record_len} bytes')
                    record = record[:fd.record_len]
                if offset_in_sector + fd.record_len > Disk.BYTES_PER_SECTOR:
                    parts.append(bytes(Disk.BYTES_PER_SECTOR - offset_in_sector))
                    sectors += 1
                    offset_in_sector = 0
                pad_len = fd.record_len - len(record)
                parts.append(record + (bytes(pad_len) if fd.type == FileDescriptor.INTERNAL else b' ' * pad_len))
                offset_in_sector += fd.record_len
                record_count += 1
            data = b''.join(parts)
            fd.eof_offset = offset_in_sector % Disk.BYTES_PER_SECTOR
            sectors = sectors + 1
            fd.lv3_records = record_count
        else:  # VARIABLE
            for record in records:
                if len(record) > fd.record_len:
                    if console:
                        console.warn(f'Record #{record_count} too long, truncating {len(record) - fd.record_len} bytes')
                    record = record[:fd.record_len]
                if offset_in_sector + 1 + len(record) + 1 > Disk.BYTES_PER_SECTOR and offset_in_sector > 0:
                    parts.append(b'\xff' + bytes(Disk.BYTES_PER_SECTOR - offset_in_sector - 1))
                    sectors += 1
                    offset_in_sector = 0
                parts.append(bytes((len(record),)) + record)
                record_count += 1
                if len(record) == Disk.BYTES_PER_SECTOR - 1:  # VAR255
                    sectors += 1
                    offset_in_sector = 0
                else:
                    offset_in_sector += len(record) + 1
            if offset_in_sector > 0:
                parts.append(b'\xff')  # EOF marker
                sectors += 1
            data = b''.join(parts)
            fd.eof_offset = offset_in_sector
            fd.lv3_records = record_count
        fd.total_sectors = sectors
        fd.size = (fd.total_sectors * Disk.BYTES_PER_SECTOR -
                   Util.pad(fd.eof_offset, Disk.BYTES_PER_SECTOR))
        return data + bytes(Util.pad(len(data), Disk.BYTES_PER_SECTOR))

    def get_contents(self, encoding=None):
        """return file contents as serialized records"""
        if self.fd.type == FileDescriptor.PROGRAM:
            return self.records
        elif self.fd.mode == FileDescriptor.FIXED:
            return b''.join(self.records)
        elif self.fd.type == FileDescriptor.DISPLAY:
            if encoding is None:
                return b''.join(r + b'\n' for r in self.records)  # as binary
            else:
                try:
                    return ''.join(r.encode(encoding) + '\n' for r in self.records)  # as text
                except UnicodeEncodeError:
                    raise DiskError('Bad encoding')
        else:  # INTERNAL
            return b''.join(bytes((len(r),)) + r for r in self.records)  # add length byte

    def get_as_tifiles(self):
        """return file contents in TIFILES format"""
        return self.fd.get_tifiles_header() + self.clean_data()

    def get_as_sdd99(self, loadtype=0):
        """return file contents in TIFILES format with SDD 99 extensions"""
        return self.fd.get_tifiles_header(sdd99_loadtype=loadtype) + self.clean_data()

    def get_as_v9t9(self):
        """return file contents in v9t9 format"""
        return self.fd.get_disk_or_v9t9_header(v9t9=True) + self.clean_data()

    def clean_data(self):
        """zero bytes in data which are not part of payload"""
        eof = self.fd.eof_offset
        if self.fd.type == FileDescriptor.PROGRAM:
            cutoff = eof - Disk.BYTES_PER_SECTOR if eof else None
        elif self.fd.mode == FileDescriptor.FIXED:
            records_in_last_sector = Util.upmod(self.fd.lv3_records, self.fd.records_per_sector or 256)
            cutoff = records_in_last_sector * self.fd.record_len - Disk.BYTES_PER_SECTOR or None
        elif self.fd.mode == FileDescriptor.VARIABLE:
            eof += 1 if eof else 0  # include >ff byte for VARIABLE files
            cutoff = eof - Disk.BYTES_PER_SECTOR if 0 < eof < Disk.BYTES_PER_SECTOR else None
        else:
            raise FileError('Unknown file type for ' + self.fd.name)
        payload = self.data[:cutoff]
        return payload + bytes(Util.pad(len(payload), Disk.BYTES_PER_SECTOR))

    @staticmethod
    def is_tifiles(image):
        """check if file image has valid TIFILES header"""
        return image[:8] == b'\x07TIFILES'

    @staticmethod
    def is_v9t9(image):
        """check if file image has v9t9 header"""
        return all(32 <= c < 127 for c in image[:10]) and image[0x30:File.HEADER_LEN] == bytes(0x50)

    def get_info(self):
        """return file meta data"""
        return self.fd.get_info()


class Console:
    """collects errors and warnings"""

    CAT_WARNING = 0
    CAT_ALLOC = 1
    CAT_GEOMETRY = 2
    CAT_IMAGE = 3

    ERROR = 2  # severity

    def __init__(self, disable_warnings=False, colors=None):
        self.enabled_warnings = not disable_warnings
        self.warnings = {}  # category x list
        self.errors = []
        if colors is None:
            self.colors = platform.system() in ('Linux', 'Darwin')  # no auto color on Windows
        else:
            self.colors = colors == 'on'

    def warn(self, message, category=CAT_WARNING):
        """record warning message"""
        try:
            if message not in self.warnings[category]:
                self.warnings[category].append(message)
        except KeyError:
            self.warnings.setdefault(category, []).append(message)

    def error(self, message):
        """record error message"""
        self.errors.append(message)

    def clear_warnings(self, category):
        """clear all warnings in given category"""
        try:
            del self.warnings[category]
        except KeyError:
            pass

    def print(self):
        """print all warnings and errors"""
        if self.enabled_warnings:
            for cat in self.warnings.keys():
                for text in self.warnings[cat]:
                    sys.stderr.write(self.color(f'Warning: {text}', severity=1) + '\n')
        for text in self.errors:
            sys.stderr.write(self.color(f'Error: {text}', severity=2) + '\n')

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

    def process_dump(self, s):
        """format binary string as hex dump (for -S)"""
        result = []
        for i in range(0, len(s), 16):
            bs = b''  # use bytes, like all other functions do
            cs = b''
            for j in range(16):
                try:
                    bs += b'%02X ' % s[i + j]
                    cs += bytes((s[i + j],)) if 32 <= s[i + j] < 127 else b'.'
                except IndexError:
                    bs += b'   '
                    cs += b' '
                if j % 4 == 3:
                    bs += b' '
                    cs += b' '
            result.append(b'%02X:  %b %b\n' % (i, bs, cs))
        return b''.join(result)

    def process_image_command(self, opts, external_data=None):
        """disk image manipulation"""
        rc = 0
        result = []  # data x filename x is disk?
        format_ = opts.format.upper() if opts.format else 'PROGRAM'

        # get disk image
        if opts.init:
            barename = os.path.splitext(os.path.basename(opts.filename))[0]
            image = Disk.blank_image(opts.init, Util.to_ti(opts.name) or barename[:10].upper())
            result = (image, opts.filename, True),
        else:
            image = external_data or Util.readdata(opts.filename)
        disk = Disk(image, console=self.console)

        # apply command to image
        if opts.print_:
            files = disk.glob_files(opts.print_)
            contents = (disk.get_file(name).get_contents() for name in files)
            sys.stdout.buffer.write(b''.join(contents))
        elif opts.extract:
            files = disk.glob_files(opts.extract)
            if opts.output and len(files) > 1 and not os.path.isdir(opts.output):
                sys.exit(self.console.color('Error: -o must provide directory when extracting multiple files',
                                            severity=Console.ERROR))
            if opts.astifiles:
                contentfn = disk.get_tifiles_file
                namefn, extension = Util.to_pc, '.tfi'
            elif opts.assdd99 is not None:
                contentfn = lambda name: disk.get_sdd99_file(name, loadtype=Util.xint(opts.assdd99))
                namefn, extension = Util.to_pc, '.tfi'
            elif opts.asv9t9:
                contentfn = disk.get_v9t9_file
                namefn, extension = Util.to_pc, '.v9t9'
            else:
                contentfn = lambda name: disk.get_file(name).get_contents()
                namefn, extension = Util.to_pc, ''
            result = ((contentfn(name),
                       namefn(name).upper() if opts.tinames else namefn(name).lower() + extension,
                       False)
                      for name in files)
        elif opts.add:
            for name in opts.add:
                data = Util.readdata(name, encoding=opts.encoding)
                if name == '-':
                    name = 'STDIN'
                if opts.astifiles:
                    disk.add_file(File.create_from_tif_image(data, hostfn=name, console=self.console))
                elif opts.asv9t9:
                    disk.add_file(File.create_from_v9t9_image(data, console=self.console))
                else:
                    name = Util.to_ti(opts.name) if opts.name else Util.tiname(name)
                    if opts.name:
                        opts.name = Util.strinc(opts.name)
                    file_ = File.create_new(name, format_, data, console=self.console)
                    disk.add_file(file_)
            result = (disk.image, opts.filename, True),
        elif opts.rename:
            names = [Util.to_ti(arg).split(':') for arg in opts.rename]
            disk.rename_files(names)
            result = (disk.image, opts.filename, True),
        elif opts.delete:
            files = disk.glob_files(opts.delete)
            for name in files:
                disk.remove_file(name)
            result = (disk.image, opts.filename, True),
        elif opts.protect:
            files = disk.glob_files(opts.protect)
            for name in files:
                disk.protect_file(name)
            result = (disk.image, opts.filename, True),
        elif opts.resize:
            size, layout = Disk.parse_geometry(opts.resize, need_sectors=True)
            disk.resize_disk(size)
            if layout:
                sides, density, tracks = layout
                disk.set_geometry(sides, density, tracks or Disk.DEFAULT_TRACKS)
            result = (disk.image, opts.filename, True),
        elif opts.geometry:
            size, layout = Disk.parse_geometry(opts.geometry)
            try:
                disk.set_geometry(*layout)
            except TypeError:
                raise DiskError('Invalid disk geometry: ' + opts.geometry)
            result = (disk.image, opts.filename, True),
        elif opts.checkonly:
            rc = 1 if self.console.errors or self.console.warnings else 0
        elif opts.repair:
            disk.fix_disk()
            result = (disk.image, opts.filename, True),
        elif opts.sector:
            opts.quiet = True
            try:
                sector_no = Util.xint(opts.sector)
                sector = disk.get_sector(sector_no)
            except (IndexError, ValueError):
                raise DiskError(f'Invalid sector: {opts.sector}')
            result = (self.process_dump(sector), '-', False),
        elif opts.name and not opts.init:
            # at this point, '-n' is supplied without command, so rename disk
            disk.rename(Util.to_ti(opts.name))
            result = (disk.image, opts.filename, True),
        elif opts.info or not opts.init:
            sys.stdout.write(disk.get_info())
            sys.stdout.write('-' * 76 + '\n')
            sys.stdout.write(disk.get_catalog())
        return rc, result

    def process_file_command(self, opts):
        """file manipulation"""
        result = []
        # files to process (opts are mutually exclusive)
        files = opts.fromfiad or opts.tofiad or opts.printfiad or opts.infofiad
        if opts.output and len(files) > 1 and not os.path.isdir(opts.output):
            sys.exit(self.console.color('Error: -o must provide directory when providing multiple files',
                                        severity=Console.ERROR))
        fmt = opts.format.upper() if opts.format else 'PROGRAM'

        for idx, filename in enumerate(files):
            image = Util.readdata(filename)
            if opts.tofiad:
                name = Util.to_ti(opts.name) or Util.tiname(filename)
                if opts.name:
                    opts.name = Util.strinc(opts.name)
                file_ = File.create_new(name, fmt, image, console=self.console)
                if opts.asv9t9:
                    result.append((file_.get_as_v9t9(),
                                   Util.to_pc(name).upper() if opts.tinames else Util.to_pc(name).lower() + '.v9t9',
                                   False))
                elif opts.assdd99 is not None:  # could be zero
                    result.append((file_.get_as_sdd99(Util.xint(opts.assdd99)),
                                   Util.to_pc(name).upper() if opts.tinames else Util.to_pc(name).lower() + '.sdd99',
                                   False))
                else:
                    result.append((file_.get_as_tifiles(),
                                   Util.to_pc(name).upper() if opts.tinames else Util.to_pc(name).lower() + '.tfi',
                                   False))
            else:
                if opts.astifiles or opts.assdd99 or File.is_tifiles(image):
                    file_ = File.create_from_tif_image(image, hostfn=filename, console=self.console)
                elif opts.asv9t9 or File.is_v9t9(image):
                    file_ = File.create_from_v9t9_image(image, console=self.console)
                else:
                    raise FileError('Unknown file format')
                if opts.fromfiad:
                    result.append((file_.get_contents(), os.path.splitext(filename)[0], False))
                elif opts.printfiad:
                    result.append((file_.get_contents(), '-', False))
                else:
                    sys.stdout.write(file_.get_info())
        return 0, result


def main(argv, external_data=None):
    import os
    import argparse
    import glob

    class GlobStore(argparse.Action):
        """argparse globbing for Windows platforms"""

        def __call__(self, parser, namespace, values, option_string=None):
            if os.name == 'nt':
                names = [glob.glob(fn) if '*' in fn or '?' in fn else [fn] for fn in values]
                values = [f for n in names for f in n]
            setattr(namespace, self.dest, values)

    args = argparse.ArgumentParser(description='xdm99: Disk image manager and file conversion tool, v' + VERSION)
    args.add_argument('filename', nargs='?', type=str, help='disk image name or filename')
    cmd = args.add_mutually_exclusive_group()

    # disk image commands
    cmd.add_argument('-i', '--info', action='store_true', dest='info',
                     help='show image infomation')
    cmd.add_argument('-p', '--print', dest='print_', nargs='+', metavar='<name>',
                     help='print file from image')
    cmd.add_argument('-e', '--extract', dest='extract', nargs='+', metavar='<name>',
                     help='extract files from image')
    cmd.add_argument('-a', '--add', action=GlobStore, dest='add', nargs='+',
                     metavar='<file>', help='add files to image or update existing files')
    cmd.add_argument('-r', '--rename', dest='rename', nargs='+', metavar='<old>:<new>',
                     help='rename files on image')
    cmd.add_argument('-d', '--delete', dest='delete', nargs='+', metavar='<name>',
                     help='delete files from image')
    cmd.add_argument('-w', '--protect', dest='protect', nargs='+', metavar='<name>',
                     help='toggle write protection of files on image')
    cmd.add_argument('-c', '--encoding', dest='encoding', nargs='?', const='utf-8', metavar='<encoding>',
                     help='set encoding for DISPLAY files')
    cmd.add_argument('-Z', '--resize', dest='resize', metavar='<sectors>',
                     help='resize image to given total sector count')
    cmd.add_argument('--set-geometry', dest='geometry', metavar='<geometry>',
                     help='set disk geometry (xSxDxT)')
    cmd.add_argument('-C', '--check', action='store_true', dest='checkonly',
                     help='check disk image integrity only')
    cmd.add_argument('-R', '--repair', action='store_true', dest='repair',
                     help='attempt to repair disk image')
    cmd.add_argument('-S', '--sector', dest='sector', metavar='<sector>',
                     help='dump disk sector')

    # file commands
    cmd.add_argument('-P', '--print-fiad', action=GlobStore, dest='printfiad', nargs='+',
                     metavar='<file>', help='print contents of file in FIAD format')
    cmd.add_argument('-T', '--to-fiad', action=GlobStore, dest='tofiad', nargs='+',
                     metavar='<file>', help='convert plain file to FIAD format')
    cmd.add_argument('-F', '--from-fiad', action=GlobStore, dest='fromfiad', nargs='+',
                     metavar='<file>', help='convert FIAD format to plain file')
    cmd.add_argument('-I', '--info-fiad', action=GlobStore, dest='infofiad', nargs='+',
                     metavar='<file>', help='show information about file in FIAD format')

    # general options
    # args.add_argument('-D', '--deark', dest='deark', nargs='*',
    #                   metavar='<archive>', help='decompress ARK archive')
    # args.add_argument('-A', '--ark', dest='ark', nargs='*',
    #                   metavar='<file>', help='compress into ARK archive')
    args.add_argument('-t', '--tifiles', action='store_true', dest='astifiles',
                      help='use TIFILES file format')
    args.add_argument('-N', '--ti-names', action='store_true', dest='tinames',
                      help='use TI filenames for resulting files')
    args.add_argument('-9', '--v9t9', action='store_true', dest='asv9t9',
                      help='use v9t9 file format')
    args.add_argument('--sdd', dest='assdd99', nargs='?', const='0', metavar='<loadtype>',
                      help='use SDD 99 file format, with given loadtype')
    args.add_argument('-f', '--format', dest='format', metavar='<format>',
                      help='set TI file format (DIS/VARxx, DIS/FIXxx, INT/VARxx, INT/FIXxx, PROGRAM) for data to add')
    args.add_argument('-n', '--name', dest='name', metavar='<name>',
                      help='set TI filename for data to add')
    args.add_argument('-X', '--initialize', dest='init', metavar='<size>',
                      help='initialize disk image (sector count or disk geometry xSxDxT)')
    args.add_argument('-o', '--output', dest='output', metavar='<file>',
                      help='set output filename or target directory')
    args.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                      help='suppress all warnings')
    args.add_argument('--color', action='store', dest='color', choices=['off', 'on'],
                      help='enable or disable color output')

    try:
        default_opts = os.environ[CONFIG].split()
    except KeyError:
        default_opts = []
    opts = args.parse_args(args=default_opts + sys.argv[1:])  # passed opts override default opts

    console = Console(disable_warnings=opts.quiet, colors=opts.color)
    process = Processor(console)

    # process image
    try:
        if opts.fromfiad or opts.tofiad or opts.printfiad or opts.infofiad:
            rc, result = process.process_file_command(opts)
        else:
            if not opts.filename:
                args.error('Missing disk image')
            rc, result = process.process_image_command(opts, external_data)
    except (IOError, DiskError, FileError) as e:
        # note that some generators haven't been evaluated yet!
        sys.exit(console.color('Error: ' + str(e), severity=Console.ERROR))

    # show error and warning messages
    console.print()

    # process result
    if external_data:
        return result  # might throw exception when evaluated!

    # write result
    if opts.output and os.path.isdir(opts.output):  # -o file or directory?
        path = opts.output
        barename = os.path.basename
        opts.output = None
    else:
        path = ''
        barename = Util.id_function

    try:
        for data, name, _is_disk in result:  # _is_disk used by xvm, xhm
            outname = os.path.join(path, opts.output or barename(name))
            Util.writedata(outname, data, encoding=opts.encoding)
    except (IOError, DiskError, FileError) as e:
        sys.exit(console.color('Error: ' + str(e), severity=Console.ERROR))

    # return status
    return rc


if __name__ == '__main__':
    status = main(sys.argv[1:])
    sys.exit(status)
