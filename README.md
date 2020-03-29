xdt99: TI 99 Cross-Development Tools
====================================

The **TI 99 Cross-Development Tools** (xdt99) are a suite of programs that
facilitate the development of programs for the TI 99 family of home computers
and other TMS9900-based systems on modern computer systems.

 * `xas99`: A TMS9900/TMS9995 cross-assembler
 * `xga99`: A GPL cross-assembler
 * `xbas99`: A TI BASIC and TI Extended BASIC encoder and encoder
 * `xda99`: A TMS9900/TMS9995 disassembler
 * `xdg99`: A GPL disassembler
 * `xdm99`: A disk and file manager
 * `xhm99`: A manager for HFE images used by HxC floppy emulators
 * `xvm99`: A volume manager for nanoPEB/CF7+ Compact Flash cards
 * `xdt99-mode`: A major mode for the GNU Emacs text editor
 * `xdt99 IDEA`: A plugin for the IntelliJ IDEA development environment

xdt99 runs on any platform that Python supports, including Linux, Windows, and
MacOS.

The `xas99` cross-assembler supports TMS9900 and TMS9995 assembly and generates
object code, E/A option 5 images, binaries, cartridges, and Extended BASIC
embeddings.  Modern extensions such as relaxed syntax, extended expressions, a
preprocessor, special-purpose operators, and local labels simplify the writing
of assembly programs on modern hardware.

The `xga99` GPL cross-assembler generates GROM image files for TI's proprietary
Graphics Programming Language (GPL).  The GPL assembler generates byte code
suitable for emulators or GROM-capable multi-carts and RPK cartridge archives
that can be run in the MAME emulator.

The `xbas99` BASIC tool tokenizes TI BASIC and TI Extended BASIC programs into
internal format that can be loaded by the BASIC interpreters.  Conversely, the
tool also lists and decodes BASIC program files.  The tool also supports label-
based programs without line numbers.

The `xda99` and `xdg99` disassemblers generate source code from machine code or
GPL bytecode files, resp.  In addition to regular top-down disassembly, both
disassemblers also support a run mode that follows the static program flow.

The `xdm99` disk manager works with sector-based TI disk images used by most
emulators, including MAME.  `xdm99` also supports disk-less files in TIFILES and
v9t9 format, used by Classic 99.  The `xvm99` volume manager extends the `xdm99`
functionality to CF cards used by the nanoPEB/CF7+ devices.  Similarly, `xhm99`
extends `xdm99` to HFE images used by the HxC floppy emulators.

The `xdt99-mode` and `xdt99 IDEA` plugins provide editor support for writing
assembly, GPL code, and TI (Extended) BASIC programs using the GNU Emacs and the
IntelliJ IDEA development environments, resp.  Plugin features include syntax
highlighting, navigation, and semantic renaming, among others.

For additional information, please refer to the [xdt99 homepage][1] or the
[xdt99 manual][4].  Windows users unfamiliar working with the command line find
some platform-specific information in the [Windows Guide][5].

**Latest version: 3.0.0**

The latest binary distribution of xdt99 is available on [GitHub][2].  xdt99
requires [Python 3.6][6] or higher.
 
xdt99 is released under the GNU GPL version 3.  All sources are available on
[GitHub][3].


Download and Installation
-------------------------

The latest xdt99 [binary release][2] is available on GitHub; experienced users
may also clone the [xdt99 repository][3].  The repository contains some
additional test cases that are useful when extending or modifying xdt99.

xdt99 requires a working installation of [Python 3.6][6] or later.  On most
Linux systems, Python is available as a package.  For other platforms, we
recommend to install the latest stable Python 3 release.  Please note that xdt99
will not run on Python 2.

All xdt99 files should be placed somewhere in the `$PATH` or where the
command-line interpreter will find them.  Windows users will find Windows-
specific instructions in the [Windows Guide][5].

Additionally, the `ide/` directory contains the editor plugins for GNU Emacs
and IntelliJ IDEA.  Please refer to the `ide/README.md` file for further
information about editor support.


Basic Usage: `xas99`
--------------------

This is just a brief overview of the most common usages for `xas99`.  For
detailed information, please refer to the [xdt99 homepage][8] or the [manual][4]
included with xdt99.

Generate object code for the Editor/Assembler cartridge, option 3:

    $ xas99.py [-R] [-C] <source file>
    
Generate program image for the Editor/Assembler cartridge, option 5:

    $ xas99.py -i [-R] <source file>

Generate cartridge file for the MAME emulator:

    $ xas99.py -c [-R] <source file>

Generate binary data files, e.g., for [FinalGROM][7] cartridge:

    $ xbas99.py -b <source file>

Generate program image embedded in Extended BASIC loader:

    $ xas99.py --embed-xb <source file>

Generate list file diagnostic output:

    $ xas99.py <source file> -L <list file>

Link object code files:

    $ xas99.py -l <obj file> <obj file> [...] -o whole.obj

For a complete overview of the available command-line options, see `xas99.py
-h`.

`xas99` offers various language extensions to the original Editor/Assembler
module:

 * Relaxed syntax (e.g., labels, comments, whitespace, case insensitivity)
 * Improved expressions (e.g., Boolean operators, binary numbers, parentheses)
 * Label continuations and local labels (e.g., `label:`, `!label`)
 * New operators (e.g., `w#`, `s#`)
 * New directives (e.g., `BCOPY`, `XORG`, `SAVE`)
 * Conditional assembly (e.g., `.ifdef`)
 * Macros (`.defm`)

Please refer to the [xdt99 manual][4] for a detailed description of these
features.


Basic Usage: `xga99`
--------------------

This is just a brief overview of the most common usages for `xga99`.  For
detailed information, please refer to the [xdt99 homepage][9] or the [manual][4]
included with xdt99.

Assemble GPL source file into GPL byte code, e.g., for [FinalGROM][7]:

    $ xga99.py <source file>

Generate cartridge file for the MAME emulator:

    $ xga99.py -c <source file>

For a complete overview of the available command-line options, see `xga99.py
-h`.

`xga99` offers various language extensions compared to native GPL assemblers:

 * Relaxed syntax (e.g., labels, comments, whitespace, case insensitivity)
 * Improved expressions (e.g., Boolean operators, binary numbers, parentheses)
 * Label continuations and local labels (e.g., `label:`, `!label`)
 * New directives (e.g., `STRI`, `BCOPY`, `FLOAT`)
 * Conditional assembly (e.g., `.ifdef`)
 * Macros (`.defm`)

Please refer to the [xdt99 manual][4] for a detailed description of these
features.


Basic Usage: `xbas99`
---------------------

This is just a brief overview of the most common usages for `xbas99`.  For
detailed information, please refer to the [xdt99 homepage][10] or the
[manual][4] included with xdt99.

Print TI BASIC or TI Extended BASIC program on screen:

    $ xbas99.py -p <program file>

Decode BASIC program to source format (i.e., list to file):

    $ xbas99.py -d <program file> [-o <output file>]

Create BASIC program in internal format for BASIC interpreter:

    $ xbas99.py [-c] <source file> [-o <output file>]

Create BASIC program from label-based source file:

    $ xbas99.py -c -l <source file> [-o <output file>]

List BASIC program stored on disk image (advanced use):

	$ xdm99.py <disk image> -p <prog name> | xbas99.py -p -

For a complete overview of the available command-line options, see `xbas99.py
-h`.


Basic Usage: `xda99`/`xdg99`
----------------------------

This is just a brief overview of the most common usages for `xda99`.  For
detailed information, please refer to the [xdt99 homepage][11] or the
[manual][4] included with xdt99.

Disassemble binary top-down:

    $ xda99.py <binary file> -a <first addr> [-f <from addr>]
    
Disassemble with run simulation:

    $ xda99.py <binary file> -a <first addr> -r <start addr> [...]

For a complete overview of the available command-line options, see `xda99.py
-h` or `xdg99 -h`.


Basic Usage: `xdm99`
--------------------

This is just a brief overview of the most common usages for `xdm99`.  For
detailed information, please refer to the [xdt99 homepage][12] or the
[manual][4] included with xdt99.

Print disk catalog on screen:

    $ xdm99.py <disk image>

Extract one or more files from disk image to local file system:

    $ xdm99.py <disk image> -e <file> [...] [-o <file or dir>]

Extract files in TIFILES or v9t9 format:

    $ xdm99.py <disk image> -t -e <file> [...]
    $ xdm99.py <disk image> -9 -e <file> [...]

Print file contents to screen:

    $ xdm99.py <disk image> -p <file> [...]

Add local files to disk image:

    $ xdm99.py <disk image> -a <file> [...] [-f <format>] [-n <name>]

Rename file on disk image:

    $ xdm99.py <disk image> -r <old name>:<new name> [...]

Delete file on disk image:

    $ xdm99.py <disk image> -d <file> [...]

Show info about TIFILES or v9t9 file:

    $ xdm99.py -I <file>

Convert TIFILES files or v9t9 files to plain files:

    $ xdm99.py -F <TIFiles file> [...]
    $ xdm99.py -F <TIFiles file> [...] -9

Convert plain files to TIFILES files or v9t9 files:

    $ xdm99.py -T <plain file> [...] [-f <format>] [-n <name>]
    $ xdm99.py -T <plain file> [...] -9 [-f <format>] [-n <name>]

Print contents of TIFILES or v9t9 file:

    $ xdm99.py -P <file>

Initialize blank disk:

    $ xdm99.py <disk image> -X <size> [-n <name>]

Resize disk image:

    $ xdm99.py <disk image> -Z <sectors>

Repair disk image with corrupt files or other inconsistencies:

    $ xdm99.py -R <disk image> [-o <new disk image>]

Override disk geometry:

    $ xdm99.py <filename> --set-geometry <geometry>

Print sector dump:

    $ xdm99.py <disk image> -S <sector>

For a complete overview of the available command-line options, see `xdm99.py
-h`.


Basic Usage: `xhm99`
--------------------

This is just a brief overview of the most common usages for `xhm99`.  For
detailed information, please refer to the [xdt99 homepage][13] or the
[manual][4] included with xdt99.

Convert disk image to HFE image:

    $ xhm99.py -T <disk image> [-o <HFE image>]

Convert HFE image to disk image:

    $ xhm99.py -F <HFE image> [-o <disk image>]

Show disk catalog:

    $ xhm99.py <HFE image>

Additionally, `xhm99` supports all commands of `xdm99`.

Add or remove files to/from image:

    $ xhm99.py <HFE file> -a <files> [...] [-n <name>] [-f <format>] [-t | -9]
    $ xhm99.py <HFE file> -e <files> [...]

Create new image (and add a file to it):

	$ xhm99.py <HFE file> -X <size> [-a <files> [...]]

Resize image (e.g., DSDD/40T to DSSD/80T):

    $ xhm99.py <HFE file> -Z <size>

For a complete overview of the available command-line options, see `xhm99.py
-h`.


Basic Usage: `xvm99`
--------------------

This is just a brief overview of the most common usages for `xvm99`.  For
detailed information, please refer to the [xdt99 homepage][14] or the
[manual][4] included with xdt99.

Show information about volumes:

    $ xvm99.py <device> <volume ids>

Read disk images from volumes:

    $ xvm99.py <device> <volume ids> -r <filename> [--keep-size]

Write disk image to volumes:

    $ xvm99.py <device> <volume ids> -w <disk image> [--keep-size]

`<device>` is the platform-specific name of the Compact Flash card drive, e.g.,
`/dev/sd<X>` on Linux, `/dev/Disk<X>` on Mac OS X, or `\\.\PHYSICALDRIVE<X>` on
Windows.

`<volume ids>` is a single value or a combination of values and ranges, e.g.,
`1,3-4,6-10`.  If more than one volume is supplied, the same command is applied
to _all_ volumes.

Additionally, `xvm99` extends most of the functionality of `xdm99` to disk
volumes.

Print disk catalog of one or more volumes:

    $ xvm99.py <device> <volume ids> -i

Add file to one or more volumes:

    $ xvm99.py <device> <volume ids> -a <file> [-n <name>] [-f <format>] [-t | -9]

For a complete overview of the available command-line options, see `xvm99.py
-h`.


Contact Information
-------------------

The xdt99 tools are released under the GNU GPL, in the hope that fellow TI 99
enthusiasts may find them useful.

Please email bug reports and feature requests to the developer at <r@0x01.de>,
or use the issue tracker of the [project][2].


[1]: https://endlos99.github.io/xdt99
[2]: https://github.com/endlos99/xdt99/releases
[3]: https://github.com/endlos99/xdt99
[4]: https://github.com/endlos99/xdt99/blob/master/doc/MANUAL.md
[5]: https://github.com/endlos99/xdt99/blob/master/doc/WINDOWS.md
[6]: https://www.python.org/downloads/
[7]: https://endlos99.github.io/finalgrom99
[8]: https://endlos99.github.io/xdt99#xas99
[9]: https://endlos99.github.io/xdt99#xga99
[10]: https://endlos99.github.io/xdt99#xbas99
[11]: https://endlos99.github.io/xdt99#xda99
[12]: https://endlos99.github.io/xdt99#xdm99
[13]: https://endlos99.github.io/xdt99#xvm99
[14]: https://endlos99.github.io/xdt99#xhm99
