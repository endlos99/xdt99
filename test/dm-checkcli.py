#!/usr/bin/env python3

import os
import shutil

from config import Dirs, Disks, Files, Masks, XDM99_CONFIG
from utils import r, t, xdm, error, delfile, check_files_eq, check_file_matches, check_file_exists, content


# Check functions

def check_file_len(infile, min_lines=-1, max_lines=99999):
    """check if text file has certain length"""
    try:
        with open(infile, 'r') as f:
            line_count = len(f.readlines())
    except IOError:
        line_count = 0
    if not min_lines <= line_count <= max_lines:
        error('CLI',
              f'{infile}: Line count mismatch: found {line_count} lines, expected {min_lines} to {max_lines}')


def check_file_size(infile, size):
    """check if file has certain size"""
    statinfo = os.stat(infile)
    if statinfo.st_size != size:
        error('CLI',
              f'{infile}: File size mismatch: found {statinfo.st_size} bytes, expected {size}')


def check_disks_eq(disk, ref):
    """check if disk metadata (sectors 0 and 1) are equal"""
    with open(disk, 'rb') as f:
        dat = f.read(512)
    with open(ref, 'rb') as f:
        ref = f.read(512)
    if dat != ref:
        error('CLI', 'Disk metadata mismatch')


def check_lines_start(reffile, starts, skip=0):
    with open(reffile, 'r') as fin:
        lines = fin.readlines()[skip:]
    for text in starts:
        if all([line[:len(text)] != text for line in lines]):
            error('line text', f"Text '{text}' could not be found")


# Main test

def runtest():
    """check command line interface"""

    os.environ[XDM99_CONFIG] = '--color off'

    # setup
    shutil.copyfile(Disks.recsgen, Disks.work)

    # disk image operations
    with open(Files.output, 'w') as f1, open(Files.reference, 'w') as f2:
        xdm(Disks.work, '-i', stdout=f2)
        xdm(Disks.work, '-q', stdout=f1)
    check_files_eq('CLI', Files.output, Files.reference, 'DIS/VAR255')

    ref_prog = r('prog00255')
    xdm(Disks.work, '-e', 'PROG00255', '-o', Files.output)
    check_files_eq('CLI', Files.output, ref_prog, 'PROGRAM')
    ref_dv = r('dv064x010')
    xdm(Disks.work, '-e', 'DV064X010', '-o', Files.output)
    check_files_eq('CLI', Files.output, ref_dv, 'DIS/VAR64')
    ref_df = r('df002x001')
    xdm(Disks.work, '-e', 'DF002X001', '-o', Files.output)
    check_files_eq('CLI', Files.output, ref_df, 'DIS/FIX 2')

    with open(Files.output, 'w') as f1:
        xdm(Disks.work, '-p', 'DV064X010', stdout=f1)
    check_files_eq('CLI', Files.output, ref_dv, 'DIS/VAR 64')

    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-e', 'INVALID', stderr=ferr, rc=1)

    xdm(Disks.work, '-S', '0x01', '-o', Files.output)
    check_files_eq('CLI', Files.output, os.path.join(Dirs.refs, 'sector1'), 'DIS/VAR255')

    # add, rename, remove files
    shutil.copyfile(Disks.blank, Disks.work)
    xdm(Disks.work, '-a', ref_prog, ref_dv, ref_df)
    xdm(Disks.work, '-e', 'PROG00255', '-o', Files.output)
    check_files_eq('CLI', Files.output, ref_prog, 'PROGRAM')
    xdm(Disks.work, '-e', 'DV064X010', '-o', Files.output)
    check_files_eq('CLI', Files.output, ref_dv, 'PROGRAM')  # use PROGRAM here to compare!

    shutil.copyfile(Disks.work, Disks.tifiles)
    xdm(Disks.work, '-e', 'PROG00255', '-o', Files.reference)
    xdm(Disks.work, '-r', 'PROG00255:OTHERNAME')
    xdm(Disks.work, '-e', 'OTHERNAME', '-o', Files.output)
    check_files_eq('CLI', Files.output, Files.reference, 'P')
    xdm(Disks.work, '-r', 'OTHERNAME:PROG00255')
    check_files_eq('CLI', Disks.work, Disks.tifiles, 'P')

    xdm(Disks.work, '-d', 'PROG00255', 'DV064X010', 'DF002X001')
    with open(Files.output, 'w') as f1, open(Files.reference, 'w') as f2:
        xdm(Disks.work, '-i', stdout=f1)
        xdm(Disks.blank, '-i', stdout=f2)
    check_files_eq('CLI', Files.output, Files.reference, 'DIS/VAR255')

    shutil.copyfile(Disks.recsgen, Disks.work)
    xdm(Disks.work, '-e', 'DF127*', 'PROG00001', 'PROG00002')
    if (not os.path.isfile('df127x001') or not os.path.isfile('df127x010') or
            not os.path.isfile('df127x020p')):
        error('CLI', 'DF127*: Missing files')

    xdm(Disks.work, '-d', 'PROG*', 'D?010X060')
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-e', 'PROG00255', stderr=ferr, rc=1)
        xdm(Disks.work, '-e', 'DV010X060', stderr=ferr, rc=1)
        xdm(Disks.work, '-e', 'DF010X060', stderr=ferr, rc=1)

    # multi-file naming
    xdm(Disks.work, '-n', 'MULTI', '-a', 'prog00001', ref_prog, 'prog00002')
    xdm(Disks.work, '-e', 'MULTI', '-o', Files.output)
    check_files_eq('CLI', 'prog00001', Files.output, 'P')
    xdm(Disks.work, '-e', 'MULTJ', '-o', Files.output)
    check_files_eq('CLI', ref_prog, Files.output, 'P')
    xdm(Disks.work, '-e', 'MULTK', '-o', Files.output)
    check_files_eq('CLI', 'prog00002', Files.output, 'P')

    xdm('-T', 'prog00001', ref_prog, 'prog00002', '-n', 'MULTFI')  # -n applies to internal name and filename!
    xdm(Disks.work, '-t', '-a', 'multfi.tfi', 'multfj.tfi', 'multfk.tfi')
    xdm(Disks.work, '-e', 'MULTFI', '-o', Files.output)
    check_files_eq('CLI', 'prog00001', Files.output, 'P')
    xdm(Disks.work, '-e', 'MULTFJ', '-o', Files.output)
    check_files_eq('CLI', ref_prog, Files.output, 'P')
    xdm(Disks.work, '-e', 'MULTFK', '-o', Files.output)
    check_files_eq('CLI', 'prog00002', Files.output, 'P')

    xdm('-T', ref_prog, 'prog00002', '-9', '-n', 'MULV9T')
    xdm(Disks.work, '-9', '-a', 'mulv9t.v9t9', 'mulv9u.v9t9')
    xdm(Disks.work, '-e', 'MULV9T', '-o', Files.output)
    check_files_eq('CLI', ref_prog, Files.output, 'P')
    xdm(Disks.work, '-e', 'MULV9U', '-o', Files.output)
    check_files_eq('CLI', 'prog00002', Files.output, 'P')

    ref = r('glob')
    xdm(Disks.work, '-a', ref + '?', '-n', 'GLOBA1', shell=True)
    xdm(Disks.work, '-e', 'GLOBA1', '-o', Files.output)
    xdm(Disks.work, '-e', 'GLOBA2', '-o', Files.output)
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-e', 'GLOBA3', '-o', Files.output, stderr=ferr, rc=1)
    xdm(Disks.work, '-d', 'GLOB*', '-o', Files.output)
    xdm(Disks.work, '-a', ref + '*', '-n', 'GLOBB1', shell=True)
    xdm(Disks.work, '-e', 'GLOBB1', '-o', Files.output)
    xdm(Disks.work, '-e', 'GLOBB2', '-o', Files.output)
    xdm(Disks.work, '-e', 'GLOBB3', '-o', Files.output)

    # initialize disk
    xdm(Disks.work, '--initialize', '360', '-n', 'SSSD')
    check_file_size(Disks.work, 360 * 256)
    check_files_eq('CLI', Disks.work, Disks.blank, 'P')
    os.remove(Disks.work)
    xdm(Disks.work, '--initialize', 'SSSD', '-n', 'SSSD')
    check_file_size(Disks.work, 360 * 256)
    check_files_eq('CLI', Disks.work, Disks.blank, 'P')
    xdm(Disks.work, '--initialize', '800', '-n', 'INIT', '-q')
    with open(Files.output, 'w') as f:
        xdm(Disks.work, '-i', '-q', stdout=f)
    check_file_matches(Files.output, [(0, r'\s2\s+used\s+798\s+free\s')])
    os.remove(Disks.work)
    xdm(Disks.work, '--initialize', 'CF', '-n', 'INIT', '-q')
    with open(Files.output, 'w') as f:
        xdm(Disks.work, '-i', '-q', stdout=f)
    check_file_matches(Files.output, [(0, r'\s2\s+used\s+1598\s+free\s')])
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '--initialize', '1', stderr=ferr, rc=1)
        xdm(Disks.work, '--initialize', '1601', stderr=ferr, rc=1)
        xdm(Disks.work, '--initialize', 'FOO', stderr=ferr, rc=1)
    f = os.path.join(Dirs.refs, 'vardis')
    for n in ['AA', 'BB']:
        xdm(Disks.work, '--initialize', 'SSSD', '-a', f, '-n', n)
        with open(Files.output, 'w') as fout:
            xdm(Disks.work, '-i', stdout=fout)
        check_file_matches(Files.output, [(0, n + r'\s+'), (2, n + r'\s+')])

    # set geometry
    xdm(Disks.work, '--initialize', '1600', '-n', 'GEO', '-q')
    for g, p in [('1S1D', r'1S/1D\s+40T'), ('99T8D7S', r'7S/8D\s+99T'),
                 ('22TDD', r'7S/2D\s+22T'), ('DSSD', r'2S/1D\s+22T'),
                 ('1T', r'2S/1D\s+1T'), ('3D10T9S', r'9S/3D\s+10T'),
                 ('SDDS', r'2S/1D\s+10T'), ('SS', r'1S/1D\s+10T')]:
        xdm(Disks.work, '--set-geometry', g, '-q')
        with open(Files.output, 'w') as fout:
            xdm(Disks.work, '-i', '-q', stdout=fout)
        check_file_matches(Files.output, [(0, p)])

    # resize disk
    shutil.copyfile(Disks.recsgen, Disks.work)
    for s in ['800', '248', '1600']:
        xdm(Disks.work, '-Z', s, '-q')
        for f in ['PROG02560', 'DF129X010', 'DV127X010', 'DV255X015P']:
            xdm(Disks.work, '-e', f, '-q', '-o', Files.output)
            xdm(Disks.recsgen, '-e', f, '-o', Files.reference)
            check_files_eq('CLI', Files.output, Files.reference, 'PROGRAM')
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-Z', '240', stderr=ferr, rc=1)
        xdm(Disks.work, '-Z', '1608', stderr=ferr, rc=1)

    # new geometry handling (v1.5.3)
    # disk will be initialized by first command
    for c, g, p in [
            ('--initialize', 'SSSD', r'358 free\s+90 KB\s+1S/1D\s+40T'),
            ('--resize', 'DS1D', r'718 free\s+180 KB\s+2S/1D\s+40T'),
            ('--set-geometry', '80T', r'718 free\s+180 KB\s+2S/1D\s+80T'),  # geom mismatch
            ('--initialize', '408', r'406 free\s+102 KB\s+2S/1D\s+40T'),
            ('--resize', 'DSSD80T', r'1438 free\s+360 KB\s+2S/1D\s+80T'),
            ('--resize', '2DSS', r'718 free\s+180 KB\s+1S/2D\s+40T'),
            ('-Z', '208', r'206 free\s+52 KB\s+1S/2D\s+40T'),
            ('--set-geometry', 'SD80T', r'206 free\s+52 KB\s+1S/1D\s+80T'),
            ('-X', 'DSSD80T', r'1438 free\s+360 KB\s+2S/1D\s+80T'),
            ('--set-geometry', '20T', r'1438 free\s+360 KB\s+2S/1D\s+20T')]:  # geom mismatch
        xdm(Disks.work, c, g, '-q')
        with open(Files.output, 'w') as fout:
            xdm(Disks.work, '-i', '-q', stdout=fout)
        check_file_matches(Files.output, [(0, p)])
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '--initialize', 'SS80T', stderr=ferr, rc=1)
        xdm(Disks.work, '--resize', '2S', stderr=ferr, rc=1)
        xdm(Disks.work, '--resize', '80T', stderr=ferr, rc=1)
        xdm(Disks.work, '--set-geometry', '123', stderr=ferr, rc=1)

    # xdm99 vs real images
    rfile = r('ti-text')  # TEXT D/V80
    with open(Files.output, 'w') as fout, open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-X', 'sssd', '-n', 'TI-DISK', stderr=ferr, rc=0)
        xdm(Disks.work, '-a', rfile, '-n', 'TEXT', '-f', 'dv80', stderr=ferr, rc=0)
        check_file_len(Files.error, max_lines=0)
        check_disks_eq(Disks.work, Disks.tisssd)
        xdm(Disks.work, '-X', 'dsdd', '-n', 'TI-DISK', stderr=ferr, rc=0)
        xdm(Disks.work, '-a', rfile, '-n', 'TEXT', '-f', 'dv80',
            stderr=ferr, rc=0)
        check_file_len(Files.error, max_lines=0)
        check_disks_eq(Disks.work, Disks.tidsdd)
        xdm(Disks.work, '-Z', 'sssd', stderr=ferr, rc=0)
        check_file_len(Files.error, max_lines=0)
        check_disks_eq(Disks.work, Disks.tisssd)
        xdm(Disks.work, '--set-geometry', 'ssdd', stderr=ferr, rc=0)  # warn
        check_file_len(Files.error, min_lines=1, max_lines=1)
        xdm(Disks.work, '-i', stdout=fout, stderr=ferr, rc=0)  # warn
        check_file_len(Files.error, min_lines=2, max_lines=2)
        xdm(Disks.work, '-Z', 'dsdd', stderr=ferr, rc=0)
        check_file_len(Files.error, max_lines=2)
        check_disks_eq(Disks.work, Disks.tidsdd)
        xdm(Disks.work, '--set-geometry', 'ssdd80t', stderr=ferr, rc=0)
        check_file_len(Files.error, max_lines=2)
        xdm(Disks.work, '-X', 'dssd80t', '-n', 'TI-DSSD80', stderr=ferr, rc=0)
        check_file_len(Files.error, max_lines=2)
        check_disks_eq(Disks.work, Disks.tidssd80)

    # repair disks
    shutil.copyfile(Disks.bad, Disks.work)
    with open(Files.output, 'w') as f1, open(Files.reference, 'w') as f2:
        xdm(Disks.work, '-C', stderr=f1, rc=1)
        xdm(Disks.work, '-R', stderr=f2)
    check_file_len(Files.output, min_lines=2)
    with open(Files.output, 'w') as f1:
        xdm(Disks.work, '-C', stderr=f1)
    check_file_len(Files.output, max_lines=0)

    # FIAD operations
    shutil.copyfile(Disks.recsgen, Disks.work)
    xdm(Disks.work, '-e', 'PROG00255', 'DV064X010', '-t')
    xdm(Disks.work, '-e', 'PROG00255', '-t', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'prog00255.tfi', 'PROGRAM')
    xdm(Disks.work, '-e', 'DV064X010', '-t', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'dv064x010.tfi', 'PROGRAM')

    with open(Files.output, 'w') as f:
        xdm('-I', 'prog00255.tfi', 'dv064x010.tfi', stdout=f)

    xdm(Disks.work, '-e', 'PROG00255', 'DV064X010', '-9')
    xdm(Disks.work, '-e', 'PROG00255', '-9', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'prog00255.v9t9', 'PROGRAM')
    xdm(Disks.work, '-e', 'DV064X010', '-9', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'dv064x010.v9t9', 'PROGRAM')

    with open(Files.output, 'w') as f:
        xdm('-I', 'prog00255.v9t9', 'dv064x010.v9t9', stdout=f)

    xdm(Disks.work, '-e', 'PROG00255')
    xdm('-T', 'prog00255', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'prog00255.tfi', 'PROGRAM', Masks.TIFile)
    xdm('-T', 'prog00255', '-9', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'prog00255.v9t9', 'PROGRAM', Masks.v9t9)

    xdm(Disks.work, '-e', 'DV064X010', '-o', Files.reference)
    xdm('-F', 'dv064x010.tfi')
    check_files_eq('CLI', 'dv064x010', Files.reference, 'DIS/VAR 64')
    xdm('-F', 'dv064x010.tfi', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'dv064x010', 'PROGRAM')

    xdm('-F', 'dv064x010.v9t9', '-9')
    check_files_eq('CLI', 'dv064x010', Files.reference, 'DIS/VAR 64')
    xdm('-F', 'dv064x010.v9t9', '-o', Files.output)
    check_files_eq('CLI', Files.output, 'dv064x010', 'PROGRAM')

    xdm('-T', 'dv064x010', '-o', Files.output, '-n', 'DV064X010', '-f', 'DIS/VAR 64')
    check_files_eq('CLI', Files.output, 'dv064x010.tfi', 'PROGRAM', Masks.TIFile)
    os.remove('dv064x010.tfi')
    xdm('-T', 'dv064x010', '-n', 'DV064X010', '-f', 'DIS/VAR 64')
    check_files_eq('CLI', 'dv064x010.tfi', Files.output, 'PROGRAM', Masks.TIFile)

    xdm('-T', 'dv064x010', '-9', '-o', Files.output, '-n', 'DV064X010', '-f', 'DIS/VAR 64')
    check_files_eq('CLI', Files.output, 'dv064x010.v9t9', 'PROGRAM', Masks.v9t9)
    os.remove('dv064x010.v9t9')
    xdm('-T', 'dv064x010', '-9', '-n', 'DV064X010', '-f', 'DIS/VAR 64')
    check_files_eq('CLI', 'dv064x010.v9t9', Files.output, 'PROGRAM', Masks.v9t9)

    # TI names
    shutil.copyfile(Disks.recsdis, Disks.work)
    xdm(Disks.work, '-t', '-e', 'F16', 'V16')
    xdm(Disks.work, '-t', '-e', 'F16', 'V16', '--ti-names')
    check_files_eq('TI names', 'F16', 'f16.tfi', 'PROGRAM')
    check_files_eq('TI names', 'V16', 'v16.tfi', 'PROGRAM')
    xdm(Disks.work, '-9', '-e', 'F1')
    xdm(Disks.work, '-9', '-e', 'F1', '--ti-names')
    check_files_eq('TI names', 'F1', 'f1.v9t9', 'PROGRAM')
    xdm(Disks.work, '-e', 'V1', '-o', Files.reference)
    xdm(Disks.work, '-e', 'V1', '--ti-names')
    check_files_eq('TI names', 'V1', Files.reference, 'PROGRAM')

    # conversion between TI/PC names ('.' vs '/')
    file1 = os.path.join(Dirs.refs, 'vardis')
    with open(os.path.join(Dirs.tmp, 'file.y.z'), 'wb') as f:
        f.write(b'\xff' * 100)
    xdm(Disks.work, '-X', 'sssd', '-a', file1, '-n', 'FILE.X')
    xdm(Disks.work, '-a', os.path.join(Dirs.tmp, 'file.y.z'))
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-i', stdout=fout, rc=0)
    check_lines_start(Files.output, ('FILE/X', 'FILE/Y'), skip=1)

    xdm(Disks.work, '-r', 'FILE/X:NEW.FILE/X')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-i', stdout=fout, rc=0)
    check_lines_start(Files.output, ('NEW/FILE/X', 'FILE/Y'), skip=1)

    xdm(Disks.work, '-e', '*')
    check_file_exists('new.file.x')
    os.remove('new.file.x')
    check_file_exists('file.y')
    os.remove('file.y')

    xdm(Disks.work, '-e', 'FILE/Y', '-t')
    check_file_exists('file.y.tfi')
    os.remove('file.y.tfi')

    # rename disk (-n)
    xdm(Disks.work, '-X', 'sssd', '-n', 'FIRST.NAME')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-i', stdout=fout, rc=0)
    check_lines_start(Files.output, ('FIRST/NAME',))

    xdm(Disks.work, '-n', 'SECND.NAME')
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-i', stdout=fout, rc=0)
    check_lines_start(Files.output, ('SECND/NAME',))

    # output directory -o <dir>
    ref1 = r('glob1')
    ref2 = r('glob12')
    xdm(Disks.work, '-X', 'sssd', '-a', ref1, ref2)
    xdm(Disks.work, '-e', 'GLOB*', '-o', Dirs.tmp)
    check_file_exists(os.path.join(Dirs.tmp, 'glob1'))
    os.remove(os.path.join(Dirs.tmp, 'glob1'))
    check_file_exists(os.path.join(Dirs.tmp, 'glob12'))
    os.remove(os.path.join(Dirs.tmp, 'glob12'))

    xdm(Disks.work, '-X', 'sssd', '-a', ref1, ref2)
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-e', 'GLOB*', '-o', Files.output, stderr=ferr, rc=1)

    # stdin and stdout
    ref = r('vardis')
    with open(ref, 'r') as fin:
        xdm(Disks.work, '--initialize', 'sssd', '-a', '-', '-f', 'dv40', stdin=fin)
    with open(Files.output, 'w') as fout:
        xdm(Disks.work, '-e', 'STDIN', '-o', '-', stdout=fout)
    check_files_eq('stdin/stdout', Files.output, ref, 'DV')
    ref = r('sector1')
    with open(Files.reference, 'wb') as fout:
        xdm(Disks.work, '--initialize', 'sssd', '-a', ref, '-n', 'T', '-o', '-', stdout=fout)
    with open(Files.reference, 'rb') as fin:
        xdm('-', '-e', 'T', '-o', Files.output, stdin=fin)
    check_files_eq('stdin/stdout', Files.output, ref, 'P')

    # usage errors
    with open(Files.error, 'w') as ferr:
        xdm('-a', Files.output, stderr=ferr, rc=2)
        xdm('-T', 'prog00001', 'prog00002', '-o', Files.output,
            stderr=ferr, rc=1)
        xdm('-T', 'prog00001', 'prog00002', '-9', '-o', Files.output,
            stderr=ferr, rc=1)
        xdm('-F', '-o', Files.output, stderr=ferr, rc=2)

    # archives
    delfile(Files.archive)
    with open(Files.error, 'w') as ferr:
        xdm('-K', Files.archive, stderr=ferr, rc=1)
    xdm('-K', Files.archive, '-Y')
    xdm('-K', Files.archive, '-a', r('F1.tfi'), r('V16.tfi'), '-t')
    xdm('-K', Files.archive, '-a', r('F129.v9t9'), '-9')
    xdm(Disks.work, '-K', 'A', '-a', r('F128.tfi'), '-Y', '-X', 'sdds', '-t')
    xdm(Disks.work, '-K', 'A', '-r', 'F128:FFF')
    xdm(Disks.work, '-K', 'A', '-E', 'FFF')
    xdm(Disks.work, '-Y', '-K', 'B', '-A', 'FFF')
    xdm(Disks.work, '-e', 'A', 'B', '-o', Dirs.tmp)
    if content(t('a')) != content(t('b')):
        error('archive', 'Archives differ')

    with open(Files.error, 'w') as ferr:
        xdm('-i', '-q', '-o', Files.output, stderr=ferr, rc=2)
    with open(Files.error, 'w') as ferr:
        xdm('-X', 'sssd', '-K', Files.archive, stderr=ferr, rc=2)
    with open(Files.error, 'w') as ferr:
        xdm(Disks.work, '-Y', '-i', stderr=ferr, rc=2)

    # write minimal files
    pass  #TODO

    # default options (must be last)
    disk = os.path.join(Dirs.disks, 'basic1.dsk')
    os.environ[XDM99_CONFIG] = '-e NONEXIST ' + os.environ[XDM99_CONFIG]
    with open(Files.error, 'w') as ferr:
        xdm(disk, '-o', Files.output, stderr=ferr, rc=1)

    delfile(Files.output)
    delfile(Files.error)
    xdm(disk, '-e', 'NUMBERS-L', '-o', Files.output, rc=0)

    # cleanup
    delfile(Dirs.tmp)
    for fn in [
        'prog00001', 'prog00002', 'df127x001', 'df127x010', 'df127x020p', 'dv064x010.tfi', 'dv064x010',
        'prog00255', 'prog00255.tfi', 'prog00255.v9t9', 'dv064x010.v9t9', 'F16', 'V16', 'multfi.tfi', 'multfj.tfi',
        'multfk.tfi', 'mulv9t.v9t9', 'mulv9u.v9t9', 'f16.tfi', 'v16.tfi', 'F1', 'f1.v9t9', 'V1'
    ]:
        delfile(fn)


if __name__ == '__main__':
    runtest()
    print('OK')
