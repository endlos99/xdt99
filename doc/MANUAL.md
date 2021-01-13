xdt99: TI 99 Cross-Development Tools
====================================

The **TI 99 Cross-Development Tools** (xdt99) are a suite of programs that
facilitate the development of programs for the TI 99 family of home computers
and other TMS9900-based systems on modern computer systems.

As of this release, the cross-development tools comprise

 * [`xas99`](#xas99), a TMS9900 cross-assembler,
 * [`xga99`](#xga99), a GPL cross-assembler,
 * [`xda99`](#xda99), a TMS9900 disassembler,
 * [`xdg99`](#xdg99), a GPL disassembler,
 * [`xbas99`](#xbas99), a TI BASIC and TI Extended BASIC encoder and decoder,
 * [`xdm99`](#xdm99), a disk and file manager,
 * [`xhm99`](#xhm99), a manager for HFE images used by HxC floppy drives, and
 * [`xvm99`](#xvm99), a volume manager for nanoPEB/CF7+ Compact Flash cards.

All programs are written in Python and thus run on any platform that Python
supports, including Linux, Windows, and macOS.

Additionally, xdt99 provides TI-specific editor support for some freely
available development environments:

 * `xdt99-mode`, a major mode for the GNU Emacs text editor, and
 * `xdt99 IDEA`, a plugin for the IntelliJ IDEA development environment.

The plugins offer syntax highlighting, source navigation, and semantic renaming
for assembly, GPL, and TI (Extended) BASIC programs.  Note, however, that both
plugins currently support an older version of the `xas99` syntax.

To get started, follow the [installation](#installation) instructions and read
the [tutorial](#tutorial).

xdt99 is released under the GNU GPL version 3.  The latest [binary release][3]
as well as all [sources][2] are available on GitHub.

The [xdt99 homepage][1] always hosts the latest version of this document.


Installation                                         <a name="installation"></a>
------------

The latest xdt99 [binary release][3] is available on GitHub.  Experienced users
may also clone the [xdt99 repository][2] instead.  The repository contains some
additional test cases that are useful when extending or modifying xdt99.

xdt99 requires a working installation of [Python 3.6][5] or later.  On most
Linux systems, Python is available as a package.  For other platforms, we
recommend installing the latest stable Python 3 release.  Please note that xdt99
will not run on Python 2.

All xdt99 files should be placed somewhere in the `$PATH` or where the
command-line interpreter will find them.  Windows users will find Windows-
specific instructions in the [Windows Guide][4].

Additionally, the `ide/` directory contains the editor plugins for GNU Emacs
and IntelliJ IDEA.  Please refer to the `ide/README.md` file for further
information about editor support.

The `example/` directory contains some sample files that are used throughout
this manual.


Tutorial                                                 <a name="tutorial"></a>
--------

The xdt99 tools lack a graphical user interface, and use the command line
instead.  While this choice will undoubtedly steepen the learning curve for some
users, the command line is ultimately very suited for repetitive tasks, as
encountered while developing assembly and GPL programs.

This section contains a hands-on introduction to using xdt99 to assemble
programs, work with disk images and files, and run the results in an emulator
and on real iron.

Commands to be typed in by the user are prefixed by `$`.  If necessary, an
additional Windows command prefixed by `>` is shown (for an example, see the
[Windows Guide][4]).  The sample outputs shown here originate from a Linux
system and may look slightly different on other platforms.

For all examples, we use files in the `example/` directory distributed with
xdt99.


### Using the Cross-Assembler

The file `ashello.asm` contains a simple assembly program in classic syntax.
When using the `xas99` _cross-assembler_ in base mode, it translates source code
into _object code_. 

    $ xas99.py -R ashello.asm

This command creates a new file `ashello.obj`.  It also issues a warning about
unresolved references

    > --- <L> **** -
    ***** Warning: Unresolved references: VSBW, VMBW, KSCAN, VWTR

which we can ignore for now.  In fact, we will hide warnings from now on, unless
we want to discuss them.

The `-R` is a so-called _option_ that tells `xas99` to use registers with an
`R` prefix instead of plain numerical values, just like the `R` option of the
Editor/Assembler.
  
Invoking `xas99` without any arguments
 
    $ xas99.py
    usage: xas99.py [-h] [-b | -i | -c | -t [<format>] | --embed-xb]
                    [-l <file> [<file> ...] | -ll <file> [<file> ...]] [-5] [-18]
                    [-s] [-n <name>] [-R] [-C] [-L <file>] [-S] [-E <file>] [-q]
                    [-a <addr>] [-I <paths>] [-D <sym=val> [<sym=val> ...]]
                    [-o <file>]
                    [<source> [<source> ...]]
    xas99.py: error: One of <source> or -l/-ll is required.

lists all available options and their expected parameters, if any.  Options
enclosed in brackets `[` ... `]` are optional, and options separated by `|` are
mutually exclusive.

The help option `-h` also lists all available options, but includes a short
description for each.

    $ xas99.py -h
    ...
    TMS9900 cross-assembler, v3.0.0

    positional arguments:
      <source>              assembly source code(s)
    
    optional arguments:
      -h, --help            show this help message and exit
      -b, --binary          create program binaries
    ...

Each option has a short form and a long form, e.g., `-h` and `--help`, which may
be used interchangeably.

As we can see, some options take one or more additional arguments.  Arguments
are strings, e.g., for `-L`, or numerical, e.g., for `-a`.  Numerical arguments
may be decimal or hexadecimal if prefixed by `>` or `0x`.  Note that the `>`
character is used for output redirection on all platforms, so the entire
argument needs to be quoted, e.g.,

    $ xas99.py -R -a ">2000" ashello.asm

If an option can take more than one argument, such as `-D`, they are separated
by spaces.

    $ xas99.py sample.asm -D x=1 y=2 z=3

If an option is shown as `-x <arg> [<arg> ...]` in the usage help, we know that
it takes one or more arguments.
  
The order of options and any other parameters such as `ashello.asm` is
generally not important, but any arguments must always stay together with their
option.  There is, however, one caveat, which we will discuss later.

Coming back to the assembly run (let's rerun it without `-a`)
 
    $ xas99.py -R ashello.asm

the resulting file `ashello.obj` contains uncompressed object code, which looks
like this:

    $ cat ashello.obj
    > type ashello.obj
    0007EASHELLO A0000B100DB4845B4C4CB4F20B574FB524CB4420B2020B68697F19FF       0001
    A0012B7420B616EB7920B6B65B7921B0300B0000B02E0B8300B04C0B02017F2F9F          0002
    A0028B2A20B0202B0300B0420B0000B0580B0602B16FBB0200B0043B02017F336F          0003
    A003EC0002B0202B001AB0420B0000B0208BFF00B04C9B0300B0002B10007F31FF          0004
    A0054B0300B0000BD809B837CBD809B8374B0420B0000B9220B8375B13F97F2D4F          0005
    A006ABD020B8375B0980B0240B000FB0260B0700B0420B0000B10E87F410F               0006
    5001CSTART 30030VSBW  30046VMBW  3007AVWTR  30062KSCAN 7F2F8F               0007
    :       xdt99 xas                                                           0008

We can load this file with the Editor/Assembler cartridge using option 3, or
alternatively with the TI Extended BASIC module using the `CALL LOAD`
statement.

Uncompressed object code is not an efficient program format, though.  If
compatibility with Extended BASIC is not required, generating _compressed
object code_ with option `-C` reduces both size and loading time:

    $ xas99.py -R -C ashello.asm -o ashello-c.obj

In order to not overwrite our already existing `ashello.obj` file, we overrode
the default output filename with the output option `-o`.
 
Compressed object code contains unprintable characters, but if we replace those
by `.`, we can show the contents:

    ..~ASHELLO A..B..BHEBLLBO BWOBRLBD B  BhiBt BanBy BkeBy!B..B..B..B..B..B..B* F
    A.*B..B..B. B..B..B..B..B..B.CB..C..B..B..B. B..B..B..B..B..B..B..B..B..B..F
    A.ZB.|B..B.tB. B..B. B.uB..B. B.uB..B.@B..B.`B..B. B..B..F
    5..SLOAD 5..SFIRST5.~SLAST 5..START 3.zVWTR  F
    3.FVMBW  3.0VSBW  3.bKSCAN F
    :       xdt99 xas 

Comparing both object files, we see that the size of the compressed version is
only about three fifths of that of the uncompressed file:

    $ ls -l ashello*.obj
    > dir ashello*.obj
    -rw-rw---- 1 ralph ralph 400 Jul 12 09:58 ashello-c.obj
    -rw-rw---- 1 ralph ralph 640 Jul 12 09:58 ashello.obj

As stated above, `ashello.asm` uses classic syntax, i.e., the syntax used by
the Editor/Assembler.  `xas99` also supports a modern, more relaxed syntax,
which allows for lowercase, additional whitespace, and longer labels, and
features new directives and a preprocessor with conditional assembly and macros.

For an example of the new syntax, please refer to file `ashello_new.asm`, which
yields the same object code as `ashello.asm`.

The list file or _listing_ provides insight into the assembled program by
showing where each assembled instruction is placed in memory.  List files are
thus particularly useful during development.

Similar to the Editor/Assembler, we create list files using the list option
`-L`, followed by a filename:

    $ xas99.py -R ashello.asm -L ashello.lst

This command yields a text file `ashello.lst` that begins like this:

    XAS99 CROSS-ASSEMBLER   VERSION 3.0.0
         **** ****     > ashello.asm
    0001               *  HELLO WORLD
    0002
    0003                      IDT 'ASHELLO'
    0004
    0005                      DEF SLOAD,SFIRST,SLAST,START
    0006                      REF VSBW,VMBW,VWTR
    0007                      REF KSCAN
    0008
    0009 0000 100D  14        JMP  START
    0010
    0011      8300     WRKSP  EQU  >8300
    0012      8374     KMODE  EQU  >8374
    0013      8375     KCODE  EQU  >8375
    0014      837C     GPLST  EQU  >837C
    0015
    0016 0002 4845     MESSG  TEXT 'HELLO WORLD'
         0004 4C4C
         0006 4F20
         0008 574F
         000A 524C
         000C 44
    0017 000D   20            TEXT '   hit any key!'
         000E 2020
         0010 6869
         0012 7420
         0014 616E
         0016 7920
         0018 6B65
         001A 7921
    0018      001A     MESSGL EQU  $-MESSG
    0019
    0020 001C 0300  24 START  LIMI 0
         001E 0000
    0021 0020 02E0  18        LWPI WRKSP
         0022 8300
    ...

The four columns before the source code show

 * the source line number,
 * the memory address,
 * the generated contents for that address, and
 * the number of cycles required to execute the instruction (under some
   assumptions).

Some directives such as `EQU` do not generate machine code, so their second and
third columns may be missing or show different information.

For more complex programs with `COPY` and/or macros, source indicators show to
which source file a certain listing sequence belongs to:

   XAS99 CROSS-ASSEMBLER   VERSION 3.1.0
        **** ****     > asmacs.asm
        ...
        **** ****     > MAC0
        ...
        **** ****     > DSK2.ASCOPY3
        ...
                      < MAC0
        ...
                      < asmacs.asm
        ...

In addition to option 3 object code, `xas99` can also generate _images_ for E/A
option 5 using the image option `-i`.

    $ xas99.py -R -i ashello.asm -o ashello5.img

Again, we override the default output name `ashello.img`, for later.  The
resulting image file `ashello5.img` has 248 bytes and contains binary data.

    $ ls -l ashello5.img
    > dir ashello5.img
    -rw-rw---- 1 ralph ralph 132 Jul 12 13:11 ashello5.img

To view the binary data, we can create a _hexdump_ of the file.

    $ hexdump -C ashello5.img
    > Format-Hex ashello5.img            (using Powershell version 5 or higher)
    00000000  00 00 00 84 a0 00 10 0d  48 45 4c 4c 4f 20 57 4f  |........HELLO WO|
    00000010  52 4c 44 20 20 20 68 69  74 20 61 6e 79 20 6b 65  |RLD   hit any ke|
    00000020  79 21 03 00 00 00 02 e0  83 00 04 c0 02 01 2a 20  |y!............* |
    00000030  02 02 03 00 04 20 00 00  05 80 06 02 16 fb 02 00  |..... ..........|
    00000040  00 43 02 01 a0 02 02 02  00 1a 04 20 00 00 02 08  |.C......... ....|
    00000050  ff 00 04 c9 03 00 00 02  10 00 03 00 00 00 d8 09  |................|
    00000060  83 7c d8 09 83 74 04 20  00 00 92 20 83 75 13 f9  |.|...t. ... .u..|
    00000070  d0 20 83 75 09 80 02 40  00 0f 02 60 07 00 04 20  |. .u...@...`... |
    00000080  00 00 10 e8                                       |....|

The first column shows the byte offset of the line, the wide second column
shows the byte values, and the third column shows the textual representation of
the bytes, where non-printable characters are shown as `.`.  All values are in
hexadecimal.

For reasons explained in section _E/A Utility Functions_, this file will might
crash when run.  `xas99` even reminds us that some utility functions are
missing.

    > --- <L> **** -
    ***** Warning: Unresolved references: VSBW, VMBW, KSCAN, VWTR

We can ignore this warning only for object code, i.e., for E/A option 3
programs.  To add the missing functions to our image, we need to assemble with
this command:

    $ xas99.py -R -i ashello.asm vsbw_ea.asm vmbw_ea.asm vwtr_ea.asm kscan_ea.asm

The additional files provide the unresolved symbols.  Thus, our revised command
does not print any warnings.

Another, more common way to provide required E/A utility functions is to `COPY` 
them in the source code.  For example, we could modify `ashello.asm` to look
like

    ...
           ORI  R0,>0700
           BLWP @VWTR
    
           JMP  NEXT

           COPY "vsbw_ea.asm"          |
           COPY "vmbw_ea.asm"          |   add these lines
           COPY "vwtr_ea.asm"          |   to provide utilities
           COPY "kscan_ea.asm"         |
           
           END

Note that both methods, command line files and `COPY`, yield identical output
files.

#### Using Emulators and Real Iron

To run either of the generated programs with the MAME emulator, we require a
disk image containing these files.  We can create this image (and more) with
the xdt99 _Disk Manager_ `xdm99`.

The `example/` directory contains an empty SS/SD image `work.dsk` that we will
use.  Invoking `xdm99` with the disk image filename displays the disk
properties and contents.

    $ xdm99.py work.dsk
    WORK      :     2 used  358 free   90 KB  1S/1D 40T  9 S/T
    ----------------------------------------------------------------------------
    
We see that the disk image with the name `WORK` has 2 used and 358 free sectors,
has a capacity of 90 KB and is a formatted as one-sided, single density with 40
tracks and 9 sectors per track.  Note that 2 sectors are always reserved for
disk information and the catalog.

We can _add files_ to the disk image with the add option `-a`, generally
together with the format option `-f`.

    $ xdm99.py work.dsk -a ashello.obj -f DIS/FIX80
    $ xdm99.py work.dsk -a ashello5.img

The format is one of the known TI file formats and may be specified rather
loosely, e.g., `INTVAR 254`, `DF80`, `PROGRAM`, `P`, etc.  If we use a space in
the format, we need to quote it, e.g., `-f "D/F 80"`.

If no format is given, `PROGRAM` type is assumed, and if the record length is
omitted, a record length of 80 is used.

If we add a single file to a disk image, we can also override the TI filename
on the disk with the name option `-n`.

Our disk image now contains two files:

    $ xdm99.py work.dsk
    WORK      :     8 used  352 free   90 KB  1S/1D 40T  9 S/T
    ----------------------------------------------------------------------------
    ASHELLO       4  DIS/FIX 80     672 B   8 recs     2020-03-25 12:13:22 C
    ASHELLO5      2  PROGRAM        248 B              2020-03-25 12:13:26 C

Should we have no blank disk image available, we can create a _new image_ with
the initialize option `-X`:

    $ xdm99.py -X sssd work.dsk

The disk size can be descriptive like `SSSD`, `2s/2d`, `1s1d80t`, or `CF`, or
explicit by specifying the number of sectors, e.g., `720`.  The maximum size
for a disk image is 1600 sectors. 

We can also combine the creation of a new image, and the addition of files into
a single operation.

    $ xdm99.py -X sssd work.dsk -a ashello.obj -f df80
    $ xdm99.py work.dsk -a ashello5.img

It's possible to list multiple files after the `-a` option if they all share the
same file type.  This is not the case here, though, so we need two commands to
accomplish our task.

We can use this disk with MAME to load our files with an emulated Editor/
Assembler cartridge.  (Make sure to type all of this in one line!)

    $ mame64 ti99_4a -ioport peb -ioport:peb:slot2 32kmem -ioport:peb:slot8 hfdc
             -ioport:peb:slot8:hfdc:f1 525dd -cart EA.rpk -flop1 work.dsk

You'll probably need to adjust the name of the Editor/Assembler cartridge image
`EA.rpk` to match your installation.  Alternatively, we could load both E/A and
the disk image using the MAME UI.

In the emulated Editor/Assembler, we select option 3, `LOAD AND RUN`, and enter
the name of the object code file at the `FILE NAME?` prompt:

    DSK1.ASHELLO

Once the loader finishes, we type `START` at the `PROGRAM NAME?` prompt.  The
words `HELLO WORLD` should appear on screen.  Pressing any key will change the
color of the screen border.

Next, we quit the program by hitting `FCTN-=` and start Editor/Assembler again.
We now select option 5, `RUN PROGRAM FILE`, and enter the name of our image
file,

    DSK1.ASHELLO5

The program will start automatically.  To quit MAME, press Esc; if that does not
work, press ScrLock and then Esc.

If we want to use the Classic 99 emulator, we could also use our disk image,
even though the emulator cannot write to disk images.  The native format of
Classic 99 are so-called _files in a directory_ (FIAD) in _TIFILES_ format.

`xdm99` can convert plain files and files on disk images into TIFILES format by
using the TIFILES options `-T` and `-t`, resp.  

For plain files, `-T` converts one or more files into TIFILES format.  Unless we
are creating files of type `PROGRAM`, we also have to provide the file type
option `-f`.

    $ xdm99.py -T ashello5.img
    $ xdm99.py -T ashello.obj -f DIS/FIX80
    $ ls -l *.tfi
    > dir *.tfi
    -rw-rw---- 1 ralph ralph 384 Mär 25 18:31 ashello5.img.tfi
    -rw-rw---- 1 ralph ralph 896 Mär 25 18:31 ashello.obj.tfi

By default, the converted files will have an additional `.tfi` extension.  In
our case, we want upper-case filenames without extension for Classic 99, so
we're using the `-o` option again.
 
    $ xdm99.py -T ashello.obj -f DIS/FIX80 -o ASHELLO
    $ xdm99.py -T ashello5.img -o ASHELLO5

We can examine the stored metadata of TIFILES or v9t9 files by using the info
option `-I`.

    $ xdm99.py -I ASHELLO
    ASHELLO       4  DIS/FIX 80     672 B   8 recs     2020-03-25 18:32:24 C

To convert in the other direction, we use the "from TIFILES" option `-F`:

    $ xdm99.py -F ASHELLO -o ashello.obj

The conversion becomes even simpler if we use our disk image instead of plain
files.  The _extract_ option `-e` will create a local copy of a file stored on
the disk image.  If we combine `-e` with the TIFILES option `-t`,  the local
file will be in TIFILES format.

    $ xdm99.py work.dsk -t -e ASHELLO -o ASHELLO
    $ xdm99.py work.dsk -t -e ASHELLO5 -o ASHELLO5

To convert in the other direction, we still use `-t`, but combine it with the
add option `-a`.  This implies that we should use plain files for disk images
and TIFILES format for files not stored in disk images.

Note that when using options that accept more than one argument, such as `-a`
or `-e`, the position of non-option arguments such as `work.dsk` becomes
important.  For example, if we rewrote the previous command into

    $ xdm99.py -t -e ASHELLO ASHELLO5 work.dsk

`xdm99` would not know that `work.dsk` is our disk image instead of another file
to extract.  Thus, always keep multi-argument options after any non-options,
like we do in this manual.

We can now copy both files `ASHELLO` and `ASHELLO5` into the `DSK1` directory
of Classic 99, start the emulator, and select the Editor/Assembler from the
menu.  All further steps are then similar to the MAME description above.

If we want to run our sample programs on a real TI 99 using the nanoPEB/CF7+ or
the HxC floppy emulator, we need to transfer our disk image to a CF or SD card
first.  In the case of the nanoPEB/CF7+, we use the `xvm99` _volume manager_.

    $ xvm99.py /dev/sdc 2 -w work.dsk

Assuming a CF card is connected to our computer, this command will store the
disk image `work.dsk` as volume 2, where it can be accessed on the TI 99 with
`CALL MOUNT(n,2)`.

The `/dev/sdc` is the Linux device the CF card is connected to on our computer.
To get the name of the device to use on a Linux machine, we can use the
`fdisk -l` command, but we need some experience to identify the CF card.

If we're running Gnome or KDE, we can also mount the CF card and then view the
card properties.  With KDE, the device name is listed under `Mounted from`.

On macOS systems, the `diskutil list` lists all devices.  We pick the device
name from the first column.

For Windows systems, we can use the `wmic` command (no admin rights required):

    > wmic diskdrive list brief
    Caption                            DeviceID            Model                      ...
    VBOX HARDDISK ATA Device           \\.\PHYSICALDRIVE0  VBOX HARDDISK ATA Device   ...
    Generic- Compact Flash USB Device  \\.\PHYSICALDRIVE2  Generic- CF USB Device     ...
    Generic- SD/MMC USB Device         \\.\PHYSICALDRIVE1  Generic- SD/MMC USB Device ...
    Generic- xD-Picture USB Device     \\.\PHYSICALDRIVE3  Generic- xD USB Device     ...   
    
Here, we see that the USB CF Card reader is connected to `\\.\PHYSICALDRIVE2`.

We can also transfer single files if the target volume already contains a disk
image.  To check this, we can get the status of a volume by invoking `xvm99`
without options.  If there is no image, we get

    $ xvm99.py /dev/sdc 2
    [   2]  (not a valid disk image)

If volume 2 contains a valid disk image, we will see a short summary instead.

    [   2] PROGRAMS3 :  1248 used   352 free

In the latter case we can add files to a volume by using the same syntax as for
`xdm99`.

    $ xvm99.py /dev/sdc 2 -a ashello.obj -f DIS/FIX80
    $ xvm99.py /dev/sdc 2 -a ashello5.img

Either way, our two programs are now available in volume 2 and can be loaded on
a TI 99 with a nanoPEB or CF7+.

Note that the volume can also be a list, e.g., `1,3` or a range, e.g., `1-3`.
Any commands are then applied to all volumes specified.  For example,

    $ xvm99.py /dev/sdc 1,3-5 -a LICENSE -f DV80
    
will add the file `LICENSE` to volumes 1, 3, 4, and 5, assuming that each volume
contains a valid disk image.

For a HxC drive made by Lotharek, we need to convert the disk image to HFE
format.  This is the job of the `xhm99` _HFE image manager_.

To convert a disk image to HFE format, we use the "to HFE" option `-T`.

    $ xhm99.py -T work.dsk

yields the HFE file `work.hfe` which we can copy onto an SD card and then
insert that into the HxC drive.

We can also check the contents of our HFE disk ty typing

    $ xhm99.py work.hfe
    WORK      :     8 used  352 free   90 KB  1S/1D 40T  9 S/T
    ----------------------------------------------------------------------------
    ASHELLO       4  DIS/FIX 80     672 B   8 recs     2020-03-25 12:13:22 C
    ASHELLO5      2  PROGRAM        248 B              2020-03-25 12:13:26 C

To convert in the other direction, we would use the "from HFE" option `-F`.

#### Other Cross-Assembler Formats

After this foray into managing disks and files of various formats, let's return
to `xas99` now.  The cross-assembler not only generates code for the
Editor/Assembler cartridge, but also raw binary code and MAME-style cartridges,
which can be used independently of E/A.

The cartridge option `-c` automatically generates a GPL header and then
assembles everything into a MAME-style cartridge RPK archive.

    $ xas99.py -R -c ascart.asm -n "HELLO CART"

Note that `ascart.asm` does not make use of VDP utilities, so we don't have to
include them on the command line.

The name option `-n` sets the program name that shows up in the TI menu screen.
Since our name contains a space, we need to quote the entire name.  If no name
is given, the filename without extension is used.

In order to add the GPL header, the source program must not use memory range
`>6000` to `>6030`.  We can ensure this by using either an `AORG >6030` or
higher directive or an `RORG` directive at the beginning of the program.  In
case of using `RORG`, `xas99` automatically relocates the code to address
`>6030`.
  
Additionally, the first instruction of the original source code must be
executable, just like for option 5 programs, unless the program uses an `END`
directive with label, pointing to the start address (see `ascart.asm`).

As an aside note, we can manually relocate the relocatable segments of a program
with the rebase option `-a`.  Thus, if a program is placed with only `RORG`, we
can use `-a` to move it to any memory address.
 
The resulting file with extension `.rpk` can be used as-is with the MAME
emulator:

    $ mame64 ti99_4a -cart ascart.rpk

In MAME, the TI menu screen will show `2 HELLO CART`, and pressing 2 will run
the (trivial) sample program.  Note that the programs runs without the 32K
memory expansion, as the program code is stored entirely inside the cartridge
ROM.

Generating cartridge images with option `-c` is recommended only for very
simple programs, since the capabilities of the generated GPL header are limited,
and the resulting `.rpk` file can only be used for MAME.

A more general approach is to write the GPL header yourself and then to assemble
the program with the binary option `-b`.

    $ xas99.py -R -b ascart_hdr.asm

The resulting binary file `ascart_hdr.bin` corresponds to an "executable" on
other platforms and contains only machine code, without any headers or padding.
It can be used as cartridge file for Classic 99, or put on a multi-cart or Flash
cart such as the FlashROM or the [FinalGROM][6].

The `-b` option is not limited to cartridges.  We can also use it to create
DSRs, or code we want to load dynamically into memory, e.g., by DSR opcode 5.
We can put the binaries in an EPROM, or store them in a microcontroller or FPGA.
As such, binary is arguably the simplest, and most versatile format.

#### E/A Utility Functions

As we now know how to assemble programs into various formats, we should briefly
discuss the use of E/A utility functions in each case.  These functions, such as
`VSBW`, `VMBR`, or `VWTR` simplify the access to VDP memory and are thus used in
most assembly programs. 

When creating object code for E/A option 3, the Editor/Assembler provides all
utilities listed in the E/A manual automatically.  To use any function, we only
need to import its name with a `REF` directive, and can then call the function
with `BLWP`.

    ref  vsbw
    ...
    li   r0, 160
    li   r1, >4000
    blwp @vsbw

Remember the warning we got when assembling `ashello.asm`?  That was because we
`REF`ed utility `VSBW`, but the function was not part of our code.  In case of
option 3, this is fine, as the function is actually provided by E/A itself. 
    
For other output formats, including E/A option 5, E/A does _not_ supply
utilities, so we must include them in our program.  For this, `xas99` provides
a variety of utilities in the `lib/` directory.  To use any function, we must
`COPY` it into our source, and can then call it with `BL`.

    li   r0, 160
    li   r1, >4000
    bl   @vsbw
    ...
    copy "vsbw.asm"

Note that `COPY` will automatically search the `lib/` directory, so we don't
need to include the `lib/` path with `-I`.

An alternative way to use functions from `lib/` is to reference their names in
the code

    ref  vsbw
    ...
    li   r0, 160
    li   r1, >4000
    bl   @vsbw
    
and then include their source files on the command line:

    $ xas99.py -R -i program.asm vsbw.asm

As the name of the resulting file is the name of the first source file given, we
should keep our main program before any utilities.  `xas99` will search for
sources automatically in the `lib/` directory, so we don't need to provide the
full path for `vsbw.asm`.

In the examples above, we used some E/A-compatible functions, which are still
called by `BLWP`.  We can identify these functions in `lib/` by their `_ea`
suffix.  Just as the original E/A utilities, these `_ea` functions use `>2094`
as their workspace base.

The `lib/` directory also contains some functions not provided by E/A, such as
`VWWT` or `VMZW`.  Please refer to `lib/README.md` for a description of each
function.

#### Linker

The last `xas99` feature we want to cover here is _linking_.  The linker is an
optional part of `xas99` that will join multiple object code files together.  In
this process, the linker will find a memory layout for all program segments, and
match the list of `REF` symbols with the list of `DEF` symbols.

To invoke the linker and join multiple object code files together, we use the
link option`-l`.

    $ xas99.py -l part1.obj part2.obj -o whole.obj

We can choose any output format for the linked code, i.e., we can combine `-l`
with `-b`, `-i`, `-c`, `-t`, or none of those if we want to keep the object code
format.

We can also link some object code files to the assembled results of some source
files.  In fact, if `part1.obj` and `part2.obj` are the object code files of
source files `part1.asm` and `part2.asm`, resp., then these three commands are
equivalent and yield three identical files `whole.obj`.

    $ xas99.py -l part1.obj part2.obj -o whole.obj
    $ xas99.py part1.asm -l part2.obj -o whole.obj
    $ xas99.py part1.asm part2.asm -o whole.obj

Note, however, that  

    $ xas99.py part2.asm -l part1.obj -o whole.obj

will yield a different file, since the order of files is preserved in the final
layout of `whole.obj`.  Also keep in mind that any files to the right of `-l`
must be object code files.

So what is the actual difference between joining object code files with `-l` and
joining source code files with `COPY`?  When joining sources, each source file
sees all the symbols of the other sources, which requires care to not create
symbol conflicts.  When joining object code, on the other hand, each unit only
sees the symbols exported by the other files exported with `DEF` and imported
with `REF`, limiting the chance of symbol conflicts.

For example, linking the object code of program 1

         def  s2, s3
    s1   equ  101
    s2   mov  r11, r10
         ...
         b    *r10
    s3   data >1234

and the object code of program 2

         ref s3
    s1   equ  202
    s2   mov  @s3, r0
         ...

does not create a symbol conflict, since `s1` is local to each program, `s2` is
not imported by program 2, and `s3` is only defined by program 1.

There is also a historical reason for favoring linking over copying.  With the
Editor/Assembler, for example, assembling takes much more time than linking.
Thus, it is more economical to break programs into small units so that during
development, we can make changes to only some units, assemble those units, and
link everything together, which is much faster than assembling everything for
every little change.

Luckily, with today's computers being unimaginably faster, we can choose either
method without worrying about performance.  Thus, it is merely a personal choice
which method we choose. 


### Creating GROM Cartridges

In this section, we use the `xga99` _GPL cross-assembler_ to assemble GPL
programs into cartridge images that run in any emulator or, with appropriate
hardware such as the [FinalGROM][6], on real hardware.

To get started, we use `xga99` to assemble the `gahello.gpl` GPL program from
the `examples/` directory:

    $ xga99.py gahello.gpl

The resulting file `gahello.gbc` contains _GPL byte code_, which corresponds to
the binary format created by `xas99.py` with the `-b` option.

    $ hexdump -C gahello.gbc
    > Format-Hex gahello.gbc             (using Powershell version 5 or higher)
    00000000  ff ff ff ff ff ff ff ff  00 00 00 00 00 00 00 00  |................|
    00000010  ff ff ff ff ff ff ff ff  34 46 6a ad dc c5 5e e3  |........4Fj...^.|
    00000020  34 46 6a ad dc c5 5e e3  63 38 00 80 0f 30 00 84  |4Fj...^.c8...0..|
    00000030  01 87 00 80 0f 82 00 84  01 d0 0c 12 12 0c 02 02  |................|
    00000040  0c 00 00 00 00 00 00 00  00 00 30 48 48 30 08 08  |..........0HH0..|
    ...
    00000150  ff 87 02 05 00 ff be 10  80 03 61 61 92 10 41 59  |..........aa..AY|
    00000160  00 0b                                             |..|
  
Note that `xga99` does not support relocatable code, and cannot create GPL
object code.

GPL byte code is the native format for GROMs, so we can use `gahello.gbc` right
away with the FinalGROM if we rename the file to something ending in `G`, for
example, `gahellog`.

Other hardware, such as the GRAM Kracker, also use GPL byte code files, but
additionally expect some header information `xga99` currently not provides.
 
For the MAME emulator, we cannot use `.gbc` files directly, but we can use them
to build an RPK cartridge archives.

Alternatively, `xga99` supports the creation of cartridges with automatically
generated GPL headers using the cartridge option `-c`:

    $ xga99.py -c gahello.gpl

Again, the memory area `>6000`-`>6030` is reserved for the generated GPL header.
To place code at some particular address, we use the `GROM` directive to choose
the GROM, and then optionally the `AORG` directive to define an offset relative
to the start of the GROM.  `GROM` supports both GROM numbers `0`, `1`, ..., `7`
and GROM base addresses `>0000`, `>2000`, ..., `>E000`.

The result of this command is a `.rpk` file we can use with MAME:

    $ mame64 ti99_4a -cart gahello.rpk

The emulated TI menu screen will show our program as `GAHELLO`.  We can override
that name with the name option `-n`.

Again, we recommend using `-c` only for simple cases, and working with GPL byte
code otherwise.

When we create GPL programs for the FinalGROM, we need to make sure to assemble
to GPL byte code and to rename the resulting `.gbc` file so that it ends in `G`
and has a `.bin` extension.  Otherwise, the FinalGROM will erroneously assume
that the file contains TMS9900 machine code.


### Working with BASIC Programs

TI BASIC and TI Extended BASIC programs are usually entered in listing format,
i.e., as text.  Internally, however, BASIC programs are stored in token format,
which is a binary format.  Disks and cassettes also store the internal format.

The `xbas99` BASIC tool can convert TI BASIC and TI Extended BASIC programs from
one format into the other format.

The TI BASIC program `nim.bas` in the `examples/` directory is in listing
format, just as if we typed it in from a home computer magazine from the 80s.
To convert this into a program we can load and run in TI BASIC, we must tokenize
the listing with the create option `-c`.

    $ xbas99.py -c nim.bas
    
To run the resulting file `nim.prg` in an emulator, we again create a disk image

    $ xdm99.py basic.dsk -X sssd -a nim.prg

and start the MAME emulator with it (again, as one line)

    $ mame64 ti99_4a -ioport peb -ioport:peb:slot8 hfdc 
             -ioport:peb:slot8:hfdc:f1 525dd -flop1 basic.dsk

In TI BASIC, we can then load and run our Nim program from `DSK1`.

    OLD DSK1.NIM
    RUN

It is important to know that `xbas99` performs a "dumb" translation from listing
to tokens -- it does __not__ perform a syntax check.  As an example, this
"program"

    10 CALL PRINT A="X" / INPUT 1,2,3
    20 LET IT BE

will tokenize with `-c` and load in TI BASIC (!) perfectly fine, but when we try
to `RUN` it, the interpreter will throw an error:

    * BAD NAME IN 10

When given a program in an internal format, such as our `nim.prg`, we can decode
it into a textual format with the decode option `-d`.

    $ xbas99.py -d nim.prg -o nim2.bas

Files `nim.bas` and `nim2.bas` should be identical.

We can also decode to `stdout`, i.e., print the decoded listing on the console
with the print option `-p`.

    $ xbas99 -p nim.prg
    100 REM A VERSION OF NIM
    110 PRINT :"THERE ARE 21 COINS ON THE"
    120 PRINT "TABLE."
    ...

Again, `-p <file>` is equivalent to `-d <file> -o -`.

`xbas99` does not distinguish between TI BASIC and TI Extended BASIC, so we must
be careful not to use TI Extended BASIC keywords when developing a TI BASIC
program.

#### Labels Replacing Line Numbers

`xbas99` also supports a more modern way to write BASIC programs.  Instead of
using line numbers for each line,

    210 X=X*2 :: Y=Y+1
    220 IF X<10 THEN 210
    230 ON Y GOTO 310,340,590
    ...
    310 REM DO THIS
    ...
    340 REM DO THAT
    ...
    590 END

we can use labels for each line that is the target of a branch:

    COUNT:
     X=X*2 :: Y=Y+1
     IF X<10 THEN @COUNT
     ON Y GOTO @DOTHIS,@DOTHAT,@DONE
    ...
    DOTHIS:
     REM DO THIS
    ...
    DOTHAT:
     REM DO THAT
    ...
    DONE:
     END

A label must be alphanumeric and followed by a colon `:`.  The actual program
lines must be indented by at least one blank.  Sadly, when using a label, e.g.,
as part of a `GOTO` statement, we must prefix the label with an `@` sign. 
The `@` prefix is needed to identify invalid, i.e., mistyped labels, or else
invalid labels would become stray variables.

In order to tokenize a program with labels, the label option `-l` must be
supplied.  `-l` can only be used together with `-c`.

    $ xbas99.py -c -l nim_labels.bas
    
Before tokenizing a program with labels, `xbas99` will apply line numbers to the
program similar to what the BASIC command `RESEQUENCE 100,10` would do.
Consequently, labels are not preserved in tokenized programs, so when we decode
a tokenized program with labels, we get line numbers back:

    $ xbas99.py -p nim_labels.prg
    100 REM A VERSION OF NIM
    110 PRINT :"THERE ARE 21 COINS ON THE"
    120 PRINT "TABLE."
    130 PRINT "BY TURNS, EACH PLAYER TAKES"
    ...

After tokenizing the program, `xbas99` reports any unused labels, i.e., labels
which are defined, but not used as targets.


### Automation

We stated in the introduction of this tutorial, command line tools like xdt99
are suited for automation.

Let's assume that we are developing an assembly program.  That usually means
that we write some part of the program, assemble it, test the new code in an
emulator, fix the code or write the next part, and so on.

To simplify this cycle, we can write a script or batch file that will perform
all of these tasks -- except for writing code, of course -- automatically.

In Linux or macOS, this sample bash file `build.sh` will assemble a file and
start the MAME emulator.

    #!/bin/sh
    set -e
    xas99.py prog1.asm prog2.asm -R -i -o program
    xdm99.py -X sssd w.dsk -a "progra?"
    mame64 ti99_4a -ioport peb -ioport:peb:slot2 32kmem -ioport:peb:slot8 hfdc \
           -ioport:peb:slot8:hfdc:f1 525dd -cart EA.rpk -flop1 work.dsk

Of course, you will have to adapt filenames and paths to your setup.  Finally,
set the executable flag for the file

    $ chmod ug+x build.sh

The `set -e` ensures that the script aborts when one of the commands returns
with an error.  The assembler will create one or more image files `program`,
`progran`, ..., which we add to a newly created disk image using a wildcard.
Finally, we start MAME with the E/A cartridge and the created disk image.

For Windows, we can adapt above script like this, and call it `build.bat`:

    @echo off
    xas99.py prog1.asm prog2.asm -R -i -o program
    if %errorlevel% neq 0 exit /b 
    xdm99.py -X sssd w.dsk -a "progra?"
    if %errorlevel% neq 0 exit /b 
    mame64 ti99_4a -ioport peb -ioport:peb:slot2 32kmem -ioport:peb:slot8 hfdc ^
           -ioport:peb:slot8:hfdc:f1 525dd -cart EA.rpk -flop1 work.dsk

The `if %errorlevel% ...` statements check if the previous command succeeded,
and if not, abort the batch file.

For each development cycle, we then only need to run our script after each code
change.

    <edit prog1.asm or prog2.asm>
    $ ./buid.sh
    > build.bat
    <edit prog1.asm or prog2.asm>
    $ ./buid.sh
    > build.bat
    ...

This automation by scripting becomes more effective the more steps the build
process takes.  The firmware of the [FinalGROM][6] cartridge, for example,
comprises an assembly part and a GPL part, and each result is included in
a C program, which is then compiled.  Executing the individual steps in the
correct order quickly becomes a too complex task to merely rely on pressing
Cursor-Up the correct number of times in the command line.     


### From Here On

This concludes our short introduction to some xdt99 tools.  For an in-depth
description of each tool, please refer to the following sections.


xas99 Cross-Assembler                                       <a name="xas99"></a>
---------------------

The `xas99` two-pass cross-assembler translates TMS9900 and TMS9995 assembly
code as well as programs for the F18A co-processor into executable programs for
the TI 99 home computer, in a variety of formats.

All existing assembly sources for the TI 99 should cross-assemble using `xas99`
without modifications.  Likewise, the generated object code is identical to the
object code produced by the TI Editor/Assembler package.  This includes all of
its quirks, such as variable-length lines or redundant address tags, but
hopefully none of its bugs.


### Assembling Source Code

In standard mode, the `xas99` cross-assembler reads an assembly source file and
generates an uncompressed object code file that is suitable for the Editor/
Assembler option 3 loader.

    $ xas99.py -R ashello.asm

This command yields object code file `ashello.obj`.  We can override the output
filename with the output option `-o`.

    $ xas99.py -R ashello.asm -o HELLO-O

The special name `-` redirects the output to `stdout`, i.e., prints it on the
screen.

    $ xas99.py -R ashello.asm -o -
    > --- <L> **** -
    ***** Warning: Unresolved references: VSBW, VMBW, KSCAN, VWTR
    0007EASHELLO A0000B100DB4845B4C4CB4F20B574FB524CB4420B2020B68697F19FF       0001
    A0012B7420B616EB7920B6B65B7921B0300B0000B02E0B8300B04C0B02017F2F9F          0002
    A0028B2A20B0202B0300B0420B0000B0580B0602B16FBB0200B0043B02017F336F          0003
    ...
    5001CSTART 30030VSBW  30046VMBW  3007AVWTR  30062KSCAN 7F2F8F               0007
    :       xdt99 xas                                                           0008

The `xas99` options `-R` for register prefixes, `-L` for creating a listing,
`-S` for adding a symbol block to the listing, and `-C` for generating
compressed object code correspond to the respective options of the
Editor/Assembler.

    $ xas99.py -R -C ashello,asm -L ashello.lst -S -o ashello-c.obj

`xas99` will report any _errors_ to `stderr` during assembly.  A typical error
may look like

    > t.asm <2> 0002 -   jmp @y
    ***** Error: Invalid '@' found in expression

Shown are the filename containing the error, the pass in which the error
occurred, the line number and the actual erroneous line, followed by the error
message.  Note that in some cases, an error may be reported twice, once for each
pass.

At the end of assembly, if there were any errors, `xas99` shows an error count
so that users can quickly see if any errors occured (especially if color is
disabled):

    12 Errors found.

The assembler may also issue a number of _warnings_, e.g.,

    > t.asm <2> 0002 -      mov  r0, >000a
    ***** Warning: Treating as register, did you intend an @address?
    > t.asm <2> 0003 -      ci   r1, r2
    ***** Warning: Register R2 used as immediate operand
    > t.asm <2> 0006 - lab  mov  @val(r1), r0
    ***** Warning: Using indexed address @0, could use *R instead
    > --- <2> **** -
    ***** Warning: Unused constants: L1

Warnings indicate a likely error made by the developer.  Warnings are also
written to `stderr`, unless they are suppressed with the quiet option `-q`.

Note that all examples above issues a warning we omitted so far:

    $ xas99.py -R ashello.asm
    > --- <L> **** -
    ***** Warning: Unresolved references: VSBW, VMBW, KSCAN, VWTR

This warning lists all symbols imported by `REF`, for which no external symbol
defined by `DEF` was found.  Since all unresolved symbols are E/A utility
functions, and we are creating object code for E/A option 3, we can ignore this
warning.  In all other cases, this warning indicates an error that might crash
our program.

On Linux and macOS platforms, all warnings and errors are _colored_ by default.
Irrespective of platform, the use of color can be turned on or off by using the
color options `--color on` or `--color off`, resp.  (Technical note: Colors
require so-called ANSI escape sequences, something that Windows `cmd.exe` only 
started to support very recently.)


### Creating Program Images

The image option `-i` tells `xas99` to generate image files that can be loaded
using Editor/Assembler option 5.

    $ xas99.py -R -i ashello.asm

Images larger than 8 KB are split automatically into multiple files, using the
filename convention of the Editor/Assembler.

The `-i` option follows the `SAVE` utility program shipped with the Editor/
Assembler package, and honors the symbols `SLOAD`, `SFIRST` and `SLAST` to
generate the image for the entire memory area spanned by those addresses.

Alternatively, if either symbol is missing, `xas99` will generate separate image
files for each program segment defined in the assembly source.  For example, a
source file containing

         AORG >A000
    L1   B @L2
         AORG >B000
    L2   B @L1

will yield two images files of 10 bytes each, instead of a single file of about
4 KB.

Note that the E/A option 5 loader happily loads non-contiguous image files, even
though the original `SAVE` utility cannot generate such images.
  
For further control about the memory regions to include in the image, see the
`SAVE` directive below.

We can use the base option `-a` to define the base address for relocatable code.
If no base address is given, default address `>A000` is used for images.  For
example, creating an image file from the source

    data >1111
    aorg >a002
    data >2222
    rorg 4
    data >3333

will yield an image containing these bytes

    00000000  00 00 00 0c a0 00 11 11  22 22 33 33              |........""33|
    0000000c

where the first six bytes are the image header.  We can see that the data from
the `RORG` segments were relocated to `>A000` and `>A004`, resp.
 
All the usual restrictions for program images apply.  In particular, the first
word of the first image file must be an executable instruction, and the E/A
utility functions must be provided by the program.

Since the command above

    $ xas99.py -R -i ashello.asm
    > --- <L> **** -
    ***** Warning: Unresolved references: VSBW, VMBW, KSCAN, VWTR

yields a warning about unresolved VDP utility functions, we need to provide
these functions ourselves, e.g., by supplying them on the command line.

    $ xas99.py -R -i ashello.asm vsbw_ea.asm vmbw_ea.asm vwtr_ea.asm kscan_ea.asm

For details, please refer to the _Tutorial_.

Caveat: When creating an image with symbols `SFIRST`, `SLAST` and supplying
utilities on the command line, e.g.,

    $ xas99.py -i source.asm vsbw.asm
    
the code of `vsbw.asm` will _not_ be included in the image, since it will be
placed outside the `SFIRST`-`SLAST` range!  In this case, we should use `COPY`.   


### Creating Binaries

Image files for E/A option 5 contain the actual program code that is loaded
verbatim into memory.  They also contain 6 bytes of metadata that instructs the
loader how many files to load and where to store the data.

The binary option `-b` tells `xas99` to generate raw binary files without
metadata.

    $ xas99.py -b -R -a ">6000" ascart.asm

The resulting `ascart.bin` file contains these bytes:

    00000000  48 45 4c 4c 4f 20 43 41  52 54 21 00 03 00 00 00  |HELLO CART!.....|
    00000010  02 e0 83 00 04 c0 02 01  20 00 02 02 03 00 d8 20  |........ ...... |
    00000020  83 01 8c 02 02 60 40 00  d8 00 8c 02 d8 01 8c 00  |.....`@.........|
    00000030  06 02 16 fc 02 00 01 8b  02 01 60 00 02 02 00 0b  |..........`.....|
    00000040  d8 20 83 01 8c 02 02 60  40 00 d8 00 8c 02 d8 31  |. .....`@......1|
    00000050  8c 00 06 02 16 fc 03 00  00 02 10 ff              |............|

By default, the assembler will generate one binary for the entire program.  This
can lead to sparse programs containing large sections of zero bytes if the
source comprises non-contiguous segments.  We can avoid this by using the
`SAVE` directive described below.

The base option `-a` sets the base address for relocatable segments; if not set,
relocatable code is kept at base 0.


### Creating MAME Cartridges

The cartridge option `-c` tells `xas99` to add a GPL header and create an RPK
cartridge file suitable for the MAME emulator.

    $ xas99.py -c -R ascart.asm -n "HELLO CART"

The name option `-n` overrides the default name of the program that shows up in
the TI menu screen.

Note that the first word in the code must be an executable instruction, or we
need to supply the start symbol as operand of the `END` directive, like was done
in `ascart.asm`.

The resulting RPK file is a ZIP archive containing the actual program code plus
various information for the MAME emulator on how to execute the program.

    $ unzip -l ascart.rpk
    Archive:  ascart.rpk
      Length      Date    Time    Name
    ---------  ---------- -----   ----
          140  02-12-2020 07:03   HELLO CART.bin
          491  02-12-2020 07:03   layout.xml
          131  02-12-2020 07:03   meta-inf.xml

`xas99` will automatically generate a suitable GPL header and relocate the
program to address `>6030`.  When using `AORG`, make sure to leave an unused >30
byte buffer at the beginning of the program.

Note that this option is very limited in what kind of headers it can generate.
We therefore recommended `-c` for only the simplest programs, and suggest
using `-b` instead.


### Creating Text Files

The text option `-t` generates a textual representation of the binary that would
be generated by `-b`.  Option `-t` has one parameter that specifies the format
of the text.  One of the following characters sets the target platform of the
generated text:    

| Character | Generated statement | For use in        |
| --------- | ------------------- | ----------------- |
|    `a`    |  DATA or BYTE       |  assembly or GPL  |
|    `b`    |  DATA               |  BASIC            |
|    `c`    |  list of values     |  C/C++            |

Adding `2` or `4` to the format generates bytes or words, respectively.  For
target platforms with different endianness, adding `r` swaps the byte order in
words.  For example,

    $ xas99.py -t a2 -R ashello.asm

yields text

    ;      aorg >0000
           byte >10, >0d, >48, >45, >4c, >4c, >4f, >20
           byte >57, >4f, >52, >4c, >44, >20, >20, >20
           byte >68, >69, >74, >20, >61, >6e, >79, >20
           byte >6b, >65, >79, >21, >03, >00, >00, >00
           ...

The result can be `COPY`ed, `#include`d, or just copy-and-pasted.

A typical use case for this option is to include a program written in language X
in another program of language Y.


### Embedding Code

For relocatable code not larger than around 24 KB, `xas99` can generate an
Extended BASIC program that invisibly contains the generated code:

    $ xas99.py -R --embed-xb ascart_xb.asm

The program `ascart_xb.asm` is almost identical to `ascart.asm`, but adds the
BASIC bias of `>60` to each character to print on the screen.

The resulting program is a regular Extended BASIC program in so-called long
format that will execute the assembly code when run.  Thus, the `--embed-xb`
options allows for the creation of assembly programs that do not require the
Editor/Assembler module for execution.

The generated Extended BASIC program will have only one visible line:

    $ xbas99 -p ascart_xb.iv254
    1 CALL INIT :: CALL LOAD(16376,88,89,90,90,89,32,255,228):: CALL LOAD(8196,6
    3,248):: CALL LINK("XYZZY")

We must not edit the generated program, though, or we will corrupt the embedded
assembly code!


### Creating List Files

The list option `-L` instructs `xas99` to generate a list file for the
assembled source code:

    $ xas99.py -R ashello.asm -L ashello.lst

The resulting file has a similar layout to the Editor/Assembler listing:

    ...
    0021 001C 0300  24 START  LIMI 0
         001E 0000
    0022 0020 02E0  18        LWPI WRKSP
         0022 8300
    0023
    0024               * CLEAR SCREEN
    0025
    0026 0024 04C0  14        CLR  R0
    0027 0026 0201  20        LI   R1,'* '
         0028 2A20
    0028 002A 0202  20        LI   R2,24*32
         002C 0300
    0029
    ...

The first columns show line number, memory address, memory contents, and
timing in cycles.  The memory contents may be suffixed by `r` for relocatable
addresses and `e` for unknown external symbols introduced by `REF`.

The list file is useful for understanding the program layout in memory and the
values of expressions.

The symbol option `-S` will append a dump of the symbol table to the listing.
Relocatable symbols are marked by `REL`.


### `xas99` Assembly Language

The `xas99` is a complete TMS9900 assembler with additional support for TMS9995
and F18A if option `-5` or `-18` is given, resp.

`xas99` understands all assembler directives described in the Editor/Assembler
manual and supported by the E/A loader, i.e.,

    DEF REF EQU DATA BYTE TEXT BSS BES AORG RORG DORG EVEN
    IDT DXOP COPY END

Note that the `DORG` directive _is_ supported, even though the TI assembler does
not do so.

The following directives are not supported by the E/A loader and are silently
ignored by `xas99`:

    PSEG PEND CSEG CEND DSEG DEND LOAD SREF LIST UNL PAGE TITL
    
`xas99` also defines a number of new directives, which are described in the
_xdt99 Extensions_ section.


#### Includes and Filename Handling

The `COPY` directive is used to include an external assembly source into the
current source unit.

Its filename argument may be a native path such as `"~/ti99/asm/sound.asm"` or
`"C:\TI Stuff\ASM\Sound.asm"`, but also a TI-style path such as `DSK1.SOUND` or
`DSK.UTILS.SOUND`.  In the latter case, `xas99` will search for include files 

    SOUND
    SOUND.A99
    SOUND.ASM
    SOUND.S

and their corresponding lower-case variants.  Note that for case-sensitive
platforms such as Linux, files with mixed-case filenames such as `Sound.Asm`
will not be found when using TI paths!

`xas99` searches for files in the current directory of the including file and
the `lib` directory of the xdt99 installation.  We can provide additional search
paths with the include path option `-I`.

    $ xas99.by ashello.asm -I gfx/ ../disk2/

For reasons described in the _Tutorial_, `-I` must appear after the source
filename.


### `xdt99` Extensions

The `xas99` cross-assembler offers various modern extensions to the original
Editor/Assembler to improve the developer experience.  All extensions are
backwards compatible, so legacy source code should compile with `xas99` as-is.

_Comments_ may be included anywhere in the source code by prepending them with
a semicolon `;`.  A semicolon inside a text literal or filename does _not_
introduce a comment.

Source code is processed case insensitively so that all labels, expressions, and
instructions may be written in upper case, lower case, or any mixture.  Text
literals are still case-sensitive, though.

    label1 byte >A,>b
    LABEL2 TEXT 'Hello World'
    Label3 mov Label1(R1),Label2(r2)

_Labels_ may be of arbitrary length and may contain arbitrary characters except
for whitespace and operators (`+-*/$#!@'"`).  Labels not imported or exported by
`REF` or `DEF`, resp., may even be in Unicode.  An optional colon `:` may be
appended to the label name.  The colon is not part of the name, but logically
continues the current line to the next:

    my_label_1:
        equ 1         ; assigns 1 to my_label_1      \
    my_label_2:                                      |  xas99 behavior
        aorg >a000    ; assigns >a000 to my_label_2  /
    my_label_3        ; assigns >a000 to my_label_3  \  standard E/A
        aorg >b000    ; no label to assign >b000 to  /  behavior

_Local labels_ simplify the implementation of small loops and subroutines to be
`COPY`ed.  A local label is introduced by an exclamation mark `!` and an
optional name.  Thus, the simplest local label is just a single `!`.  Local
labels need not be unique within the program.

References to local labels are resolved relative to the current position.  By
default, matching labels are searched after the current position.  References
prefixed with a unary minus sign `-` are searched before the current position.

    clear_data:
        li   r0, >a000
        li   r2, >100
    !   clr  *r0+         ; make jump target without potential name conflicts
        dec  r2
        jne  -!           ; jump to target two lines above
        rt

Doubling, tripling, ... the number of `!`s before a reference refers to the
second, third, ... match of the local label relative to the current position:

    !   dec  r1              <-+
        jeq  !     --+         |
        inc  r2      |         |
        jne  !!      |  --+    |
        jmp  -!      |    |  --|
    !   dec  r2    <-+    |    |
        jmp  -!!          |  --|
    !   inc  r1         <-+    |
        jmp  -!!!            --+
    !   rt

Note that the search for the nearest local label doesn't wrap around the source,
so

    !   inc  r1
        jmp  !
        end
        
yields error `Invalid local target`.

Labels `label` and `!label` are entirely different and can be used without
conflict in the same program.  Thus, local labels used in `COPY`ed source code
cannot interfere with the main source.

The use of _whitespace_ has been relaxed.  Single spaces may be used judiciously
within the operand field to increase the legibility of expressions.  Two or more
spaces as well as a tab character introduce the comment field.

    label  data addr + len - 1  comment
           movb @addr + 2(r1), *r2+ ; comment

_Technical note:_ It is not possible to detect the beginning of the comment
field based on the current instruction, as the example
 
    maxval equ 8 * 9 would be too big

shows.  Where does the comment start, and what is the value of `maxval`?

The _extended expression_ syntax supports parentheses `(`, `)`, the modulo
operator `%`, the exponentiation operator `**`, and binary operators bit-and
`&`, bit-or `|`, bit-xor `^`, and bit-not `~` as well as binary literals
introduced by `:`.

    area    equ (xmax + 1) * (ymax + 1)
    addr2   equ addr1 | >A000 & ~>001F
    padding bss size % 8
    binval  equ :01011010

Remember that all operators have the _same precedence_, i.e., an expression such
as `1 + 2 * 3 - 4 & 5` evaluates as `(((1 + 2) * 3) - 4) & 5`.  This may sound
annoying, but changing the established order of evaluation would break
compatibility with existing sources.  To adjust the order of evaluation,
parentheses are used: `1 + (2 * 3) - (4 & 5)`.

`xas99` features a number of so-called _modifiers_ that apply to expressions.

Many programs use byte or word constants, e.g., for `MOV`/`MOVB` or `C`/`CB`
instructions, when immediate values are not available or feasible.  A common
problem then is to keep track of all used constants.  `xas99` assists the
developer here by warning about unused constants (see _Warnings_ section).

A convenient alternative is to use _auto-generated constants_ with modifiers
`b#` and `w#`.  As an example,

    n   equ  40
        mov  w#>ff01, @status
        socb b#2 * n + 1, r1
        cb   @keycode, b#'Q'

is equivalent to this code without modifiers:

        mov  @h_ff01, @status
        socb @b_81, r1
        cb   @keycode, @b_81
    b_81:
        byte 81   ; note that 'Q' == 81 == 2*n+1
    h_ff01:
        data >ff01

For a word character constant such as `w#'A'`, a zero byte is appended to the
generated byte, e.g., `>4100`.

The `b#` and `w#` modifiers apply to the entire expression following the
modifier.  Parentheses can change this behavior, but doing so will yield
meaningless results.  For example,

        mov (w#30) + 2, r0
        
is equivalent to

        mov @c_30 + 2, r0
    c_30:
        data 30
        data ???
        
which will store an unknown value `???` in `R0`.

The assembler ensures that each value is added only once, so for constants
`b#>41`, `b#65`, and `b#'A'`, it will add only one constant to the code.

For each auto-generated constant, a `BYTE` or `DATA` directive will be
generated.  To denote _where_ these values should be placed, the `AUTO`
directive is used.  During assembly, it will be replaced by a sequence of
`BYTE`s and `DATA`s.

        save >2000,>3000

        aorg >2000
    start:
        movb b#1, @acc
        ...
        auto
        ...
        aorg >2ffc
    start_vector:
        data >8300
        data start

Auto-generated constants observe banks, and only appear in the bank where they
were defined.  You can place `AUTO` only in those banks, where at least one
auto-generated constant is used.  If on the other hand an `AUTO` is missing,
an error is thrown.

All auto-generated constants will also appear in the list file.

The _symbol size_ modifier `s#` returns the size of the label it is attached to,
where size is defined as the difference of the address of the attached symbol
and the address of the syntactically next symbol.

         li   r0, 320
         li   r1, text1
         li   r2, s#text1      ; s#text1 data 12
         bl   @vmbw
         ...
    text1:
        text 'HELLO WORLD!'
    text2:
        text 'GOOD BYE!'

In this example, `s#text1` translates to the address of an automatically
generated word constant 12, since the address difference of `@text1` and
`@text2` is 12 bytes.

The size modifier detects if the last byte of the range is a padding byte and
subtracts it from the size.

    text1:
        text 'HELLO WORLD'    ; now 11 bytes, but 12 bytes difference
    start:
        lwpi >8300

Here, `s#text1` yields 11, even though there are still 12 bytes difference
between `@text1` and `@start`, as the `lwpi` instruction must be placed on an
even address.

Keep in mind that `s#` requires a label immediately following the text or byte
constant it refers to.  In practice, this should almost always be the case.

Note that `s#` only applies to labels; symbols created by `EQU` are not
supported.

The _cross-bank access_ modifier `x#` enables cross-bank symbol access.  For a
detailed description on `x#`, see the paragraph on bank switching further down.

We can supply _additional symbols_ from the command line with the define option
`-D`.

    $ xas99.py ashello.asm -D symbol1 symbol2=2

If no value is given, the symbol is set to value `1`.

Symbols defined by `-D` are treated internally like labels and are stored as
absolute address.  They are not added to the `DEF` lists.

The symbol option `-E` dumps all symbols in EQU-like syntax to an external
file `sym.asm`:

    $ xas99.py -R ashello.asm -E sym.asm

The result reads like

    CLS:
           equ  >002E  ; REL    <-- relocatable address
    GPLST:
           equ  >837C  ;
    KCODE:
           equ  >8375  ;
    ...

and can be `COPY`ed into another program.

`xas99` also provides _new directives_.  The `BCOPY` directive includes an
external binary file as a sequence of `BYTE`s.  For example, if `sprite.raw`
is a raw data file containing some sprite pattern

    00000000  18 3c 7e ff ff 7e 3c 18                           |.<~..~<.|

then including this file with `BCOPY`

    sprite  bcopy "sprite.raw"

is equivalent to statement

    sprite  byte >18,>3c,>7e,>ff,>ff,>7e,>3c,>18

The `TEXT` directive also supports hex strings, e.g.,

    pattern text >8040201008040201

The `STRI` directive is similar to `TEXT`, but prepends a length byte.  In other
words,

    stri 'HELLO WORLD'

is equivalent to

    text >0b, 'HELLO WORLD'

The `FLOA` directive stores a decimal number in the 8-byte RADIX-100 format
used by the TI 99.  Note that digits exceeding the accuracy of RADIX-100 are
silently ignored.

    floa 123.456789012

The exponent notation `1e9` is currently not supported.

The `BANK` directive specifies the memory bank and optionally the base address
for the following code segment, or a shared code segment if the special value
`ALL` is used.  Banks count from zero.

    * asbank.asm
	      bank all, >6000
    func1 clr r0
          ...
          bank 1
    func2 li  r1,>1234
          ...

The address of a `BANK` directive defines the base address for other, 
addressless `BANK`s.  In the previous example, bank 1 also starts at `>6000`,
since bank 0 defined that base address.

A shared segment introduced by `BANK ALL` without optional address first
obtains the next available addresses for all banks, and then picks the biggest
one as start address.  If a plain `BANK n` without address follows a shared
segment, then its start is at the end of the shared segment.

For example, the program 

Within each bank, all `*ORG` directives may be used, without leaving the current
bank.
 
Note that the optional second argument of the `AORG` directive to specify the
current bank has been removed, and is no longer available.  Programs with such
a directive will fail during assembly.

Generating binary files with the `-b` command stores banked segments in separate
files.  For example, assembling source file `asbank.asm` containing directives

    BANK 0
    BANK 1
    BANK ALL
    
into a binary will yield files `asbank_b0.bin` and `asbank_b1.bin`.

`xas99` detects cross-bank accesses in address arguments.  Of those, accesses
from and to shared code segments are fine, but others are at least dubious.

By default, `xas99` allows all cross-bank accesses.  Using the cross-check
option `-X`, however, makes the assembler issues an error for each illegal
cross-bank access.

So, assuming `-X` is supplied for the following program, only the `ok` accesses
are legal, and the `error` accesses throw an error.

          bank 0, >6000
    l1    b    @l3      ; ok
          b    @l2      ; error: different bank

          bank 1
    l2    b    @l3      ; ok
          b    @l1      ; error: different bank

          bank all, >7000
    l3    b    @l1      ; ok, could branch to bank 0 or 1, i.e., l1 or l2

Also, the `B` instructions in segment `>7000` will branch to `L1` or `L2`,
depending on which bank is active then.

If cross-bank accesses are illegal (`-X`), the _cross-bank modifier_ `X#` still
overrides checks for individual uses, e.g., because the offending code will be
relocated to a different memory address during runtime.

          bank 0
    cont  clr  r0

          bank 1
          b    @x#cont  ; OK, no error

The new _`XORG` directive_ sets the location counter to a new address but does
not change the actual placement of the subsequent code segment.

          aorg >6000
    l1    data 0             ; l1 = >6000
          bl   @func         ; branches to >8382

    l2    xorg >8380         ; l2 = >6006
    l3    data 0             ; l3 = >8380
    func  inc  @l3
          rt
    l4    aorg               ; l4 = >600C
          ...

The list file for this program shows that the code of the `XORG` segment is
placed within the `>6000` segment, but the labels get values in the `>8380`
range.

    XAS99 CROSS-ASSEMBLER   VERSION 3.0.0
         **** ****     > t.asm
    0001                     aorg >6000
    0002 6000 0000     l1    data 0
    0003 6002 06A0  32       bl   @func
         6004 8382
    0004
    0005               l2    xorg >8380
    0006 6006 0000     l3    data 0
    0007 6008 05A0  34 func  inc  @l3
         600A 8380
    0008 600C 045B  20       rt
    0009               l4    aorg
    ...
        FUNC................ >8382 :
        L1.................. >6000 :
        L2.................. >6006 :
        L3.................. >8380 :
        L4.................. >600E :

`XORG` is useful for assembling code blocks that will be moved to a different
memory location, e.g., the scratchpad RAM, during run time.

    * move function to scratchpad RAM
    init  li   r0, >8380     ; target address for XORG segment
          li   r1, l2        ; start address of XORG segment
          li   r2, l4 - l2   ; length of XORG segment to copy
          bl   @memcpy

Note that `XORG` does not place code directly at the target address.  Instead,
we must copy all `XORG` segments during runtime, e.g., using the code template
shown before.

The `SAVE` directive limits the memory range to output and controls the
resulting files for the image `-i` and binary `-b` output.  For those formats,
each `SAVE` directive will yield one file, containing only code in the memory
range specified.

          save >6000,>7000   ; generate single image for >6000->6fff

          aorg >6100
    main  limi 0
          ...
          aorg >6800
    subr  clr  r0
          ...                ; assume final address is >6DFE
          end

By default, the resulting binary will contain the entire address range of the
SAVE(s), with bytes at unspecified addresses set to 0.

When supplying the minimize option `-M`, however, save ranges are minimized,
i.e., the resulting binary only contains those addresses contained in the 
program (and zero any gaps between them).

As an example, the simple program

         save >2000, >2100
         aorg >2010
         data 1, 2, 3, 4

will contain >100 bytes normally, but only 8 bytes together with `-M`.

Note that always the entire program is assembled, even if only a portion of it
is SAVEed.

In combination with banking, there will be one output file per SAVE per bank, 
even if that file is empty.

The arguments of `SAVE` may be expressions, and may be omitted to denote the
start and end of a program, resp.

          save lab1, lab2 + >100
          save ,>5000
          save >6000,

If no `SAVE` directives are provided, option `-b` will create one binary file
for the entire program.  Option `-i` will save the region between symbols
`SFIRST` and `SLAST`, if present, and generate one file for each segment
otherwise.

The source code _preprocessor_ allows for conditional assembly based on
well-defined conditional expressions.  The preprocessor commands `.ifdef` and
`.ifndef` check if a given symbol is defined or not.

           .ifdef lang_de
    msg    text 'Hallo Welt'
           .else
    msg    text 'Hello World'
           .endif

The commands `.ifeq`, `.ifne`, `.ifgt`, and `.ifge` test if two arguments are
equal, not equal, greater than, or greater than or equal, resp.  If the second
argument is missing, the first argument is compared against value `0`.

Conditional assembly preprocessor commands may be nested.  Valid conditional
expressions and their rules of evaluation correspond to those of the `EQU`
directive.

The `.print` preprocessor command prints its arguments to `stdout`.

    answer equ 42
           ...
           .print 'Selected answer is', answer

The `.error` command prints a message to `stderr` and aborts the assembly.

           aorg >6000
           ...
           .ifgt $, >7fff
           .error 'Cartridge program too large'
           .endif

In addition to symbols defined by labels, `xas99` also sets exactly one of

    _xas99_obj
    _xas99_image
    _xas99_bin
    _xas99_cart
    _xas99_xb 

depending on the assembler mode selected.  We can use these symbols to enable
the generation of multiple formats from one source.

`xas99` supports _macros_.  The `.defm` preprocessor command introduces a new
macro, which is terminated by the `.endm` command.  Inside the macro body, the
macro parameters `#1`, `#2`, ... are substituted by the macro arguments when
instantiating the macro:

    * fill bottom #1 rows with char #2
        .defm fill
        li   r0, 768
        li   r1, #2
        li   r2, #1 * 32
        s    r2, r0
        bl   @vmbw
        .endm

Macro parameters may only occur in operand positions, but not in labels or
mnemonics.  Parameters in literals, e.g., `text '#1'`, are also not substituted.
These restrictions currently prevent advanced macro trickery.

Macros are used like preprocessor commands, with any arguments separated by
commas:

        .fill 10, '* '

Macro instantiations are parsed like normal instructions, so macro arguments
cannot contain certain symbols such as `,` or `;`.  Empty arguments are allowed
if the macro expects at least two parameters.

Macro parameters are resolved by textual replacement.  Thus, when a macro
containing the line

        li   r0, 2 * #1

is instantiated with argument `1 + 2`, the resulting code will assign `R0` the
value 4 instead of 6.  We can avoid these pitfalls by supplying expressions in
parentheses:

        .macro (1 + 2)

Labels are allowed inside macro definitions.  To avoid duplicate symbols when
instantiating a macro more than once, all labels should be local.

A macro can instantiate other macros, but instantiations must not be circular.
Macro definitions cannot be nested.

Preprocessor commands are always executed, even inside inactive `.ifdef`/
`.endif` blocks.  The correct way to define environment-dependent macros is thus

    .defm mymacro
    .ifdef symbol
    clr r0
    .else
    clr r1
    .endif
    .endm

instead of using `.defm` ... `.endm` inside `.ifdef` ... `.endif`.

`xas99` also supports _TMS9995_ opcodes
    
    MPYS <gas>
    DIVS <gas>
    LWP  <wa>
    LST  <wa>
 
when using the `-5` option, and the _F18A GPU_ instruction set

    CALL <gas>
    RET
    PUSH <gas>
    POP  <gad>
    SLC  <wa>, <count>
    PIX  <gas>, <wa>

when using the `-18` option.  The `SPI` family of instructions is not supported;
please use their equivalents `CKON`, ... instead.


### Linker

`xas99` features a linker that can join object code files into any supported
format.  The linker is invoked by link option `-l` or by supplying more than one
source file.

If `fileN.obj` is the object code of source file `fileN.asm`, then these
commands are equivalent and yield the same file `result.obj`:

    $ xas99.py file1.asm file2.asm file3.asm ... -o result.obj
    $ xas99.py file1.asm file2.asm -l file3.obj ... -o result.obj
    $ xas99.py file1.asm -l file2.obj file3.obj ... -o result.obj
    $ xas99.py -l file1.obj file2.obj file3.obj ... -o result.obj

The order is important, though, so

    $ xas99.py file2.asm -l file1.obj file3.obj ... -o result.obj

will yield a different result.

Note that for the Editor/Assembler cartridge, the option 3 loader assumes the
role of the linker.

Linking will determine a memory layout for all object code files, and match
symbols imported by `REF` with symbols exported by `DEF`.  Linking mostly
concerns relocatable code, since the position of absolute code is fixed.

As an example, linking (the object code of) files

        def x2
        rorg >10
    x1  data 1
    x2  data 2
        aorg >20
    x3  data x2

and

        ref x2
        rorg >20
    y1  data 4
        aorg >22
    y2  data 5

yields this file (ignoring the order of instructions, but not their addresses):

        rorg >10
        data 1
        data 2
        rorg >34       ; next available reloc addr >14 + RORG offset >20
        data 4
        aorg >20
        data >12
        data 5

The `xas99` linker has two modes.  The default mode follows the logic of the
E/A loader.  The safe mode, invoked by safe link option `-ll`, additionally
resolves conflicts that may arise when linking relocatable code with absolute
code.  As an example, linking

        * program 1
        rorg >a000
        data 1
        aorg >a010
        data 2, 3
        
        * program 2
        rorg >10
        data 4
        
creates a conflict at address `>A012`, since both `DATA 3` and `DATA 4` will be
placed at that address.  (Note that for program 2, the next available
relocatable address is `>A002`, and the `RORG` offset is >10.)
  
Option `-l` will not resolve this conflict, and the later instruction `DATA 4`
will be placed at `>A012`.  Option `-ll`, on the other hand, resolves the
conflict by moving the conflicting program unit towards higher addresses until
all conflicts are resolved.  In this example, `DATA 4` is placed at `>A014`.

When finding a layout, with or without conflict resolution, each individual
object code file is placed as a unit, i.e., the same positive offset is applied
to all relocatable segments of one program unit.

Safe linking is most useful when linking source or object code that someone else
has written and which may contain unknown conflicts.  When linking our own
program, normal linking should be sufficient.
  

### Compatibility with E/A

The strictness option `-s` disables most `xas99`-specific extensions, in
particular the relaxed syntax, to improve backwards compatibility for legacy
sources:

    $ xas99.py -s ashello.asm

Strictness is required, for example, to assemble the _Tombstone City_ sample
source shipped with the Editor/Assembler package, as some comments in Tombstone
do not adhere to the two-space separator rule of `xas99`.

    R5LB   EQU SUBWS+11 * REGISTER 5 LOW BYTE.
    ***** Unknown symbol: REGISTER 5 LOW BYTE.

Finally, note that case insensitivity cannot be disabled.


xga99 GPL Cross-Assembler                                   <a name="xga99"></a>
-------------------------

The `xga99` GPL cross-assembler translates programs written in TI's proprietary
Graphics Programming Language into byte code that can be interpreted by the TI
99 home computer.

Invoking `xga99` in standard mode will assemble a GPL source code file into
_GPL byte code_ that may be placed in a physical or emulated GROM or GRAM
device.

    $ xga99.py gahello.gpl
    $ xga99.py gahello.gpl -o HELLOG

The output parameter `-o` may be used to override the default output filename
using extension `.gbc` (for "GPL byte code").

Note that in `gahello.asm`, the `GROM` directive is commented out, which places
the byte code in GROM 0 by default.  We can override this with the GROM option
`-G`.  For example, to place the byte code in the cartridge GROM,

    $ xga99.py gahello.gpl -G ">6000"
 
By default, `xga99` will yield one single file for the entire program, even if
it spans multiple GROMs.  To generate one file per GROM, we can use the split
GROM option `-g`.

    $ xga99.py sample.gpl -g

Note that `-g` splits based on `GROM` directives, and not by size.  Therefore,
we must ensure ourselves that the size of each GROM does not exceed >2000 bytes.

The cartridge parameter `-c` relocates the GPL program to the cartridge GROM
area, generates GPL header data, and packages the byte code image into a
cartridge file suitable for the MAME emulator.

    $ xga99.py -c gahello.gpl

The resulting `.rpk` file may be executed as-is by the MAME emulator:

    $ mame64 ti99_4a -cart gahello.rpk

The name parameter `-n` overrides the default name of the program that shows up
in the TI 99 menu selection screen.

    $ xga99.py -c gahello.gpl -n "HELLO GPL WORLD"

Again, we recommend `-c` only for very simple programs, and suggest using plain
byte code instead.

The text option `-t` creates a textual representation of the byte code.  The
text format can be specified similarly to `xas99`.

    $ xga99.py -t b4 gahello.gpl -o -
    DATA -1, -1, -1, -1
    DATA 0, 0, 0, 0
    DATA -1, -1, -1, -1
    DATA 13382, 27309, -9019, 24291
    DATA 13382, 27309, -9019, 24291
    ...

The listing option `-L` creates a list file that shows the addresses and byte
values for each source line.

    $ xga99.py gahello.gpl -L gahello.lst

When `-L` is given, the symbol dump option `-S` includes the symbol table in the
list file.

The include path option `-I`, the define option `-D`, the quiet option `-q` and
the symbol dump option `-E` work identical to their `xas99` counterparts.

As the Graphics Programming Language was never intended for public release,
existing tools for assembling GPL source code differ substantially in the syntax
they use.  `xga99` adopts a combination of the Ryte Data and the RAG GPL
Assemblers' syntax as its native format.
  
We can choose other syntax styles, however, with the syntax parameter `-y`.
Currently, the only extra syntax is the syntax of the TI Image Tool
disassembler, available with name `mizapf` (named after the creator of the image
tool).

    $ xga99.py gahello_timt.gpl -y mizapf

Note that the original GPL syntax described in TI's _GPL Programmer's Guide_ is
considered too arcane to be included in `xga99`.

The native `xga99` syntax style is more "modern" in that it supports lower case
sources, extended expressions, relaxed labels, local labels, and relaxed use of
whitespace, similar to `xas99`.  Both cross-assemblers also share the same
preprocessor.


### GPL Instructions

`xga99` supports all GPL mnemonics described in the _GPL Programmer's Guide_,
but adopted the common reversed operand order `Gs, Gd` for all but the shift
instructions.

Operands use the following prefix notation for (CPU) RAM, VDP RAM, and GROM
addresses, resp.:

| Prefix   | To address type   | Yields             | Restrictions |
| -------- | ----------------- | ------------------ | ------------ |
|   `@`    | RAM               | RAM direct         |              |
|   `*`    | RAM               | RAM indirect       |              |
|  `V@`    | VDP RAM           | VDP RAM direct     |              |
|  `V*`    | RAM (!)           | VDP RAM indirect   |              |
|  `G@`    | GROM              | GROM/GRAM direct   | `MOVE` only  |
| `@ (@)`  | RAM (Pad RAM)     | CPU RAM indexed    |              |
| `V@ (@)` | VDP RAM (Pad RAM) | VDP RAM indexed    |              |
| `G@ (@)` | GROM (Pad RAM)    | GROM/GRAM indexed  | `MOVE` only  |
|   `#`    | VDP register      | VDP register       | `MOVE` only  |

Note that indexes must be located in scratchpad RAM.  We can thus abbreviate an
indexed address like `V@>100(@>83e0)` to `V@>100(@>e0)`. 

There is no `G*<RAM>` GROM indirect address mode, but `G0(<Pad RAM>)` can be
used for Scratchpad RAM addresses instead.

Labels, even when attached to instructions, do not represent any memory type.
We could thus use any address prefix on any label, which on the other hand
implies that we _must_ use `G@` in `MOVE` instructions:

    t1  text 'HELLO'
        move 5, g@t1, v@100

The only exceptions to this rule are branch and call instructions, where the
address prefix `G@` is optional:

        b    l1
        b    g@l1

And just as we can tag labels in expressions with any address prefix, we cannot
endow a label with a type:

    s   equ  v@1    ;  Error: Unknown symbol: V@1

_Expressions_ are built using arithmetical operators `+`, `-`, `*`, `/`, `%`,
and `**` and bit operators `&`, `|`, `^`, and `~`.  Expressions are evaluated
left-to-right with equal operator precedence; parentheses may be used to change
the order of evaluation.  For further details, please refer to the `xas99`
section on expressions.

_Literals_ may be decimal numbers, hexadecimal numbers prefixed by `>`, binary
numbers prefixed by `:`, and text literals enclosed in single quotes `'`.

    byte 10, >10, :10, '1'

The following mnemonics for the _`FMT` sub-language_ are recommended, but the
styles of Ryte Data and RAG are also available.  Finally, we can choose other
styles with the `-y` option.

    HTEXT/VTEXT <text>
    HCHAR/VCHAR <count>, <char>
    HSTR <count>, <addr>          (no GROM, no VDP, no indexing, no indirection)
    ROW/COL <count>
    ROW+/COL+ <count>
    BIAS <count/gs>
    FOR <count> ... FEND [<label>]

Here, `<count>` represents an immediate value.


### GPL Directives

The `xga99` GPL assembler supports the following directives:

    GROM AORG EQU DATA BYTE TEXT STRI FLOAT BSS TITLE COPY BCOPY

Directives affecting listing generation are currently ignored:

    PAGE LIST UNL LISTM UNLM

Most `xga99` directives work very similar to their `xas99` counterparts.

The `BYTE` and `DATA` directives insert bytes and words into the program, resp.,
irrespective of the size of their arguments.

    label byte 1, >02, :11011010, '@', >100     ; >100 becomes >00
          data 1, >1000, 'A'                    ; 'A' becomes >0041

The `TEXT` directive generates a sequence of bytes from a text literal or an
extended hexadecimal literal.

    label text 'Groovin'' With GPL'
          text >183c7effe7c38100

Note that the second instruction is equivalent to `BYTE >18,>3C,>7E,...`.

The `STRI` directive works similar to the `TEXT` directive, but prepends a
length byte to the generated byte sequence.

The `FLOAT` directive stores a decimal number in the 8-byte RADIX-100 format
used by the TI 99.  Note that digits exceeding the accuracy of RADIX-100 are
silently ignored.

    float -123.456789012

The exponent notation `1e9` is currently not supported.

The `GROM` directive sets the GROM base address for the code that follows.
You can specify either the GROM number `0`, ..., `7`, or the absolute address
`>0000`, ..., `>e000`, where bits 0-12 are ignored.

If more than one `GROM` directive is placed in one program, each GROM segment
will be placed in a separate file, whose name is appended with the GROM address.

The `AORG` directive is used to place individual code segments at specific
addresses _within_ the given GROM.  The address argument is thus relative to
the GROM base address given by `GROM`.

Instead of using the `GROM` and `AORG` directives, the location of the byte code
may also be specified by the GROM option `-G` and AORG option `-A`, resp.  The
cartridge option `-c` implies `-G 0x6000` and `-A 0x30`.
  
Options `-G` and `-A` will not override `GROM` or `AORG` directives, but set the
GROM and address offset of the first line of the code.

The `COPY` and `BCOPY` directives include text files or binary files, resp.  A
binary file is translated as a sequence of `BYTE`s.


### `xdt99` Extensions

The `xga99` GPL cross-assembler offers various "modern" extensions to the
original TI GPL specification to improve the developer experience.  All
extensions are backwards compatible so that any existing source code using
suitable syntax should assemble as-is.

The `xas99` extensions regarding _comments_, _labels_, _local labels_,
_whitespace_, _expressions_, _external symbols_ and the _preprocessor_ also
apply to `xga99`.  Note, however, that GPL macros use macro parameters `$1`,
`$2`, ... instead of `#1`, `#2`, ..., as the `#` sign is used to denote VDP
registers in GPL.

The _predefined symbols_ set by `xga99` are `_xga99_gbc` or `_xga99_cart`,
depending on the output format chosen.


xda99 Disassembler                                          <a name="xda99"></a>
------------------

The cross-disassembler `xda99` is a command-line tool to convert machine code
back into assembly source code.

As an example file for this section, we will use `ascart.bin`, among others,
which we can create by typing

    $ xas99.py -R -b ascart.asm

To disassemble a binary machine code file, we need to tell the disassembler the
first address of the machine code with address option `-a` and the starting
address for the disassembly with "from" option `-f`:

	$ xda99.py ascart.bin -a 6000 -f 600c

All command line values are interpreted as hexadecimal values.  They can
optionally be prefixed by `>` or `0x`.

The resulting file `ascart.dis` contains the disassembled instructions in a
listing-like format:

                aorg >6000
    6000 4845?
    6002 4c4c?
    6004 4f20?
    6006 4341?
    6008 5254?
    600a 2100?
    600c 0300   limi  >0000
    600e 0000
    6010 02e0   lwpi  pad
    6012 8300
    6014 04c0   clr   r0
    ...

We see for each addresses the contents and the assembly instruction located at
the address.  Words showing `?` have not been disassembled.

The output option `-o` redirects the output to a different file, or prints to
`stdout` when using the special filename `-`.

We can also specify an upper bound on the range to disassemble with the "to"
option `-t`.

By default, `xda99` disassembles TMS9900 machine code.  We can, however, extend
the recognized opcodes to TMS9995 and F18A by supplying options `-5` or `-18`,
resp. 

The skip option `-k` skips some bytes at the beginning of the binary to
disassemble.  For example, when disassembling an E/A option 5 image, we use `-k`
to skip the 6-byte header:

    $ xda99.py ashello5.img -k 6 -a a000 -f a000

Machine code consists of both code and data segments, which are often
intermingled.  Without context information, however, a disassembler cannot tell
data from code.

Using `xda99` with the from parameter `-f` will start the disassembly in
_top-down mode_, which disassembles sequentially word by word.  This mode often
yields bad results, as data segments will be translated into meaningless
statements.
  
For example, if we change the from address in the `ascart.bin` example above to
`-f 6000`, we get

    $ xda99.py ascart.bin -a 6000 -f 6000 -o -
                aorg >6000
    6000 4845   szc   r5, @>4c4c(r1)     |
    6002 4c4c                            |  data erroneously
    6004 4f20   szc   @>4341, *r12+      |  disassembled into
    6006 4341                            |  source code
    6008 5254   szcb  *r4, r9            |
    600a 2100   coc   r0, r4             |
    600c 0300   limi  >0000
    600e 0000
    ...

For some kinds of data, we can spot if the data was disassembled erroneously, as
the resulting source often contains uncommon mnemonics and operands with complex
address formats and random-looking addresses.

The situation gets worse when disassembling data into nonsense statements spills
over to the real code, e.g., if the last data word is assembled into a two-word
instruction:

        aorg >a000
        byte 4, 224
    start:
        lwpi >8300
        limi 0
        ...

Disassembling the machine code generated by above program with `-f a000` yields

                aorg >a000
    a000 04e0   clr  @>02e0        |  disassembled data
    a002 02e0                      |  swallowed the LWPI
    a004 8300   c    r0, r12       |  instruction
    a006 0300   limi >0000
    a008 0000
    ...

If the data segments are known, those can be excluded from disassembly with the
exclude option `-e`.

	$ xda99.py ascart.bin -a 6000 -f 6000 -e 6000-600c

The upper address `yyyy` of an exclude range `xxxx-yyyy` is not included in the
range, so range `6000-6000` is an empty range.  Range addresses should always be
even.

For unknown programs, excluding data segments is difficult.  Thus, `xda99`
offers an additional _run mode_ `-r` that observes static branch, call, and
return statements, and disassembles only along the program flow.

	$ xda99.py ascart.bin -a 6000 -r 600c

For the `ascart.bin` program, though, there is no difference between run mode
and top-down mode, as code and data are separate in that program.

Run mode is not limited to one starting address:

	$ xda99.py suprdupC.bin -a 6000 -r 6034 603c

For convenience, the special run start address `start` denotes all start
addresses derived from the machine code.  Thus, the above line becomes

	$ xda99.py suprdupC.bin -a 6000 -r start

Currently, `start` only works for cartridge images containing a GPL header.  In
all other cases, `start` defaults to the address given by `-a`.

Run mode adds jump marker comments to the output that show from which address
a given instruction was branched to:

    6058 d809   movb r9, @>837c
    605a 837c
    605c d809   movb r9, @>8374           ; <- >6068
    605e 8374
    6060 0420   blwp @kscan
    6062 2108
    6064 9220   cb   @>8375, r8
    6066 8375
    6068 13f9   jeq  >605c
    606a d020   movb @>8375, r0
    606c 8375

The program option `-p` turns the disassembly into actual source code that can
be re-assembled again:

           aorg >6000
    vdpwd  equ  >8c00
    pad    equ  >8300
    gpllnk equ  >2100
    vdpwa  equ  >8c02
    l6000  data >4845
    l6002  data >4c4c
    l6004  data >4f20
    l6006  data >4341
    l6008  data >5254
    l600a  data gpllnk
    l600c  limi >0000
    l600e
    l6010  lwpi pad
    l6012
    l6014  clr  r0
    ...

The `-p` options will also include an `EQU` stanza of all symbols used, in this
case all `xas99` internal symbols that were imported with `REF` by the program.

To use more symbols, a symbol file can be supplied with the `-S` parameter.  The
symbol file can be generated with the EQU option `-E` of `xas99`, or written
manually in a fairly free style, e.g.,

    s1 equ >10
    s2:
            equ 10
    s3 >10
    s4: 0x10

Data segments often contain strings, that can be restored heuristically by using
the string option `-n`, either with or without the `-p` option.

    $ xda99.py ascart.bin -a 6000 -f 600c -n -o -
                aorg >6000
    6000 4845   text  'HELLO CART'
    6002 4c4c
    6004 4f20
    6006 4341
    6008 5254
    600a 2100?
    600c 0300   limi  >0000
    600e 0000
    6010 02e0   lwpi  pad
    ...

Option `-n` tries to find strings in un-disassembled areas.  Thus, `-n` is only
useful in run mode or top-down mode with exclusions, as otherwise top-down mode
will not leave behind any data segments where strings could be found.

Note that currently, `xda99` only disassembles even length strings.

The concise option `-c` ignores all non-disassembled addresses in the output by
merging those addresses marked by `?` and replacing them by `....`.

                aorg >2000
    2000 1008   jmp  >2012
    ....
    2012 c481   mov  r1, *r2
    2014 05a2   inc  @>0002(r2)
    2016 0002
    2018 2881   xor  r1, r2
    201a 1309   jeq  >202e
    201c 10fa   jmp  >2012

Options `-c` and `-p` cannot be combined.

The strict option `-s` generates output files in legacy Editor/Assembler format,
in particular in upper-case and without extra whitespace.

The register option `-R` tells the disassembler to use plain integers for
registers, i.e., to _not_ prepend registers with `R`.


### Run Mode and Conflicts

When the run mode disassembler hits an address which has already been
disassembled, it stops the current run.  This regularly happens for multiple
calls to a subroutine, loops, or recursion, and is perfectly normal.

But run mode is not always 100% accurate, as `xda99` cannot follow indirect
branches such as `B *R1`, and doesn't know if a condition for `JEQ LABEL` is
always true and thus has no alternate path.  (The latter remark is more relevant
for `xdg99`, where `BR` is often used as a shorter `B`.)  As a consequence, a
run may "run off", and worse, different runs may try to disassemble the same
range differently:

                   First run,              Second run,
                   starting @>6000         starting @>6002

                   aorg >6000              aorg >6000
    6000 c820      mov  @pad, @>831c                         |
    6002 8300                              c    r0, r12      | disagreement
    6004 831c                              c    *r12, r12    |
    6006 0a51      sla  r1, 5              sla  r1, 5
    6008 1620      jne  >604a              jne  >604a

Above, the second run hits an address that is only _part_ of a previously
disassembled address (i.e., an operator), which raises a conflict about which
version is correct.

The default behavior of `xda99` is to stop the run, leaving the previous
disassembly untouched.  You can override the default with the force option `-F`,
which will always overwrite previous results.  This is done cleanly, so that
run 2 above will reset the overridden instruction at address `@>6000`.

There is no recommendation to disassemble with or without force.  The result of
each disassembly may vary with each binary, and should be tried out.

In general, we should not expect an optimal result by invoking `xda99` just
once.  Instead, disassembly is an iterative process, where the run mode will
continuously uncover new code fragments, and where previous disassemblies have
to be revised as we gather new information about the program.


xdg99 GPL Disassembler                                      <a name="xdg99"></a>
----------------------

The GPL disassembler `xdg99` is a command-line tool to translate GPL byte code
into GPL source code.

`xdg99` shares almost all options with `xda99`, and works very similar.  In
fact, at some point in the future, both programs might be merged into one.

To show the similarities,

	$ xdg99.py gacart.gbc -a 6000 -f 6030

disassembles byte code file `gacart.bin`, into GPL instructions:

              grom >6000
              aorg >0000
	6000 aa?
	...
	602f 00?
    6030 07   all   >20
    6031 20
    6032 04   back  >04
    6033 04
    6034 be   st    >48, v@>0021
    6035 a0
    6036 21
    6037 48
    ...

The only option that `xdg99` features over `xda99` is the syntax selection
option `-y`, which is already known from `xga99`:

	$ xdg99.py gacart.bin -a 6000 -f 6030
    ...
    6206 31   move >0010, g@>6ec4, v@>0033
    ...

	$ xdg99.py gacart.bin -a 6000 -f 6030 -y mizapf
    ...
    6206 31   move >0010 bytes from grom@>6ec4 to vdp@>0033
    ...

At the same time, the `-R` option of `xda99` has no meaning for GPL, and thus
is not supported by `xdg99`.


xbas99 TI BASIC and TI Extended BASIC Tool                 <a name="xbas99"></a>
------------------------------------------

`xbas99` is a command-line tool for converting TI BASIC and TI Extended BASIC
programs from source format to internal format, and vice versa.  For brevity, we
will refer to both TI BASIC and TI Extended BASIC programs simply as BASIC
programs.

Programs in source or _listing_ format are plain text files that contain the
BASIC statements that a user would type in.  These kind of text files are
usually not stored on a floppy disk.

Programs in internal or _tokenized_ format are TI-specific files in `PROGRAM`
format that are generated by the `SAVE` command and understood by the `OLD` and
`RUN` commands.  `xbas99` also supports programs created in so-called long
format of file type `INT/VAR 254` and merge format of type `DIS/VAR 163`.

Typical use cases for `xbas99` include the listing of programs stored in
internal format and the creation of program files for the BASIC interpreter from
a text file with BASIC statements.

The create option `-c` encodes a BASIC listing into internal format so that the
resulting file can be loaded and run by one of the BASIC interpreters.

    $ xbas99.py -c bashello.bas

`xbas99` uses the `.prg` extension for BASIC programs in tokenized format.
 
The print option `-p` lists the statements of a BASIC program in tokenized
format on the screen.  Formatting is identical to the built-in BASIC `LIST`
command modulo the line wrapping.

    $ xbas99.py -p bashello.prg
    10 REM HELLO
    20 INPUT "YOUR NAME? ":NAME$
    30 PRINT "HELLO ";NAME$
    40 END

The similar decode option `-d` saves the listing of program to a file.

    $ xbas99.py -d bashello.prg -o bashello2.bas

BASIC programs in long format are detected automatically.  To list programs in
merge format, we must add the merge option `--merge`.  Merge format is currently
not detected automatically.

The create option `-c` assumes that each line of the text file contains exactly
one line of the program.  If the listing has been formatted with a fixed line
width, e.g., when stored as `DIS/VAR`, or derived from a physical print-out by
OCR, this assumption may not hold.

To join split lines, we can use the join option `-j`.  However, this task is not
as simple as it seems, as this example in `DIS/VAR 40` shows:

    100 CALL CLEAR :: CALL SCREEN(2) :: CALL
     HCHAR(1,1,42,768)
    110 SHIPS=3 :: SCORE=0 :: LEVEL=1 :: SHI
    ELD=0 :: ALIENS=99
    120 CALL KEY(0,KEY,STA):: IF KEY=9 THEN
    290 ELSE GOSUB 560
    130 CALL CHAR(96,"8040201008040201")
    ... 

As we see, program line `120` is split in two rows, and the `THEN` target of the
`IF-THEN-ELSE` statement happens to be wrapped to the start of the second row.
Since `xbas99` does not perform a syntactic analysis, the program cannot tell if
the line starting with `290` is the continuation of the previous line or the
next program line with line number `290`.

To handle this situation, `-j` has an optional parameter.  This parameter tells
`xbas99` how many text lines each program lines may occupy, and/or what the
biggest difference between two consecutive line numbers is.  In the example
above, the first value would be 2, because we have no program line wrapped over
three or more text lines, and the second value would be 10, since the difference
between two consecutive line numbers is always 10.

Thus, we should tokenize our program with

    $ xbas99.py -c aliens.bas -j 2,10

If we want to provide only one of these values, we can write `2,` or `,10`.

Since the biggest line number difference is 10, `xbas99` knows that for the line
starting with `290`, the `290` cannot be a line number, and thus the line must
be part of the statement starting with `120`.
 
There are additional heuristics that `xbas99` applies, e.g., that line numbers
must always increase.  If a translation using `-j` fails, we need to join the
lines manually.

To check that the translation was successful, we can print the listing of the
tokenized program.

    $ xbas99.py -p aliens.prg
    100 CALL CLEAR :: CALL SCREEN(2):: CALL HCHAR(1,1,42,768)
    110 SHIPS=3 :: SCORE=0 :: LEVEL=1 :: SHIELD=0 :: ALIENS=99
    120 CALL KEY(0,KEY,STA):: IF KEY=9 THEN 290 ELSE GOSUB 560
    130 CALL CHAR(96,"8040201008040201")
    ...

`xbas99` also supports a _label mode_ in which no line numbers are used.
Instead, targets for branch statements such as `GOTO` or `THEN` are defined by 
labels.

A label has to start at the beginning of the line and must end in a colon. 
Other lines must be indented by at least one blank.

    START:
      INPUT "CHECK WHICH NUMBER? ":N
      GOSUB @ISPRIME
      IF PRIME THEN @PRIME
      PRINT "NOT PRIME"
      GOTO @START
    PRIME:
      PRINT "PRIME!"
      GOTO @START
    ISPRIME:
      REM CHECK IF N IS PRIME
      ...
      PRIME=0
      ...
      PRIME=1
      RETURN

To tokenize a label-based program, we use the label option `-l`.

    $ xbas99.py -c -l prime.bas
    
Note that `-c` will convert label-based programs into regular line number-based
programs, so decoding `-d` will never yield a label-based program.

    $ xbas99.py -p prime.prg
    100 INPUT "CHECK WHICH NUMBER? ":N
    110 GOSUB 170
    120 IF PRIME THEN 150
    130 PRINT "NOT PRIME"
    140 GOTO 100
    ...

The long option `-L` instructs `xbas99` to create the program in long format.
Long programs are stored within the 32 KB memory expansion and may be larger
than conventional programs.  The creation of programs in merge format is
currently not supported.

The protection option `--protect` will add list protection to the generated
program.  Programs with list protection cannot be listed or edited by the BASIC
interpreters.  Note, however, that the print option `-p` of `xbas99` will _not_
honor the protection flag.


### Running BASIC Programs

Before we can run programs created by `xbas99` in an emulator or on a real TI,
we have to transfer them to a disk image or convert them into TIFILES format
using `xdm99`.

    $ xdm99.py -X sssd basic.dsk -a bashello.prg
    $ xdm99.py -T bashello.prg -o BASHELLO

Advanced users of xdt99 may also combine the creation of the BASIC program file
and the transfer to a disk image into one single step using a pipe:

    $ xbas99.py -c bashello.bas -o - | xdm99.py basic.dsk -a - -n HELLO

All tools in xdt99 follow the convention that the special filename `-` denotes
`stdin` or `stdout`, depending on context.  We can also pipe from `xdm99` into
`xbas99` to list BASIC programs that are stored on a disk image:

    $ xdm99.py basic.dsk -p BASHELLO | xbas99.py -p -
    10 REM HELLO
    20 INPUT "YOUR NAME? ":NAME$
    30 PRINT "HELLO ";NAME$
    40 END

Also note that `xbas99` will read and encode any text file that we supply, with
only minimal syntax checking.  In other words, the resulting program file should
always load with `OLD`, but it may not `RUN`.  A future version of `xbas99` may
contain more advanced syntax checks to assure that only correct programs may be
tokenized.


xdm99 Disk Manager                                          <a name="xdm99"></a>
------------------

`xdm99` is a command-line tool for handling sector-based TI disk images and
files in TIFILES or v9t9 format.


### Cataloging Disks

When we invoke `xdm99` without any options, the tool prints the file catalog of
the disk image to `stdout`:

    $ xdm99.py ed-asm.dsk
    ED-ASSM   :     97 used  263 free   90 KB  1S/1D  40 TpS
    ----------------------------------------------------------------------------
    ASSM1         33  PROGRAM       8192 B            P
    ASSM2         18  PROGRAM       4102 B            P
    EDIT1         25  PROGRAM       5894 B            P
    SAVE          13  DIS/FIX 80    3072 B   36 recs  P
    SFIRST/O       3  DIS/FIX 80     512 B    5 recs  P
    SLAST/O        3  DIS/FIX 80     512 B    4 recs  P

The top line shows the name of the disk, protection status, the number of used
and free sectors, and the disk geometry.  For each file, the number of used
sectors, the file type, the file length, the number of records, and the
protection status is shown.  If present, the file creation or modification time
is also shown.

`xdm99` warns about any inconsistencies it may find, e.g., blocks claimed by
files that are not allocated in the allocation map.  For example, when using the
Editor/Assembler on a real machine with the TI Floppy Disk Controller, these
inconsistencies happen more frequently than one would assume.  Files affected
are flagged with `ERR` in the catalog.  In such cases, we can use the repair
option `-R` to automatically try to repair disks with inconsistencies.


### Extracting Files

The extract option `-e` extracts one or more files from the disk image to the
local file system.

    $ xdm99.py work.dsk -e HELLO-S CART-S

The local filename is derived automatically from the TI filename by lowercasing.
If we want to keep the original filename as it was on the disk, we can use the
TI-style name option `-N`.

We can override the default name with the output option `-o`.

    $ xdm99.py work.dsk -e HELLO-S -o hello.asm

If `-o` specifies a directory, all output files are placed in that directory.

    $ xdm99.py work.dsk -e HELLO-O HELLO-S -o ti-stuff/
    
When extracting two or more files, `-o` may only be used with a directory
argument.

To print the contents of a file to `stdout`, the print option `-p` may be used.

    $ xdm99.py work.dsk -p HELLO-S

In general, printing files only makes sense for files in `DIS/FIX` or `DIS/VAR`
format.  For `INT` or `PROGRAM` files, however, we can pipe the output of
`xdm99` into an external tool, e.g., `hexdump`, to visualize the contents.

    $ xdm99.py work.dsk -p ASHELLO5 | hexdump -C
    > (only possible with external hexdump utility)
    00000000  00 00 00 f8 a0 00 10 0d  48 45 4c 4c 4f 20 57 4f  |........HELLO WO|
    00000010  52 4c 44 20 20 20 68 69  74 20 61 6e 79 20 6b 65  |RLD   hit any ke|
    00000020  79 21 03 00 00 00 02 e0  83 00 04 c0 02 01 2a 20  |y!............* |
    00000030  02 02 03 00 04 20 a0 7e  05 80 06 02 16 fb 02 00  |..... .~........|
    ...
    000000e0  a0 dc 02 e0 83 e0 c8 0b  20 aa 06 a0 00 0e 02 e0  |........ .......|
    000000f0  20 94 c8 0b 83 f6 03 80                           | .......|

Note that `-p` is equivalent to combining parameters `-e` and `-o -`.

Filenames given by `-e` may be glob patterns containing wildcards `*` and `?`.
This will extract all files matching the given pattern.

    $ xdm99.py work.dsk -e "H?LLO-*"

Note that on Linux and macOS platforms, we have to quote our glob pattern to
prevent the shell from expanding the pattern prematurely.
    
Extracting files will yield the file contents only.  In we also want to retain
the metadata, i.e., file type and record length, we should extract files in
TIFILES or v9t9 format, described below.


### Working with Disks

The _add_ option `-a` adds local files to the disk image.  `xdm99` will infer a
suitable TI filename from the local filename unless an explicit filename is
given by the _name_ option `-n`.  If the file is not of type `PROGRAM`, we must
provide the file type using the _file type_ option `-f`.

    $ xdm99.py work.dsk -a ashello.asm -n HELLO-S -f DIS/VAR80

The syntax for `-f` is fairly permissible, e.g., `DIS/FIX 80`, `DISFIX80`, or
`df80` all work.

If we add multiple files with `-a` and specify a name with `-n`, all files will
get that filename, but with the last character incremented for each file.

    $ xdm99.py work.dsk -a intro main appendix -n NAME

will add the three files as `NAME`, `NAMF`, and `NAMG` to the disk image.

The _rename_ option `-r` renames one or more files on the disk.

    $ xdm99.py work.dsk -r HELLO-S:HELLO/S

For each file to rename, we have to provide the old and the new filename,
separated by a colon `:`.

To rename the disk itself, we use the `-n` option without `-e` or `-a` options.

    $ xdm99.py work.dsk -n WORK-2

The _delete_ parameter `-d` deletes one or more files from the disk.

    $ xdm99.py work.dsk -d HELLO-I HELLO-O
    $ xdm99.py work.dsk -d "*-O"

Note that the deletion is "secure" in the sense that the contents of the deleted
files cannot be found anywhere on the disk after the deletion.

The _write protection_ parameter `-w` toggles the current protection status of
the given files.

    $ xdm99.py work.dsk -w HELLO HELLO-CPY

Note that file protection affects only TI 99 systems and emulators, and will be
ignored by `xdm99`.

Modifying file operations, such as `-a`, `-r`, or `-d`, do not retain the
overall sector structure of the disk.  In particular, for all such operations,
the disk image will be automatically defragmented.  Simply cataloging the disk
or extracting a file, however, will _not_ modify the disk image.

By default, all modifying disk operations will change the disk image directly.
To create an independent copy of the original disk image with the changes
applied, the `-o` option may be used.

    $ xdm99.py work.dsk -a file -o copy.dsk

The original disk image `work.dsk` will not be changed.


### Working with Files

As we already mentioned, extracting files from a disk image to the local file
system will lose certain TI-specific information, such as the file type or the
record length.  In order to retain this meta information, the v9t9 and TIFILES
formats were created.

Both formats use a header of 128 bytes containing filename and file properties.
For example, for file `ASHELLO` in `DIS/FIX 80` format, the TIFILES header
contains

    $ xdm99.py work.dsk -e ASHELLO -t | hexdump -C
    00000000  07 54 49 46 49 4c 45 53  00 03 00 03 a0 50 08 00  |.TIFILES.....P..|
    00000010  41 53 48 45 4c 4c 4f 20  20 20 00 00 00 00 6e b9  |ASHELLO   ....n.|
    00000020  28 7b 6e b9 28 7b ff ff  20 20 20 20 20 20 20 20  |({n.({..        |
    00000030  20 20 20 20 20 20 20 20  20 20 20 20 20 20 20 20  |                |
    ...
    
and the v9t9 header contains

    00000000  41 53 48 45 4c 4c 4f 20  20 20 00 00 00 03 00 03  |ASHELLO   ......|
    00000010  a0 50 08 00 6e d7 28 7b  6e d7 28 7b 00 00 00 00  |.P..n.({n.({....|
    00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    ...

`xdm99` supports both TIFILES and v9t9 formats by adding the TIFILES option `-t`
or the v9t9 option `-9` options to add or extract operations.

    $ xdm99.py work.disk -t -e HELLO-S
    $ xdm99.py work.disk -9 -e HELLO-S

By default, files extracted in TIFILES or v9t9 format will have extension `.tfi`
or `.v9t9`, resp.

    $ xdm99.py work.disk -t -a hello-s.tfi
    $ xdm99.py work.disk -9 -a hello-s.v9t9

Note that `xdm99` will not infer the format automatically, so if we forget to
supply `-t` or `-9` when adding files, the metadata of the files will be stored
on the disk image as part of the file contents.

Since TIFILES and v9t9 formats already store all metadata, options `-n` and
`-f` are ignored when used in combination with `-t` or `-9`.

We should note that `xdm99` also handles short TIFILES files as used by
Classic 99 and other programs.  Short TIFILES files do not store the TI filename
and creation date, but use the host filesystem information instead.

Extracted TIFILES files are always in long format.  Classic 99 will use long
files, but ignore the stored filename.  Thus, for Classic 99, we should set the
actual filename to a TI-style filename.  We can easily do this with the TI-style
name option `-N` when extracting files with `-t` and `-e`.

    $ xdm99.py work.disk -t -N -e HELLO-O

Note that for v9t9 or long TIFILES files, there is no relation between the TI
filename stored in the TIFILES or v9t9 metadata, and the host filename of the
TIFILES or v9t9 file itself.  Renaming the file will not change the TI filename.
The `-N` option changes the host filename, not the TI filename.  It is therefore
only useful for short TIFILES files, e.g., for use with the Classic 99 emulator.
 
If we want to view the metadata information of a TIFILES or v9t9 file, we can
use the info option `-I`.

    $ xdm99.py -I ashello.asm.tfi
    ASHELLO       5  DIS/VAR 80     938 B  63 recs     2020-03-15 17:59:10 C

If we want to see the contents, we use the print `-P` option instead.

    $ ../xdm99.py -P ashello.asm.tfi
    *  HELLO WORLD
    
           IDT 'ASHELLO'
           
           REF VSBW,VMBW,VWTR
           REF KSCAN
    ...

To convert from between TIFILES/v9t9 files and plain files, we can use the from
and to options `-F` and `-T`, where the reference is the TIFILES/v9t9 format.
Since plain files lack metadata information, we need to add that data with the
file type option `-f` and the name option `-n`.

    $ xdm99.py -F hello-s.tfi
    $ xdm99.py -T ashello.asm -f dv80 -n HELLO-S -o hello-s.tfi

Note that `-F`, `-I`, and `-P` infer automatically whether the file is in
TIFILES or v9t9 format.  We can still override the format with `-t` or `-9`,
though.


### Analyzing Disks

The _check disk_ option `-C` analyzes a disk image for errors and prints a
summary to `stderr`.  While all disk operations, including cataloging, also
check and report any disk errors found, the `-C` parameter restricts the output
of `xdm99` to those errors only.

    $ xdm99.py -C work.dsk

The `-C` parameter also causes `xdm99` to set its return value to non-zero for
warnings, making it simple to write shell scripts for batch processing bad disk
images.

The _disk repair_ option `-R` tries to fix any disk errors, mostly by deleting
erroneous files from it.

    $ xdm99.py -R bad.dsk
    $ xdm99.py -R bad.dsk -o fixed.dsk

The repair operation is likely to cause data loss, so it is best to extract
erroneous files beforehand or to specify an alternative output file with `-o`.

The _initialize_ option `-X` creates a new, blank disk image, using an optional
name provided by `-n`.

    $ xdm99.py blank.dsk -X 720 -n BLANK

The size of the disk image is given by the number of sectors.  You may also use
a disk geometry string, which is any combination of the number of sides `<n>S`,
the density `<n>D`, and an optional number of tracks `<n>T`, where `<n>` is an
integer or the letters `S` or `D`.  If `<n>T` is missing, `40T` is assumed.

    $ xdm99.py blank.dsk -X DSDD
    $ xdm99.py blank.dsk -X 1d2s80t

`xdm99` cannot create disk images with more than 1600 sectors or with `2S2D80T`
geometry.

The special geometry `CF` is used for disk images for the CF7+/nanoPEB devices
and corresponds to 1600 sectors.

    $ xdm99.py volume.dsk -X cf

You can combine `-X` with other parameters such `-a` to work with the newly
created image immediately:

    $ xdm99.py work.dsk -X SSSD -a file -f DV80

The _disk resize_ option `-Z` will change the total number of sectors of
the disk without changing the contents of the files currently stored.

    $ xdm99.py work.dsk -Z 720

An integer argument will not change the geometry information of the disk.  To
change both size and geometry, `-Z` also accepts a disk geometry string:

    $ xdm99.py corcomp.dsk -Z dssd80t -o ti-80t.dsk  # convert to 80 tracks

Resizing fails if more sectors are used than the target size specifies.

The _geometry option_ `--set-geometry` explicitly sets the number of sides, the
density, and the number of tracks of the disk image.

    $ xdm99.py work.dsk --set-geometry 2S1D80T

The `--set-geometry` command is rarely required for regular images but may be
helpful for experimenting with non-standard disk image formats.

The _sector dump_ option `-S` prints the hexadecimal contents of individual
sectors to `stdout`.  This can be used to further analyze disk errors or to save
fragments of corrupted files.

    $ xdm99.py work.dsk -S 1
    00:  00 02 00 03  00 04 00 05  00 06 00 07  00 08 00 09   .... .... .... ....
    10:  00 0A 00 0B  00 0C 00 0D  00 0E 00 0F  00 10 00 11   .... .... .... ....
    20:  00 12 00 13  00 14 00 15  00 16 00 17  00 18 00 19   .... .... .... ....
    30:  00 1A 00 1B  00 1C 00 1D  00 1E 00 1F  00 20 00 21   .... .... .... . .!
    40:  00 22 00 23  00 24 00 25  00 26 00 27  00 28 00 29   .".# .$.% .&.' .(.)
    50:  00 2A 00 2B  00 2C 00 2D  00 2E 00 2F  00 30 00 31   .*.+ .,.- .../ .0.1
    60:  00 32 00 33  00 34 00 35  00 36 00 37  00 38 00 39   .2.3 .4.5 .6.7 .8.9
    70:  00 3A 00 3B  00 3C 00 3D  00 3E 00 3F  00 40 00 41   .:.; .<.= .>.? .@.A
    80:  00 42 00 43  00 44 00 45  00 46 00 47  00 48 00 49   .B.C .D.E .F.G .H.I
    90:  00 4A 00 4B  00 4C 00 4D  00 4E 00 4F  00 50 00 51   .J.K .L.M .N.O .P.Q
    A0:  00 52 00 53  00 54 00 55  00 56 00 57  00 58 00 59   .R.S .T.U .V.W .X.Y
    B0:  00 5A 00 5B  00 5C 00 5D  00 5E 00 5F  00 60 00 61   .Z.[ .\.] .^._ .`.a
    C0:  00 62 00 63  00 64 00 65  00 66 00 67  00 68 00 69   .b.c .d.e .f.g .h.i
    D0:  00 6A 00 6B  00 6C 00 6D  00 6E 00 6F  00 70 00 71   .j.k .l.m .n.o .p.q
    E0:  00 72 00 73  00 74 00 75  00 76 00 77  00 78 00 79   .r.s .t.u .v.w .x.y
    F0:  00 7A 00 7B  00 00 00 00  00 00 00 00  00 00 00 00   .z.{ .... .... ....

Of course, we can redirect output with `-o`.
 
    $ xdm99.py work.dsk -S 0x22 -o fdr.txt

For convenience, integer arguments of `-S`, `-X` and `-Z` may be specified in
decimal or, with `>` or `0x`, hexadecimal notation.


xhm99 HFE Image Manager                                     <a name="xhm99"></a>
-----------------------

The `xhm99` _HFE image manager_ is an extension to the `xdm99` disk manager that
is both a conversion tool and a manager for HFE images used by the HxC floppy
emulators.


### Converting Images

To convert disk images to HFE images, or vice versa, we use the to HFE and from
HFE options, `-T` and `-F`.  Each option takes an arbitrary number of files.

	$ xhm99.py -T work.dsk
	$ xhm99.py -T work.dsk -o work_dsk.hfe
	$ xhm99.py -F *.hfe

By default, HFE images end in `.hfe`.


### Managing Image Contents

All options other than `-F` and `-T` are similar to those of `xdm99` and operate
directly on the disk image that is contained in the HFE image supplied.

To show the contents of a HFE image, we invoke `xhm99` with no options.

	$ xhm99.py image.hfe
    SOMEDISK  :     4 used  356 free   90 KB  1S/1D 40T  9 S/T
    ----------------------------------------------------------------------------
    SOMEFILE       2  DIS/FIX 60      60 B    1 recs  2016-08-18 20:50:12

To show the contents of a file on the console, use the print argument `-P`.

	$ xhm99.py image.hfe -p SOMEFILE
	Hello xdt99, meet HFE!

You may also add, extract, rename, or delete files:

	$ xhm99.py image.hfe -a manual.txt -f dv80
	$ xhm99.py image.hfe -r MANUAL:README
	$ xhm99.py image.hfe -e SOMEFILE -o greeting.txt
	$ xhm99.py image.hfe -d SOMEFILE

We can create new HFE images with the initialize option `-X`.  Again, we can
combine `-X` with other options.

	$ xhm99.py new.hfe -X dssd -a hello-s.tfi -t

We can also resize HFE images, e.g., if we want to create more free space:

	$ xhm99.py sssd.hfe -Z dssd

The resize argument `-Z` can even change the number of tracks, e.g., converting
from `DSDD` with 40 tracks to `DSSD` with 80 tracks:

	$ xhm99.py dsdd_image.hfe -Z dssd80t

Note that the disk geometry `DSDD80T` is currently not supported.

For further information about available arguments, please refer to the `xdm99`
section.


xvm99 nanoPEB Volume Manager                                <a name="xvm99"></a>
----------------------------

The `xvm99` _volume manager_ is an extension to the `xdm99` disk manager that is
both a conversion tool and a manager for CF card volumes used by nanoPEB/CF7+
devices.


### Managing Volumes

All options require a device name and list of volume numbers.  `xvm99` invoked
without any options prints a short summary of the disk images stored in the
specified volumes.

    $ xvm99.py /dev/sdc 1-4,8
    [   1]  EXTBASIC  :     4 used  1596 free
    [   2]  EMPTY     :     2 used  1598 free
    [   3]  SSSD      :    39 used  1561 free
    [   4]  INFOCOM   :   459 used  1141 free
    [   8]  (not a valid disk image)

The device name is the name or the port our CF card is connected to.  Device
names differ by platform, as well as the method to find out what the correct
device name is.

| Platform | Sample device name  | Command to get device name           |
| -------- | ------------------- | ------------------------------------ |  
| Linux    | /dev/sdc            | fdisk -l                             |
| MacOS    | /dev/disk3          | diskutil list                        |
| Windows  | \\.\PHYSICALDRIVE2  | wmic diskdrive list brief (DeviceID) |

Note that we need to be `Administrator` or `root` in order to access the device.
On Linux, we can use `sudo`, and on Windows, we should start the `cmd.exe`
command prompt as administrator.

Note that the device names listed above are examples only.  We need to run above
commands _every time after we insert a CF card_, since the device name can
change depending on how many devices are connected.

__Caution:__ Make sure you identify your card device correctly, _or you will
lose data!_  __You might even delete your harddisk!__

The second argument of `xvm99` may be a single volume number or a list of value
ranges, e.g., `1,3-4,6-10`.  In general, commands are applied to _all_ volumes.

The write option `-w` writes a disk image to one or more volumes.

    $ xvm99.py /dev/sdc 1,3 -w work.dsk

`xvm99` automatically extends the disk image to match the 1600 sector format
used by the CF7+ device, unless the `--keep-size` option is given.

The read option `-r` reads a disk image from a volume.

    $ xvm99.py /dev/sdc 2 -r vol2.dsk

When reading from multiple volumes, the resulting disk images will be renamed
automatically.  `xvm99` trims disk images to match the sector count stored in
the image, unless the `--keep-size` option is given.


### Manipulating Volumes

Most commands provided by `xdm99` are also available for `xvm99`.

For example, to catalog a volume, you use the same `-i` command as for `xdm99`:

    $ xvm99.py /dev/sdc 8 -i

Other commands supported by `xvm99` are print files `-p`, extract files `-e`,
add files `-a`, delete files `-d`, check disk `-C`, and repair disk `-R`.

Again, if more than one volume is specified, then the command is applied to all
volumes.  For example,

    $ xvm99.py /dev/sdc 1-20 -a README -f DV80

adds the local file README to all disk images in volumes 1 through 20.


Feedback and Bug Reports
------------------------

The xdt99 tools are released under the GNU GPL, in the hope that fellow TI 99
enthusiasts may find them useful.

Please email bug reports and feature requests to the developer at <r@0x01.de>,
or use the issue tracker of the [project][2].


[1]: https://endlos99.github.io/xdt99
[2]: https://github.com/endlos99/xdt99
[3]: https://github.com/endlos99/xdt99/releases
[4]: https://github.com/endlos99/xdt99/blob/master/doc/WINDOWS.md
[5]: https://www.python.org/downloads
[6]: https://endlos99.github.io/finalgrom99
