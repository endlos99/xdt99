xdt99: TI 99 Cross-Development Tools
====================================

The **TI 99 Cross-Development Tools** (xdt99) are a small suite of programs that
facilitate the development of programs for the TI 99 family of home computers on
modern computer systems:

 * [`xas99`](#xas99): A TMS9900 cross-assembler
 * [`xga99`](#xga99): A GPL cross-assembler
 * [`xbas99`](#xbas99): A TI BASIC and TI Extended BASIC lister and encoder
 * [`xda99`](#xda99): A TMS9900 disassembler
 * [`xdg99`](#xda99): A GPL disassembler
 * [`xdm99`](#xdm99): A disk manager for sector-based TI disk images
 * [`xhm99`](#xhm99): A manager for HFE images used by HxC floppy emulators
 * [`xvm99`](#xvm99): A volume manager for nanoPEB/CF7+ Compact Flash cards
 * `xdt99-mode`: A [major mode][7] for the GNU Emacs text editor
 * `xdt99 IDEA`: A [plugin][8] for the IntelliJ IDEA development environment

The `xas99` cross-assembler supports all documented TMS9900 opcodes and should
assemble any existing assembly code for the TI 99 without modification.  Object
code generated by `xas99` is identical to compressed or uncompressed object code
produced by the original TI Editor/Assembler package.  Modern extensions such as
local labels and macro support simplify the writing of assembly programs on
modern hardware.  The F18A GPU instruction set is also supported.

The `xga99` GPL cross-assembler generates GROM image files for TI's proprietary
Graphics Programming Language (GPL).  The GPL assembler is a quick way to
translate self-written GPL programs into RPK cartridge files that can be run
with the MESS emulator.

The `xbas99` BASIC tool encodes TI BASIC and TI Extended BASIC programs into
their internal format that can be loaded by the BASIC interpreter using
the `OLD` command.  Conversely, the tool also lists BASIC program files
similarly to the `LIST` command.

The `xda99` and `xdg99` disassembler generate source code from machine code
or GPL bytecode files, respectively.  In addition to regular top-down
disassembly, both disassemblers also support a run mode that follows
the program flow statically.

The `xdm99` disk manager works with sector-based TI disk images used by most
emulators, including MESS.  `xdm99` also supports disk-less files in TIFiles and
V9T9 format.  The `xvm99` volume manager extends the `xdm99` functionality to CF
cards used by the nanoPEB/CF7+ devices.  Similarly, `xhm99` extends `xdm99` to
HFE images used by the HxC floppy emulators.

The `xdt99-mode` and `xdt99 IDEA` plugins provide editor support for writing
assembly and TI Extended BASIC programs using the GNU Emacs and the IntelliJ
IDEA development environments, respectively.  Plugin features include syntax
highlighting, navigation, and semantic renaming, among others.

For additional information, please refer to the [xdt99 homepage][1] or the
[xdt99 manual][4].  Windows users unfamiliar with working with the command line
will find some platform-specific information in the [Windows tutorial][5].

**Latest version: 3.3.0**

The latest binary distribution of xdt99 is available on the project
[releases page][2] on GitHub.  xdt99 requires [Python 3.8][6] or higher and runs
on any platform that Python supports, including Linux, Windows, and maxOS.

xdt99 is released under the GNU GPLv2.  All sources are available on
[GitHub][3].


Download and Installation
-------------------------

Download the latest [binary release][2] from GitHub.  Alternatively, clone the
entire xdt99 GitHub [repository][3].

While almost all xdt99 tools are standalone, self-contained Python programs that
can be used independently of each other, we strongly recommend placing all files
together somewhere in your `$PATH` or wherever your Python installation will
find them.

The `xdt99-mode` and `xdt99 IDEA` plugins provide editor support and may be used
separately of the other xdt99 tools.  Likewise, `xas99` and others may be used
without these plugins.  They do, however, provide useful assistance when
creating or editing assembly, GPL, or TI (Extended) BASIC programs.

First-time xdt99 users running Windows will find additional information about
installation and getting started in the [Windows tutorial][5].  Users of other
platforms who are unfamiliar with the command line may also benefit from that
guide.


Basic Usage: `xas99`                                        <a name="xas99"></a>
--------------------

This is just a brief overview of the most common usages for `xas99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the [manual][4]
included with xdt99.

Generate object code for the Editor/Assembler cartridge, option 3:

    $ xas99.py [-R] [-C] <source file>

Generate program image for the Editor/Assembler cartridge, option 5:

    $ xas99.py -i [-R] <source file>

Generate cartridge file for the MESS emulator:

    $ xas99.py -c [-R] <source file>

Generate program image embedded in Extended BASIC loader:

    $ xas99.py --embed-xb <source file>

Generate raw binary data files:

    $ xbas99.py -b [--base <addr>] <source file>

Generate list file showing assigned addresses and generated data:

    $ xas99.py <source file> -L <list file>

For a complete overview of the available command-line options, see `xas99.py
-h`.

`xas99` offers various language extensions to the original Editor/Assembler
module:

 * Relaxed syntax (e.g., labels, comments, whitespace, case insensitivity)
 * Improved expressions (e.g., Boolean operators, binary numbers, parentheses)
 * Label continuations and local labels (e.g., `! dec r0; jne -!`)
 * New directives (e.g., `BCOPY`, `XORG`, `SAVE`)
 * Conditional assembly (e.g., `.ifdef`)
 * Macros (`.defm`)

Please refer to the [xdt99 manual][4] for a detailed description of these
features.


Basic Usage: `xga99`                                        <a name="xga99"></a>
--------------------

This is just a brief overview of the most common usages for `xga99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Assemble GPL source file into GPL byte code:

    $ xga99.py <source file>

Generate image file for GROM/GRAM device:

    $ xga99.py -i <source file>

Generate cartridge file for the MESS emulator:

    $ xga99.py -c <source file>

Assemble source file using "RAG GPL Assembler" syntax style:

    $ xga99.py <source file> -s rag

For a complete overview of the available command-line options, see `xga99.py
-h`.

`xga99` offers various language extensions similar to `xas99`:

 * Relaxed syntax (e.g., labels, comments, whitespace, case insensitivity)
 * Conditional assembly (e.g., `.ifdef`)
 * Macros (`.defm`)

Please refer to the [xdt99 manual][4] for a detailed description of these
features.


Basic Usage: `xbas99`                                      <a name="xbas99"></a>
---------------------

This is just a brief overview of the most common usages for `xbas99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

List TI BASIC or TI Extended BASIC program on screen:

    $ xbas99.py -l <program file>

Decode BASIC program to source format (i.e., list to file):

    $ xbas99.py -d <program file> [-o <output file>]

Create BASIC program for interpreter from source listing:

    $ xbas99.py [-c] <source file> [-o <output file>]

List BASIC program stored on disk image (advanced use):

	$ xdm99.py <disk image> -p <prog name> | xbas99.py -l -

For a complete overview of the available command-line options, see `xbas99.py
-h`.

`xbas99` also offers some advances features:

 * Automatically joining split lines (i.e., "type-in listing mode")
 * Using labels instead of line numbers

Please refer to the [xdt99 manual][4] for a detailed description of these
features.


Basic Usage: `xda99`                                        <a name="xda99"></a>
--------------------

Since `xda99` and `xdg99` are very similar, this short description applies to
both tools.

This is just a brief overview of the most common usages for `xda99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the [manual][4]
included with xdt99.

Disassemble binary top-down:

    $ xda99.py <binary file> -d -a <bin addr> [-f <from addr>]

Disassemble with run simulation:

    $ xda99.py <binary file> -a <bin addr> [-f <from addr>]

Disassemble with run simulation and additional starting points:

    $ xda99.py <binary file> -a <bin addr> -r <addr> [...]

Disassemble using a list of symbols:

    $ xda99.py <binary file> -a <bin addr> -S <symbol file>

For a complete overview of the available command-line options, see `xda99.py
-h`.


Basic Usage: `xdm99`                                        <a name="xdm99"></a>
--------------------

This is just a brief overview of the most common usages for `xdm99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Print disk catalog on screen:

    $ xdm99.py <disk image>

Extract one or more files from disk image to local file system:

    $ xdm99.py <disk image> -e <file> ...

Extract files in TIFiles or v9t9 format:

    $ xdm99.py <disk image> -t -e <file> ...
    $ xdm99.py <disk image> -9 -e <file> ...

Print file contents to screen:

    $ xdm99.py <disk image> -p <file> ...

Add local files to disk image:

    $ xdm99.py <disk image> -a <file> ... [-f <format>] [-n <name>]

Rename file on disk image:

    $ xdm99.py <disk image> -r <old name>:<new name> ...

Delete file on disk image:

    $ xdm99.py <disk image> -d <file> ...

Convert TIFiles files or v9t9 files to plain files:

    $ xdm99.py -F <TIFiles file> ...
    $ xdm99.py -F <TIFiles file> ... -9

Convert plain files to TIFiles files or v9t9 files:

    $ xdm99.py -T <plain file> ... [-f <format>] [-n <name>]
    $ xdm99.py -T <plain file> ... -9 [-f <format>] [-n <name>]

Print contents of TIFiles file:

    $ xdm99.py -P <TIFiles file>

Initialize blank disk:

    $ xdm99.py <disk image> --initialize <size> [-n <name>]

Resize disk image:

    $ xdm99.py <disk image> -Z <sectors>

Repair disk image with corrupt files or other inconsistencies:

    $ xdm99.py -R <disk image>

Override disk geometry:

    $ xdm99.py <filename> --set-geometry <geometry>

Print sector dump:

    $ xdm99.py <disk image> -S <sector>

For a complete overview of the available command-line options, see `xdm99.py
-h`.


Basic Usage: `xhm99`                                        <a name="xhm99"></a>
--------------------

This is just a brief overview of the most common usages for `xhm99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Convert disk image to HFE image:

    $ xhm99.py -T <disk image> [-o <HFE image>]

Convert HFE image to disk image:

    $ xhm99.py -F <HFE image> [-o <disk image>]

Show disk catalog:

    $ xhm99.py <HFE image>

Additionally, `xhm99` supports all commands of `xdm99`.

Add or remove files to/from image:

    $ xhm99.py <HFE file> -a <files> ... [-n <name>] [-f <format>] [-t | -9]
    $ xhm99.py <HFE file> -e <files> ...

Create new image (and add a file to it):

	$ xhm99.py <HFE file> -X <size> [-a <files> ...]

Resize image (e.g., DSDD/40T to DSSD/80T):

    $ xhm99.py <HFE file> -Z <size>

For a complete overview of the available command-line options, see `xhm99.py
-h`.


Basic Usage: `xvm99`                                        <a name="xvm99"></a>
--------------------

This is just a brief overview of the most common usages for `xvm99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Show information about volumes:

    $ xvm99.py <device> <volumes>

Read disk images from volumes:

    $ xvm99.py <device> <volumes> -r <filename> [--keep-size]

Write disk image to volumes:

    $ xvm99.py <device> <volumes> -w <disk image> [--keep-size]

`<device>` is the platform-specific name of the Compact Flash card drive, e.g.,
`/dev/sd<X>` on Linux, `/dev/Disk<X>` on Mac OS X, or `\\.\PHYSICALDRIVE<X>` on
Windows.

`<volumes>` is a single value or a combination of values and ranges, e.g.,
`1,3-4,6-10`.  If more than one volume is supplied, the same command is applied
to *all* volumes.

Additionally, `xvm99` extends most of the functionality of `xdm99` to disk
volumes.

Print disk catalog of one or more volumes:

    $ xvm99.py <device> <volumes> -i

Add file to one or more volumes:

    $ xvm99.py <device> <volumes> -a <file> [-n <name>] [-f <format>] [-t | -9]

For a complete overview of the available command-line options, see `xvm99.py
-h`.


Contact Information
-------------------

The xdt99 tools are released under the GNU GPL, in the hope that TI 99
enthusiasts may find them useful.

Please email all feedback and bug reports to the developer at <r@0x01.de>.


[1]: https://endlos99.github.io/xdt99
[2]: https://github.com/endlos99/xdt99/releases
[3]: https://github.com/endlos99/xdt99
[4]: https://github.com/endlos99/xdt99/blob/master/doc/MANUAL.md
[5]: https://github.com/endlos99/xdt99/blob/master/doc/WINDOWS.md
[6]: https://www.python.org/downloads/
[7]: https://endlos99.github.io/xdt99/emacs.html
[8]: https://endlos99.github.io/xdt99/idea.html
