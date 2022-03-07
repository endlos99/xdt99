#!/usr/bin/env python3

import os
import shutil

from config import Dirs, Disks, Files
from utils import xvm, xdm, error, content


# Main test

def runtest():
    """check error handling"""

    # setup
    with open(Disks.volumes, 'wb') as v:
        for i in range(4 * 1600):
            v.write(bytes(2 * 256))  # Disk.bytes_per_sector plus padding
    shutil.copyfile(Disks.recsgen, Disks.work)
    xvm(Disks.volumes, '1,2', '-X', 'cf', '-q')

    # file errors
    with open(Files.error, 'w') as ferr:
        xvm('nosuchvol', '1', '-i', stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badfile', 'Bad file not caught')

    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '1', '-a', 'nosuchfile', stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badfile', 'Bad file not caught')

    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '1', '-K', 'NOARC', stderr=ferr, rc=1)

    xvm(Disks.volumes, '1', '-Y', '-K', 'ARC', '-q')
    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '1', '-K', 'ARC', '-e', 'NOSUCH', stderr=ferr, rc=1)

    xvm(Disks.volumes, '1', '-K', 'ARC', '-E', '*', '-q', rc=0)  # no error

    # bad arguments
    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, 'zzz', '-i', stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '1-2-3', '-i', stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    with open(Files.input, 'wb') as fin:
        fin.write(b'\x99' * 123)
    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '0', '-a', Files.input, '-f', 'foo', stderr=ferr, rc=1)
    if 'Traceback' in content(Files.error, mode='r'):
        error('badarg', 'Bad argument not caught')

    with open(Files.error, 'w') as ferr:
        xvm(Disks.volumes, '1', '-Y', stderr=ferr, rc=2)

    # cleanup
    os.remove(Files.error)
    os.remove(Files.input)
    os.remove(Disks.work)
    os.remove(Disks.volumes)


if __name__ == '__main__':
    runtest()
    print('OK')
