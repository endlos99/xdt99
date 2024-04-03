#!/usr/bin/env python3

import os
import re

from config import Dirs, Disks, Files, XAS99_CONFIG
from utils import (xas, xdm, error, clear_env, delfile, read_stderr, get_source_markers, check_errors, content,
                   content_len, content_line_array)


def cutout(lines, start_char, frm=0, to=0, pattern=None):
    occurences = dict()
    for line in lines:
        if line[0] != start_char:
            continue
        if pattern is None:
            cut = line[frm:to]
        else:
            m = re.search(pattern, line)
            if not m:
                continue
            cut = m.group(1)
        try:
            occurences[cut] += 1
        except KeyError:
            occurences[cut] = 1
    return occurences


# Main test

def runtest():
    """check error messages against native assembler listing"""

    clear_env(XAS99_CONFIG)

    # cross-assembler error messages
    source = os.path.join(Dirs.sources, 'aserrs.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-s', '-o', Files.output, stderr=ferr, rc=1)
    warnings = read_stderr(Files.error)

    # TI assembler error messages
    ti_errors = []
    xdm(Disks.asmsrcs, '-e', 'ASERRS-L', '-o', Files.reference)
    with open(Files.reference, 'r') as f:
        for line in f:
            err = re.match(r'\*{5}\s+([A-Z ]*) - (\d+)', line)
            if err:
                lino = err.group(2)
                ti_errors.append(lino)

    # compare
    check_errors(ti_errors, warnings)

    # invalid labels and confirmation of label specs
    for fn, s in (('aslabele.asm', []),
                  ('aslabele-ti.asm', ['-s']),
                  ('asxlabe.asm', [])):
        source = os.path.join(Dirs.sources, fn)
        with open(Files.error, 'w') as ferr:
            xas(source, '-q', *s, '-o', Files.output, stderr=ferr, rc=1)
        act_errors = read_stderr(Files.error)
        ref_errors = get_source_markers(source, r';ERROR')
        check_errors(ref_errors, act_errors)

    # xdt99-specific errors
    source = os.path.join(Dirs.sources, 'asxerrs.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-o', Files.output, stderr=ferr, rc=1)
    warnings = read_stderr(Files.error)
    ref_errors = get_source_markers(source, r';ERROR(:....)?')
    check_errors(ref_errors, warnings)

    source = os.path.join(Dirs.sources, 'assyntax.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-o', Files.output, stderr=ferr, rc=1)
    if content_line_array(Files.error)[-1][:2] != '1 ':
        error('syntax', 'Incorrect number of errors')

    source = os.path.join(Dirs.sources, 'assyntax.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-r', '-o', Files.output, stderr=ferr, rc=1)
    if content_line_array(Files.error)[-1][:2] != '3 ':
        error('syntax', 'Incorrect number of errors')

    # xdt99-specific errors (image generation)
    source = os.path.join(Dirs.sources, 'asxerrsb.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-b', '-X', '-o', Files.output, stderr=ferr, rc=1)
    warnings = read_stderr(Files.error)
    ref_errors = get_source_markers(source, tag=r';ERROR(:....)?')
    check_errors(ref_errors, warnings)

    # open .if-.endif or .defm-.endm
    source = os.path.join(Dirs.sources, 'asopenif.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)
    with open(Files.error, 'r') as fin:
        msgs = ' '.join(fin.readlines())
    if 'Missing .ENDIF' not in msgs:
        error('open', 'Missing error for open .if/.endif')

    source = os.path.join(Dirs.sources, 'asopenmac.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)
    with open(Files.error, 'r') as fin:
        msgs = ' '.join(fin.readlines())
    if 'Missing .ENDM' not in msgs:
        error('open', 'Missing error for open .defm/.endm')

    # macro errors
    source = os.path.join(Dirs.sources, 'asmacse.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)
    act_errors = read_stderr(Files.error)
    exp_errors = get_source_markers(source, tag=r';ERROR')
    check_errors(exp_errors, act_errors)

    # files not found
    source = os.path.join(Dirs.sources, 'ascopyi.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)

    # warnings
    source = os.path.join(Dirs.sources, 'aswarn.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-R', '-o', Files.output, stderr=ferr, rc=0)  # no error
    act_errors = read_stderr(Files.error, include_warnings=True)
    exp_errors = get_source_markers(source, tag=r';WARN')
    check_errors(exp_errors, act_errors)

    source = os.path.join(Dirs.sources, 'asuusym.asm')  # undefined symbols
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-o', Files.output, stderr=ferr, rc=0)  # no error
    with open(Files.error, 'r') as fin:
        output = fin.read()
    if 'u1:2, u2:9, u3:11, u4:19, u5:20' not in output:
        error('stdout', 'Bad listing of unreferenced symbols')

    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-q', '-o', Files.output, stderr=ferr, rc=0)  # no error
    with open(Files.error, 'r') as fin:
        output = fin.read()
    if output.strip():
        error('stdout', 'Unwanted  listing of unreferenced symbols')

    # warning categories
    source = os.path.join(Dirs.sources, 'asxwarn.asm')  # various warnings in different categories
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '-o', Files.output, stderr=ferr, rc=0)  # no error
    filenames = cutout(content_line_array(Files.error), '>', 2, 10)
    if filenames.get('asxwarn.') != 4 or filenames.get('asxwarni') != 1:
        error('xwarn', 'Incorrect warning distribution across files')
    lines = cutout(content_line_array(Files.error), '>', pattern='<\\d> (....) -')
    if lines.get('0006') != 1 or lines.get('0007') != 1 or lines.get('0011') != 1 or lines.get('****') != 2:
        error('xwarn', 'Incorrect line numbers for warnings')

    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '--quiet-unused-syms', '-o', Files.output, stderr=ferr, rc=0)  # no error
    filenames = cutout(content_line_array(Files.error), '>', 2, 10)
    if filenames.get('asxwarn.') != 3 or filenames.get('asxwarni') is not None:
        error('xwarn', 'Incorrect warning distribution across files for --quiet-unused-syms')
    lines = cutout(content_line_array(Files.error), '>', pattern='<\\d> (....) -')
    if lines.get('0006') != 1 or lines.get('0007') != 1 or lines.get('0011') != 1 or lines.get('****') is not None:
        error('xwarn', 'Incorrect line numbers for warnings for --quiet-unused-syms')

    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '--quiet-opts', '-o', Files.output, stderr=ferr, rc=0)  # no error
    filenames = cutout(content_line_array(Files.error), '>', 2, 10)
    if filenames.get('asxwarn.') != 3 or filenames.get('asxwarni') != 1:
        error('xwarn', 'Incorrect warning distribution across files for --quiet-opts')
    lines = cutout(content_line_array(Files.error), '>', pattern='<\\d> (....) -')
    if lines.get('0006') != 1 or lines.get('0007') != 1 or lines.get('0011') is not None or lines.get('****') != 2:
        error('xwarn', 'Incorrect line numbers for warnings for --quiet-opts')

    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '--quiet-usage', '-o', Files.output, stderr=ferr, rc=0)  # no error
    filenames = cutout(content_line_array(Files.error), '>', 2, 10)
    if filenames.get('asxwarn.') != 2 or filenames.get('asxwarni') != 1:
        error('xwarn', 'Incorrect warning distribution across files for --quiet-usage')
    lines = cutout(content_line_array(Files.error), '>', pattern='<\\d> (....) -')
    if lines.get('0006') is not None or lines.get('0007') is not None or lines.get('0011') != 1 or \
            lines.get('****') != 2:
        error('xwarn', 'Incorrect line numbers for warnings for --quiet-usage')

    with open(Files.error, 'w') as ferr:
        xas(source, '--color', 'off', '-o', Files.output, stderr=ferr, rc=0)  # no error
    filenames = cutout(content_line_array(Files.error), '>', 2, 10)
    if filenames.get('asxwarn.') != 2 or filenames.get('asxwarni') != 1:
        error('xwarn', 'Incorrect warning distribution across files w/o -R')
    lines = cutout(content_line_array(Files.error), '>', pattern=r'<\d> (....) -')
    if lines.get('0006') is not None or lines.get('0007') is not None or lines.get('0011') != 1 or\
            lines.get('****') != 2:
        error('xwarn', 'Incorrect line numbers for warnings w/o -R')

    # unused symbols w/locations
    source = os.path.join(Dirs.sources, 'asxwarn.asm')  # various warnings in different categories
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '--quiet-usage', '--quiet-opts', '-o', Files.output, stderr=ferr, rc=0)
    ocurrences = cutout(content_line_array(Files.error), '*', 33, -1)
    try:
        success = len(ocurrences) == 2 and ocurrences['s1:4'] == 1 or ocurrences['sinc:3'] == 1
    except KeyError:
        success = False
    if not success:
        error('xwarn', 'Incorrect unused symbols lists')

    # unresolved references
    source = os.path.join(Dirs.sources, 'asunref.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=0)
    if content_len(Files.error) > 0:
        error('unresolved refs', 'Extra warning about unresolved refs')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-o', Files.output, stderr=ferr, rc=0)
    if 'Unresolved references:' not in content(Files.error, 'r'):
        error('unresolved refs', 'Missing warning about unresolved refs')
    with open(Files.error, 'w') as ferr:
        xas(source, '-t', 'a2', '-o', Files.output, stderr=ferr, rc=0)
    if 'Unresolved references:' not in content(Files.error, 'r'):
        error('unresolved refs', 'Missing warning about unresolved refs')

    # misplaces auto-generated constants
    source = os.path.join(Dirs.sources, 'asautoe.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-o', Files.output, stderr=ferr, rc=1)
    errs = re.findall(r'Auto-constant defined after AUTO directive', content(Files.error, 'r'))
    if len(errs) != 4:
        error('misplaced auto-cons', 'Missing error about auto-cons after AUTO')

    # warning about arith expressions relying on non-standard precedence
    source = os.path.join(Dirs.sources, 'asaprec.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '--color', 'off', '-o', Files.output, stderr=ferr, rc=0)
    warnings = read_stderr(Files.error, include_warnings=True)
    markers = get_source_markers(source, r';WARN')
    check_errors(markers, warnings)

    # STDOUT
    source = os.path.join(Dirs.sources, 'asstdout.asm')
    with open(Files.error, 'w') as fout:
        xas(source, '-b', '-R', '-o', Files.output, stdout=fout, rc=0)  # no error
    with open(Files.error, 'r') as fin:
        output = fin.read()
    if output.strip() != 'hello 42 world!':
        error('stdout', 'Invalid STDOUT output: ' + output)

    # register alias (3.5.1) [also see as-checkext]
    source = os.path.join(Dirs.sources, 'asxrals.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-b', '-D', 'err', '-o', Files.output, stderr=ferr, rc=1)
    errors = read_stderr(Files.error, include_warnings=True)
    err_markers = get_source_markers(source, r';ERROR')
    wrn_markers = get_source_markers(source, r';WARN')
    check_errors(err_markers + wrn_markers, errors)

    source = os.path.join(Dirs.sources, 'asxralse.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)
    errors = read_stderr(Files.error)
    markers = get_source_markers(source, r';ERROR')
    check_errors(markers, errors)

    # .rept/.endr
    source = os.path.join(Dirs.sources, 'asxrepte.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)
    errors = read_stderr(Files.error)
    markers = get_source_markers(source, r';ERROR')
    check_errors(markers, errors)

    source = os.path.join(Dirs.sources, 'asxrepte2.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-o', Files.output, stderr=ferr, rc=1)

    # parser error
    source = os.path.join(Dirs.sources, 'aserrpar.asm')
    with open(Files.error, 'w') as ferr:
        xas(source, '-R', '-o', Files.output, stderr=ferr, rc=1)
    errs = content_line_array(Files.error)[1:-1:2]
    lines = set(e[22] for e in errs)
    if lines != set(str(i) for i in range(1, 9)):
        error('parser', f'Missing error message: {lines}')

    # cleanup
    delfile(Dirs.tmp)


if __name__ == '__main__':
    runtest()
    print('OK')
