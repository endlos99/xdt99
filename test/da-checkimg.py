#!/usr/bin/env python3

import os
import random

from config import Dirs, Files, XDA99_CONFIG
from utils import xda, xas, error, clear_env, delfile, check_binary_files_eq


# Check function

def xint(s):
    """return hex or decimal value"""
    return int(s.lstrip('>'), 16 if s[:2] == '0x' or s[:1] == '>' else 10)


def check_data(fn):
    """count DATAs in source"""
    datas = 0
    with open(fn, 'r') as fin:
        source = fin.readlines()
    for line in source:
        cs = line.split()
        if len(cs) >= 2 and cs[1].lower() == 'data' or len(cs) >= 1 and cs[0].lower() == 'data':
            datas += 1
    return datas
    
    
def check_eq(value1, value2, msg):
    if value1 != value2:
        error(msg, 'Count mismatch: expected %d, but got %d' % (value2, value1))


# Main test

def runtest():
    """check cross-generated output against native reference files"""

    clear_env(XDA99_CONFIG)

    # disassembler: run
    for srcfile, aopts, addr, start in [
            #('asopcs.asm', ['-R'], '0000', '0000']), only for -d
            #('asexprs.asm', [], '0000', '0154'),  too many segments
            ('ashello.asm', ['-R', '--base', '0xa000'], 'a000', 'a016'),
            ('asregs.asm', ['-R'], '0000', '0000'),
            ('ascart.asm', ['-R'], '0000', '000c'),
            ('darun.asm', ['-R'], '0000', '0002')
            ]:
        source = os.path.join(Dirs.sources, srcfile)
        xas(*[source, '-b'] + aopts + ['-q', '-o', Files.reference])
        xda(Files.reference, '-a', addr, '-r', start, '-p', '-q', '-o', Files.input)
        xas(*[Files.input, '-b', '-R', '-q', '-o', Files.output])
        check_binary_files_eq(srcfile, Files.output, Files.reference)

    # disassembler: top-down
    for srcfile, aopts, addr, start in [
            ('asopcs.asm', ['-R'], '0000', '0000'),
            ('asexprs.asm', [], '0000', '0154'),
            ('asregs.asm', ['-R'], '0000', '0000'),
            ('ascart.asm', ['-R'], '0000', '000c'),
            ('darun.asm', ['-R'], '0000', '0002')
            ]:
        source = os.path.join(Dirs.sources, srcfile)
        xas(*[source, '-b'] + aopts + ['-q', '-o', Files.reference])
        xda(Files.reference, '-a', addr, '-f', start, '-p', '-o', Files.input)
        xas(*[Files.input, '-b', '-R', '-q', '-o', Files.output])
        check_binary_files_eq(srcfile, Files.output, Files.reference)

    # running disassembler
    source = os.path.join(Dirs.sources, 'darun.asm')
    xas(source, '-b', '-R', '-q', '-o', Files.reference)
    xda(Files.reference, '-a', '0', '-r', '2', '-p', '-o', Files.output)
    check_eq(check_data(Files.output), check_data(source), 'run')

    source = os.path.join(Dirs.sources, 'daexec.asm')
    xas(source, '-b', '-R', '-q', '-o', Files.reference)
    xda(Files.reference, '-a', '1000', '-r', '103c', '1008', '-p', '-o', Files.output)
    check_eq(check_data(Files.output), check_data(source), 'run')

    # disassemble cart BINs
    for binfile, start in (
            ('blobm.bin', '6012'),
            ('blobh.bin', 'start')):
        binary = os.path.join(Dirs.refs, binfile)
        xda(binary, '-a', '6000', '-r', start, '-p', '-q', '-o', Files.input)
        xas(Files.input, '-b', '-R', '-q', '-o', Files.output)
        check_binary_files_eq(binary, Files.output, binary)

        xda(binary, '-a', '6000', '-f', start, '-p', '-o', Files.input)
        xas(Files.input, '-b', '-R', '-q', '-o', Files.output)
        check_binary_files_eq(binary, Files.output, binary)

    # disassemble random
    for r in range(16):
        random.seed(r)
        binary = bytes([random.randrange(256) for i in range(2048)])
        with open(Files.reference, 'wb') as fref:
            fref.write(binary)
        xda(Files.reference, '-a', '1000', '-f', '1000', '-p', '-o', Files.input)
        xas(Files.input, '-b', '-R', '-q', '-o', Files.output)
        check_binary_files_eq('random' + str(r), Files.reference, Files.output)
        xda(Files.reference, '-a', '1000', '-f', '1000', '-p', '-5', '-18', '-o', Files.input)
        xas(Files.input, '-b', '-R', '-5', '-18', '-q', '-o', Files.output)
        check_binary_files_eq('random' + str(r) + '518', Files.reference, Files.output)

    # Cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
