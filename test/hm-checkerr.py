#!/usr/bin/env python3

from config import Dirs, Disks, Files, XHM99_CONFIG
from utils import xhm, t, r, clear_env, delfile


# Main test

def runtest():
    """check command line interface"""

    clear_env(XHM99_CONFIG)

    # HFE disk errors
    xhm(Disks.work, '-X', 'sssd', '-n', 'FOOBAR')
    with open(Files.error, 'w') as ferr:
        xhm(Disks.work, '-e', 'NOSUCHFILE', stderr=ferr, rc=1)

    xhm(Disks.work, '-X', 'sssd', '-a', r('V64V.v9t9'), '-9')
    with open(Files.error, 'w') as ferr:
        xhm(Disks.work, '-K', 'NOSUCHARK', '-A', 'V64V', stderr=ferr, rc=1)

    # file errors
    with open(Files.error, 'w') as ferr:
        xhm(t('doesnotexist'), '-i', stderr=ferr, rc=1)

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
