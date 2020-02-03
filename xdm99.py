#!/usr/bin/env python

# xdm99: A disk manager for TI disk images
#
# Copyright (c) 2015-2020 Ralph Benzinger <xdt99@endlos.net>
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


VERSION = '3.0.0'


# Utility functions

def ordw(word):
    """word ord"""
    return word[0] << 8 | word[1]


def ordwR(word):
    """reverse word ord"""
    return word[1] << 8 | word[0]


def chrw(word):
    """word chr"""
    return bytes((word >> 8, word & 0xff))


def bval(bytes_):
    """n-length ord"""
    return [b for b in bytes_]


def pad(n, m):
    """return increment to next multiple of m"""
    return -n % m


def used(n, m):
    """integer division rounding up"""
    return (n + m - 1) // m


def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip('>'), 16 if s[:2] == '0x' or s[:1] == '>' else 10)


def tiname(s):
    """create TI filename from local filename"""
    return to_ti(os.path.splitext(os.path.basename(s))[0][:10].upper())


def to_pc(n):
    """escaoe TI filename for PC"""
    return None if n is None else n.replace('/', '.')


def to_ti(n):
    """escape PC name for TI"""
    return None if n is None else n.replace('.', '/')


def sseq(s, i):
    """create string sequence"""
    return s[:-1] + chr(ord(s[-1]) + i)


def chop(s, n):
    """generator that produces n-sized parts of s"""
    while True:
        part, s = s[:n], s[n:]
        if not part:
            break
        yield part

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

    def __init__(self, image):
        if len(image) < 2 * Disk.BYTES_PER_SECTOR:
            raise DiskError('Invalid disk image')
        self.image = image
        self.read_sectors = []
        self.warnings = {}
        # meta data
        sector_0 = self.get_sector(0)
        if sector_0[0] == 0x00 and sector_0[21:23] == b'\x00\xfe':
            raise DiskError('Track dump images not supported')
        try:
            self.name = sector_0[:0x0a].decode()
        except UnicodeDecodeError:
            self.name = 'INVALID   '
            self.warn('Disk name contains invalid Unicode', 'image')
        self.total_sectors = ordw(sector_0[0x0a:0x0c])
        self.sectors_per_track = sector_0[0x0c]
        self.dsk_id = sector_0[0x0d:0x10]
        self.protected = sector_0[0x10]  # int, not boolean
        self.tracks_per_side = sector_0[0x11]
        self.sides = sector_0[0x12]
        self.density = sector_0[0x13]
        self.alloc_bitmap = sector_0[0x38:]
        # derived values and sanity checks
        if self.dsk_id != b'DSK':
            self.warn('Disk image not initialized', 'image')
        if len(self.image) < self.total_sectors * Disk.BYTES_PER_SECTOR:
            self.warn('Disk image truncated', 'image')
        self.check_geometry()
        self.used_sectors = 0
        try:
            for i in range(used(self.total_sectors, 8)):
                self.used_sectors += bin(self.alloc_bitmap[i]).count('1')
        except IndexError:
            self.warn('Allocation map corrupted', 'allocation')
        self.catalog = {}
        self.init_catalog()
        self.check_allocation()

    def check_geometry(self):
        """check geometry against sector count"""
        if self.total_sectors != self.sides * self.tracks_per_side * self.sectors_per_track:
            self.warn('Sector count does not match disk geometry', 'geometry')
        if self.total_sectors % 8 != 0:
            self.warn('Sector count is not multiple of 8', 'geometry')

    def rename(self, name):
        """rename disk"""
        self.name = name
        if len(self.name.encode()) > 10:
            raise DiskError('Encoded name is too long')
        self.image = self.name.encode() + b' ' * (10 - len(self.name)) + self.image[0x0a:]

    def init_catalog(self):
        """read all files from disk"""
        sector_1 = self.get_sector(1)
        sector_count = 0
        for i in range(0, Disk.BYTES_PER_SECTOR, 2):
            # get file descriptor
            fd_index = ordw(sector_1[i:i + 2])
            if fd_index == 0:
                break
            try:
                fd_sector = self.get_sector(fd_index, b'FDR#%d' % fd_index)
            except IndexError:
                self.warn('File descriptor index corrupted')
                continue
            fd = FileDescriptor().from_fdr_sector(fd_sector)
            # get file contents
            data, error = self.read_file(fd.name, fd.total_sectors, fd.clusters)
            if error:
                fd.error = True
            self.catalog[fd.name] = File(fd=fd, data=data)
            sector_count += fd.total_sectors + 1
        # consistency check
        if sector_count != self.used_sectors - 2:
            self.warn('Used sector mismatch: found {} file sectors, expected {}'.format(
                    sector_count, self.used_sectors - 2))

    def read_file(self, name, sectors, clusters):
        """read file contents based on FDR cluster data"""
        parts = []
        offset = -1
        error = False
        for i in range(0, len(clusters) - 2, 3):
            start = clusters[i] | (clusters[i + 1] & 0x0f) << 8
            if start == 0:
                break
            prev_offset = offset
            offset = clusters[i + 1] >> 4 | clusters[i + 2] << 4
            for j in range(offset - prev_offset):
                try:
                    parts.append(self.get_sector(start + j, name))
                except IndexError:
                    self.warn(f'{name:s}: File contents corrupted')
                    error = True
                    continue
        data = b''.join(parts)
        if len(data) != sectors * Disk.BYTES_PER_SECTOR:
            self.warn('{}: File size mismatch: found {} bytes, expected {}'.format(
                name, len(data), sectors * Disk.BYTES_PER_SECTOR))
            error = True
        return data, error

    def glob_files(self, patterns):
        """return listing of filenames matching glob pattern"""
        wildcards = [pattern for pattern in patterns if re.search('[?*]', pattern)]
        glob_re = '|'.join(re.escape(p).replace(r'\*', '.*').replace(r'\?', '.')
                           for p in wildcards) + '$'
        matches = [name for name in self.catalog if re.match(glob_re, name)]
        plains = [pattern for pattern in patterns if pattern not in wildcards]
        return matches + plains

    def rebuild_disk(self):
        """rebuild disk metadata after changes to file catalog"""
        required_sectors = sum(self.catalog[n].fd.total_sectors for n in self.catalog)
        # preferred start at sector >22
        first_free = next_free = min(max(2 + len(self.catalog), 0x22), self.total_sectors - required_sectors)
        if first_free < 2 + len(self.catalog):
            raise DiskError('Disk full, lacking {} sectors'.format(2 + len(self.catalog) - first_free))
        sector_1 = b''
        index = 2
        for idx, file_ in sorted(self.catalog.items()):
            # put file data into single cluster
            data = file_.data
            for i in range(file_.fd.total_sectors):
                self.set_sector(next_free + i, data[Disk.BYTES_PER_SECTOR * i:Disk.BYTES_PER_SECTOR * (i + 1)])
            # build file descriptor
            if file_.fd.total_sectors > 0:
                start = next_free
                offset = file_.fd.total_sectors - 1
            else:
                start = offset = 0
            file_.fd.clusters = (bytes((start & 0xff, start >> 8 | (offset & 0xf) << 4, offset >> 4)) +
                                 bytes(Disk.BYTES_PER_SECTOR - 0x1c - 3))
            self.set_sector(index, file_.fd.get_image())
            # update FDR index in sector 1
            sector_1 += chrw(index)
            next_free += file_.fd.total_sectors
            index += 1
        sector_1 += bytes(Disk.BYTES_PER_SECTOR - len(sector_1))
        self.set_sector(1, sector_1)
        # update allocation bitmap in sector 0 (used: 0..i-1, ff..nf-1)
        assert 0 < index <= first_free <= next_free
        mask = int('1' * (next_free - first_free) +
                   '0' * (first_free - index) + '1' * index, 2)  # bitmap as bits, parsed into (very large) int
        bytes_ = []
        for i in range(self.total_sectors // 8):
            bytes_.append(bytes((mask & 0xff,)))  # byte-ize int from the tail
            mask >>= 8
        self.alloc_bitmap = b''.join(bytes_) + b'\xff' * (Disk.BYTES_PER_SECTOR - 0x38 - len(bytes_))
        sector_0 = self.get_sector(0)
        self.set_sector(0, sector_0[:0x38] + self.alloc_bitmap)

    @staticmethod
    def extend_sectors(image, new_size):
        """increase total number of sectors and clear alloc map (for xvm99)"""
        current = ordw(image[0x0a:0x0c])
        if not current <= new_size <= Disk.MAX_SECTORS:
            raise DiskError(f'Invalid size {new_size:d} for sector increase')
        if current % 8 != 0:
            raise DiskError('Sector count must be multiple of 8')
        bitmap = image[0x38:0x38 + current // 8] + b'\xff' * (Disk.BYTES_PER_SECTOR - 0x38 - current // 8)
        return image[:0x0a] + chrw(new_size) + image[0x0c:0x38] + bitmap + image[0x100:]

    @staticmethod
    def trim_sectors(image):
        """shrink image to actually existing sectors"""
        total_sectors = ordw(image[0x0a:0x0c])
        return image[:total_sectors * Disk.BYTES_PER_SECTOR]

    def get_sector(self, sector_no, context=None):
        """retrieve sector from image"""
        if sector_no > 0 and sector_no >= self.total_sectors:
            if sector_no < len(self.image) // Disk.BYTES_PER_SECTOR:
                self.warn('Total sectors not set properly')
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
        for i in range(used(self.total_sectors, 8)):
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
                self.warn(f'{context}: Used sector {sector_no} not allocated')
                file_ = self.catalog.get(context)
                if file_:
                    file_.fd.error = True
        # sectors allocated to multiple files
        for sector_no, files in reads.items():
            if len(files) <= 1:
                continue
            self.warn(f"Sector {sector_no} claimed by multiple files: {'/'.join(files)}")
            for name in files:
                file_ = self.catalog.get(name)
                if file_:
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
        self.image = (self.image[:0x0a] + chrw(new_size) +
                      self.image[0x0c:new_size * self.BYTES_PER_SECTOR] +
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
        self.image = (self.image[:0x0c] + bytes((self.sectors_per_track,)) +
                      self.image[0x0d:0x11] + bytes((self.tracks_per_side, self.sides, self.density)) +
                      self.image[0x14:])
        self.clear_warnings('geometry')
        self.check_geometry()

    def fix_disk(self):
        """rebuild disk with non-erroneous files"""
        for name, file_ in self.catalog.items():
            if file_.fd.error:
                del self.catalog[name]
        self.rebuild_disk()

    def get_tifiles_file(self, name):
        """get file in TIFiles format from disk catalog"""
        file_ = self.get_file(name)
        return file_.get_as_tifiles()

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
        sectors, layout = Disk.parse_geometry(geometry)
        if layout:
            sides, density, tracks = layout
        else:
            sides = 2 if 360 <= (sectors - 1) % 720 else 1
            density = 2 if 720 < sectors <= 1440 else 1  # favor DSSD over SSDD
            tracks = Disk.DEFAULT_TRACKS
        if not 2 < sectors <= Disk.MAX_SECTORS or sectors % 8 != 0 or not (sides and density):
            raise DiskError('Invalid disk size')
        sector_0 = (b'%-10b%2b%cDSK ' % (name.encode()[:10],
                                         chrw(sectors),
                                         Disk.DEFAULT_SECTORS_PER_TRACK * density) +  # header
                    bytes((tracks or Disk.DEFAULT_TRACKS, sides, density)) +
                    bytes(0x24) +  # reserved
                    b'\x03' + bytes(sectors // 8 - 1) +  # allocation map
                    b'\xff' * (Disk.BYTES_PER_SECTOR - sectors // 8 - 0x38))
        return (sector_0 +
                bytes(Disk.BYTES_PER_SECTOR) +  # blank sector 1
                Disk.BLANK_BYTE * ((sectors - 2) * Disk.BYTES_PER_SECTOR))  # sectors 2 and up

    @staticmethod
    def parse_geometry(geometry):
        """get disk size and layout from geometry string"""
        if geometry.upper() == 'CF':
            return 1600, (1, 1, Disk.DEFAULT_TRACKS)
        try:
            sectors = xint(geometry)
            return sectors, None
        except ValueError:
            pass
        sides = density = tracks = None
        parse = lambda s: 1 if s == 'S' else 2 if s == 'D' else int(s)
        geometry_parts = re.split(r'(\d+|[SD])([SDT])', geometry.upper())
        if ''.join(geometry_parts[::3]) not in ('', '/'):
            raise DiskError('Invalid disk geometry ' + geometry)
        try:
            for val, part in zip(geometry_parts[1::3], geometry_parts[2::3]):
                if part == 'S' and sides is None:
                    sides = parse(val)
                elif part == 'D' and density is None:
                    density = parse(val)
                elif part == 'T' and tracks is None:
                    tracks = parse(val)
                else:
                    raise DiskError('Invalid disk geometry: ' + geometry)
        except (IndexError, ValueError):
            raise DiskError('Invalid disk geometry: ' + geometry)
        try:
            sectors = sides * (tracks or Disk.DEFAULT_TRACKS) * Disk.DEFAULT_SECTORS_PER_TRACK * density
        except TypeError:
            sectors = None
        return sectors, (sides, density, tracks)

    def warn(self, text, category='main'):
        """issue warning; categories are used to delete warnings selectively"""
        if category not in self.warnings:
            self.warnings[category] = []
        if text not in self.warnings[category]:
            self.warnings[category].append(text)

    def clear_warnings(self, category):
        """clear all warnings in given category"""
        try:
            del self.warnings[category]
        except KeyError:
            pass

    def get_warnings(self):
        """return warnings issued while processing disk image"""
        return ''.join(f'Warning: {w}\n'
                       for c in self.warnings.keys()
                       for w in self.warnings[c])


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

    def __init__(self, hostfn=None):
        self.error = False
        self.hostfn = hostfn
        self.name = None
        self.type = None
        self.mode = None
        self.format = None  # display format
        self.flags = None
        self.total_sectors = 0
        self.eof_offset = 0
        self.total_lv3_records = 0
        self.size = 0
        self.actual_records = 0
        self.protected = False
        self.records_per_sector = None
        self.record_len = None
        self.created = None  # time and date
        self.modified = None
        self.clusters = None

    def from_fdr_sector(self, sector):
        """create file descriptor from FDR sector"""
        if len(sector) < 0x20:
            raise FileError('Invalid file descriptor')
        try:
            self.name = sector[:0x0a].decode().rstrip()
        except UnicodeDecodeError:
            raise FileError('Invalid Unicode filename')
        self.flags = sector[0x0c]
        self.records_per_sector = sector[0x0d]
        self.total_sectors = ordw(sector[0x0e:0x10])
        self.eof_offset = sector[0x10]
        self.record_len = sector[0x11]
        self.total_lv3_records = ordwR(sector[0x12:0x14])
        self.created = sector[0x14:0x18]  # time, date
        self.modified = sector[0x18:0x1c]
        self.clusters = sector[0x1c:]
        self.init_fd()
        return self

    def from_tif_header(self, header):
        """create file descriptor from TIFiles header"""
        if len(header) < 0x26 or not File.is_tifiles(header):
            raise FileError('Invalid TIFiles header')
        self.total_sectors = ordw(header[0x08:0x0a])
        self.flags = header[0x0a] & 0x83
        self.records_per_sector = header[0x0b]
        self.eof_offset = header[0x0c]
        self.record_len = header[0x0d]
        self.total_lv3_records = ordwR(header[0x0e:0x10])
        if header[0x10] == 0x00:
            # short TIFiles: use file properties
            self.name = tiname(self.hostfn)
            dt = datetime.datetime.fromtimestamp(os.path.getctime(self.hostfn))
            self.created = self.encode_date(dt)
            dt = datetime.datetime.fromtimestamp(os.path.getmtime(self.hostfn))
            self.modified = self.encode_date(dt)
        else:
            # long TIFiles: use header data
            self.name = header[0x10:0x1a].decode().rstrip()
            self.created = header[0x1e:0x22]
            self.modified = header[0x22:0x26]
        self.init_fd()
        return self

    def new(self, name, format_):
        """create new empty file descriptor"""
        self.name = name
        m_fmt = re.match('([PDIB])[ROGAMISNT]*(?:/?([VF])[ARIX]*\s*(\d+))?', format_.upper())
        if not m_fmt:
            raise FileError('Unknown file format: ' + format_)
        # build flags for specified format
        fmt_type = m_fmt.group(1)
        if fmt_type == 'P':  # P, D, or I
            self.flags = FileDescriptor.PROGRAM
            self.record_len = self.records_per_sector = 0
        else:
            fmt_mode = m_fmt.group(2)  # F or V
            self.flags = ((FileDescriptor.INTERNAL if fmt_type == 'I' else FileDescriptor.DISPLAY) |
                          (FileDescriptor.FIXED if fmt_mode == 'F' else FileDescriptor.VARIABLE))
            fmt_len = m_fmt.group(3)
            self.record_len = int(fmt_len) if fmt_len else 80
            self.records_per_sector = ((Disk.BYTES_PER_SECTOR if fmt_mode == 'F' else Disk.BYTES_PER_SECTOR - 2) //
                                       self.record_len) % Disk.BYTES_PER_SECTOR  # mod for DF1
        self.created = self.modified = self.encode_date(datetime.datetime.now())
        self.init_fd()
        return self

    def init_fd(self):
        """initialize internal data structures"""
        self.type = (FileDescriptor.DISPLAY, FileDescriptor.PROGRAM,
                     FileDescriptor.INTERNAL, FileDescriptor.UNKNOWN)[self.flags & 0x03]
        self.mode = FileDescriptor.VARIABLE if self.flags & 0x80 else FileDescriptor.FIXED
        self.format = ('DIS/', 'PROGRAM', 'INT/', 'unknown')[self.flags & 0x03]
        if self.type in (FileDescriptor.DISPLAY, FileDescriptor.INTERNAL):
            self.format += ('VAR ' if self.mode == FileDescriptor.VARIABLE else 'FIX ') + str(self.record_len)
        self.protected = self.flags & 0x08
        self.size = (self.total_sectors * Disk.BYTES_PER_SECTOR -
                     pad(self.eof_offset, Disk.BYTES_PER_SECTOR))  # excludes FDR

    def toggle_protection(self):
        self.protected = not self.protected
        self.flags ^= FileDescriptor.PROTECTED

    @staticmethod
    def encode_date(dt):
        """convert datetime object into FDR date and time word"""
        date = (dt.year % 100) << 9 | dt.month << 5 | dt.day
        time = dt.hour << 11 | dt.minute << 5 | dt.second // 2
        return chrw(time) + chrw(date)

    @staticmethod
    def decode_date(qword):
        """extract date and time information from header data"""
        time = ordw(qword[0:2])
        date = ordw(qword[2:4])
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

    def get_image(self, v9t9=False):
        """return FDR as disk image sector"""
        return (b'%-10b' % self.name.encode()[:10] +
                bytes((0, 0,
                       self.flags,
                       self.records_per_sector,
                       self.total_sectors >> 8, self.total_sectors & 0xff,
                       self.eof_offset,
                       self.record_len,
                       self.total_lv3_records & 0xff, self.total_lv3_records >> 8,
                       *bval(self.created + self.modified))) +
                (bytes(100) if v9t9 else self.clusters))

    def get_tifiles_header(self):
        """return FDR as TIFiles header"""
        return (b'\x07TIFILES' +
                bytes((self.total_sectors >> 8, self.total_sectors & 0xff,
                       self.flags,
                       self.records_per_sector,
                       self.eof_offset,
                       self.record_len,
                       self.total_lv3_records & 0xff, self.total_lv3_records >> 8)) +
                b'%-10b' % self.name.encode()[:10] +
                bytes((0, 0, 0, 0, *bval(self.created + self.modified), 0xff, 0xff)) +
                b' ' * 88)

    def get_info(self):
        """return information about file"""
        date_str = FileDescriptor.decode_date(self.modified)
        return '{:10s} {:4d}  {:11s} {:6d} B {:>8s}  {:1s}  {:>19s} {:s}  {:1s}\n'.format(
            self.name,
            self.total_sectors + 1,
            self.format,
            self.size,
            '{:3d} recs'.format(self.actual_records) if self.type != FileDescriptor.PROGRAM else '',
            'P' if self.protected else '',
            str(date_str),
            '' if self.modified == self.created == bytes(4) else 'C' if self.modified == self.created else 'M',
            'ERR' if self.error else '')


class File:
    """main file object with FDR metadata and sector contents"""

    def __init__(self, fd=None, data=None):
        self.warnings = []
        self.records = None
        if fd is not None and data is not None:
            self.fd = fd
            self.data = data + bytes(pad(len(data), Disk.BYTES_PER_SECTOR))
            self.records = self.unpack_records()
        else:
            self.fd = self.data = None

    def new(self, name, format_, data, hostfn=None):
        """create plain file"""
        self.fd = FileDescriptor(hostfn=hostfn).new(name=name, format_=format_)
        self.records = self.split_contents(data)
        self.data = self.pack_records()
        return self

    def from_tif_image(self, image, hostfn=None):
        """create FIFILES file"""
        if not File.is_tifiles(image):
            raise FileError('Invalid TIFiles image')
        self.fd = FileDescriptor(hostfn=hostfn).from_tif_header(image[:0x80])
        self.data = image[0x80:] + bytes(pad(len(image) - 0x80, Disk.BYTES_PER_SECTOR))
        self.records = self.unpack_records()
        return self

    def from_v9t9_image(self, image):
        """create v9t9 file"""
        if not File.is_v9t9(image):
            raise FileError('Invalid v9t9 image')
        self.fd = FileDescriptor().from_fdr_sector(image[:0x80])
        self.data = image[0x80:] + bytes(pad(len(image) - 0x80, Disk.BYTES_PER_SECTOR))
        self.records = self.unpack_records()
        return self

    def split_contents(self, data):
        """split blob into records"""
        if self.fd.type == FileDescriptor.PROGRAM:
            return data
        elif self.fd.mode == FileDescriptor.FIXED:
            reclen = self.fd.record_len
            return [data[i:i + reclen] for i in range(0, len(data), reclen)]
        elif self.fd.type == FileDescriptor.DISPLAY:
            return data.splitlines()
        else:
            records = []
            i = 0
            while i < len(data):
                reclen = data[i] + 1
                records.append(data[i + 1:i + reclen])  # remove record length
                i += reclen
            return records

    def unpack_records(self):
        """extract list of records from sector image (-e)"""
        records = []
        if self.fd.type == FileDescriptor.PROGRAM:
            records = self.data[:self.fd.eof_offset - Disk.BYTES_PER_SECTOR] if self.fd.eof_offset else self.data
            self.fd.actual_records = 0
        elif self.fd.mode == FileDescriptor.FIXED:
            records_per_sector = self.fd.records_per_sector or 256
            recno = recs_added_to_sector = sector = 0
            while recno < self.fd.total_lv3_records:
                if recs_added_to_sector >= records_per_sector:
                    sector += 1
                    recs_added_to_sector = 0
                    continue
                idx = sector * Disk.BYTES_PER_SECTOR + recs_added_to_sector * self.fd.record_len
                records.append(self.data[idx:idx + self.fd.record_len])
                recno += 1
                recs_added_to_sector += 1
            self.fd.actual_records = recno
        else:  # VARIABLE
            recno = offset_in_sector = sector = 0
            while sector < self.fd.total_lv3_records:  # == self.total_sectors
                idx = sector * Disk.BYTES_PER_SECTOR + offset_in_sector
                reclen = self.data[idx] if idx < len(self.data) else -1
                if (reclen == 0xff and offset_in_sector > 0) or reclen == -1:
                    sector += 1
                    offset_in_sector = 0
                    continue
                records.append(self.data[idx + 1:idx + 1 + reclen])  # store w/o record length
                recno += 1
                if reclen == 0xff and offset_in_sector == 0:  # DIS/VAR255
                    sector += 1
                else:
                    offset_in_sector += reclen + 1
            self.fd.actual_records = recno
        return records

    def pack_records(self):
        """create sector image from listing of records (-a)"""
        if self.fd.type == FileDescriptor.PROGRAM:
            data = self.records
            self.fd.eof_offset = len(data) % Disk.BYTES_PER_SECTOR
            self.fd.total_sectors = used(len(data), Disk.BYTES_PER_SECTOR)
            self.fd.total_lv3_records = 0
        elif self.fd.mode == FileDescriptor.FIXED:
            parts = []
            recno = sectors = offset_in_sector = 0
            for record in self.records:
                if len(record) > self.fd.record_len:
                    self.warn(f'Record #{recno} too long, truncating {len(record) - self.fd.record_len} bytes')
                    record = record[:self.fd.record_len]
                if offset_in_sector + self.fd.record_len > Disk.BYTES_PER_SECTOR:
                    parts.append(bytes(Disk.BYTES_PER_SECTOR - offset_in_sector))
                    sectors += 1
                    offset_in_sector = 0
                padlen = self.fd.record_len - len(record)
                parts.append(record + (bytes(padlen) if self.fd.type == FileDescriptor.INTERNAL else b' ' * padlen))
                offset_in_sector += self.fd.record_len
                recno += 1
            data = b''.join(parts)
            self.fd.eof_offset = offset_in_sector % Disk.BYTES_PER_SECTOR
            self.fd.total_sectors = sectors + 1
            self.fd.total_lv3_records = recno
        else:  # VARIABLE
            parts = []
            recno = 1
            sectors = offset_in_sector = 0
            for record in self.records:
                if len(record) > self.fd.record_len:
                    self.warn(f'Record #{recno} too long, truncating {len(record) - self.fd.record_len} bytes')
                    record = record[:self.fd.record_len]
                if offset_in_sector + 1 + len(record) + 1 > Disk.BYTES_PER_SECTOR and offset_in_sector > 0:
                    parts.append(b'\xff' + bytes(Disk.BYTES_PER_SECTOR - offset_in_sector - 1))
                    sectors += 1
                    offset_in_sector = 0
                parts.append(bytes((len(record),)) + record)
                recno += 1
                if len(record) == Disk.BYTES_PER_SECTOR - 1:  # VAR255
                    sectors += 1
                    offset_in_sector = 0
                else:
                    offset_in_sector += len(record) + 1
            if offset_in_sector > 0:
                parts.append(b'\xff')  # EOF marker
                sectors += 1
            data = b''.join(parts)
            self.fd.eof_offset = offset_in_sector
            self.fd.total_sectors = self.fd.total_lv3_records = sectors  # by fiat
        return data + bytes(pad(len(data), Disk.BYTES_PER_SECTOR))

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
        """return file contents in TIFiles format"""
        return self.fd.get_tifiles_header() + self.data

    def get_as_v9t9(self):
        """return file contents in v9t9 format"""
        return self.fd.get_image(v9t9=True) + self.data

    @staticmethod
    def is_tifiles(image):
        """check if file image has valid TIFiles header"""
        return image[:8] == b'\x07TIFILES'

    @staticmethod
    def is_v9t9(image):
        """check if file image has v9t9 header"""
        return all(32 <= c < 127 for c in image[:10]) and image[0x30:0x80] == bytes(0x50)

    def get_info(self):
        """return file meta data"""
        return self.fd.get_info()

    def warn(self, text):
        """issue non-critical warning"""
        if text not in self.warnings:
            self.warnings.append(text)

    def get_warnings(self):
        """return warnings issued while processing file"""
        return ''.join(f'Warning: {w:s}\n' for w in self.warnings)


# Command line processing

def dump(s):
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


def image_cmds(opts, external_data=None):
    """disk image manipulation"""
    rc = 0
    result = []  # data x filename x is disk?
    format_ = opts.format.upper() if opts.format else 'PROGRAM'

    # get disk image
    if opts.init:
        barename = os.path.splitext(os.path.basename(opts.filename))[0]
        image = Disk.blank_image(opts.init, to_ti(opts.name) or barename[:10].upper())
        result = (image, opts.filename, True),
    else:
        image = external_data or readdata(opts.filename)
    disk = Disk(image)

    # apply command to image
    if opts.print_:
        files = disk.glob_files(opts.print_)
        contents = (disk.get_file(name).get_contents() for name in files)
        sys.stdout.buffer.write(b''.join(contents))
    elif opts.extract:
        files = disk.glob_files(opts.extract)
        if opts.output and len(files) > 1 and not os.path.isdir(opts.output):
            sys.exit('Error: -o must provide directory when extracting multiple files')
        if opts.astifiles:
            result = ((disk.get_tifiles_file(name),
                       to_pc(name).upper() if opts.tinames else to_pc(name).lower() + '.tfi',
                       False)
                      for name in files)
        elif opts.asv9t9:
            result = ((disk.get_v9t9_file(name),
                       to_pc(name).upper() if opts.tinames else to_pc(name).lower() + '.v9t9',
                       False)
                      for name in files)
        else:
            files = ((to_pc(name), disk.get_file(name)) for name in files)
            result = ((file_.get_contents(),
                       name.upper() if opts.tinames else name.lower(),
                       False)
                      for name, file_ in files)
    elif opts.add:
        seq_no = 0
        for name in opts.add:
            data = readdata(name, encoding=opts.encoding)
            if name == '-':
                name = 'STDIN'
            if opts.astifiles:
                disk.add_file(File().from_tif_image(data, hostfn=name))
            elif opts.asv9t9:
                disk.add_file(File().from_v9t9_image(data))
            else:
                name = sseq(to_ti(opts.name), seq_no) if opts.name else tiname(name)
                file_ = File().new(name, format_, data)
                seq_no += 1
                if file_.warnings and not opts.quiet:
                    sys.stderr.write(file_.get_warnings())
                disk.add_file(file_)
        result = (disk.image, opts.filename, True),
    elif opts.rename:
        names = [to_ti(arg).split(':') for arg in opts.rename]
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
        size, layout = Disk.parse_geometry(opts.resize)
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
        rc = 1 if disk.warnings else 0
    elif opts.repair:
        disk.fix_disk()
        result = (disk.image, opts.filename, True),
    elif opts.sector:
        opts.quiet = True
        try:
            sector_no = xint(opts.sector)
            sector = disk.get_sector(sector_no)
        except (IndexError, ValueError):
            raise DiskError(f'Invalid sector: {opts.sector}')
        result = (dump(sector), '-', False),
    elif opts.name and not opts.init:
        # at this point, '-n' is supplied without command, so rename disk
        disk.rename(to_ti(opts.name))
        result = (disk.image, opts.filename, True),
    elif opts.info or not opts.init:
        sys.stdout.write(disk.get_info())
        sys.stdout.write('-' * 76 + '\n')
        sys.stdout.write(disk.get_catalog())
    if not opts.quiet:
        sys.stderr.write(disk.get_warnings())
    return rc, result


def file_cmds(opts):
    """file manipulation"""
    rc = 0
    result = []
    # files to process (opts are mutually exclusive)
    files = opts.fromfiad or opts.tofiad or opts.printfiad or opts.infofiad
    if opts.output and len(files) > 1 and not os.path.isdir(opts.output):
        sys.exit('Error: -o must provide directory when providing multiple files')
    fmt = opts.format.upper() if opts.format else 'PROGRAM'

    for idx, filename in enumerate(files):
        image = readdata(filename)
        if opts.tofiad:
            name = sseq(to_ti(opts.name), idx) if opts.name else tiname(filename)
            file_ = File().new(name, fmt, image)
            if opts.asv9t9:
                result.append((file_.get_as_v9t9(), filename + '.v9t9', False))
            else:
                result.append((file_.get_as_tifiles(), filename + '.tfi', False))
        else:
            if opts.astifiles or File.is_tifiles(image):
                file_ = File().from_tif_image(image, hostfn=filename)
            elif opts.asv9t9 or File.is_v9t9(image):
                file_ = File().from_v9t9_image(image)
            else:
                raise FileError('Unknown file format')
            if opts.fromfiad:
                result.append((file_.get_contents(), os.path.splitext(filename)[0], False))
            elif opts.printfiad:
                result.append((file_.get_contents(), '-', False))
            else:
                sys.stdout.write(file_.get_info())
    return rc, result


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
                      help='use TIFiles file format for added/extracted files')
    args.add_argument('-N', '--ti-names', action='store_true', dest='tinames',
                      help='use TI filenames for resulting files')
    args.add_argument('-9', '--v9t9', action='store_true', dest='asv9t9',
                      help='use v9t9 file format for added/extracted files')
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
    opts = args.parse_args(argv)

    # process image
    try:
        if opts.fromfiad or opts.tofiad or opts.printfiad or opts.infofiad:
            rc, result = file_cmds(opts)
        else:
            if not opts.filename:
                args.error('Missing disk image')
            rc, result = image_cmds(opts, external_data)
    except (IOError, DiskError, FileError) as e:
        # note that some generators haven't been evaluated yet!
        sys.exit('Error: ' + str(e))

    # process result
    if external_data:
        return result  # might throw exception when evaluated!

    # write result
    if opts.output and os.path.isdir(opts.output):  # -o file or directory?
        path = opts.output
        opts.output = None
    else:
        path = ''

    try:
        for data, name, _ in result:
            outname = os.path.join(path, opts.output or name)
            writedata(outname, data, encoding=opts.encoding)
    except (IOError, DiskError, FileError) as e:
        sys.exit('Error: ' + str(e))

    # return status
    return rc


if __name__ == '__main__':
    status = main(sys.argv[1:])
    sys.exit(status)