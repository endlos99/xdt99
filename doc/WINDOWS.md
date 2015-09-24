xdt99 Windows Tutorial
======================

This is a brief tutorial aimed at Windows users to guide through the
installation process and to introduce the command-line interface of xdt99.

Note that OS X already ships with Python preinstalled, and for Linux the package
manager of your distribution will install and configure Python automatically for
you.


Installation
------------

For most Windows users, installation is a two-step process, as we need to get
both Python and xdt99.


### Python

xdt99 is written in the [Python programming language][1], which is easy to learn
and available for all major platforms.  Linux and OS X already ship with Python,
but on Windows you need to install it yourself.  No worries, though: After
installation, you won't have to deal with Python ever again.

Go to the [Python download page][2] and select the latest available Python 2
release.  As of this writing, this is version 2.7.10.  *Caution:* Python 3 will
not work!  The downloaded file should be a Windows installer with extension
`.msi`.  Double-click on the file and the installer will guide you through the
installation process.  Python won't modify your system and is easily uninstalled
again if you don't like it.

To check if the installation was successful, open a command prompt (also known
as "DOS box") by opening the Start menu, selecting "Run ...", and entering
`cmd.exe`.  In the resulting window, type

    python

and hit `Return`.  You should see a response like

    Python 2.7.10 (default, May 23 2015, 09:44:00) [MSC v.1500 64 bit (AMD64)]
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Congratulations, you're running Python now!  Play around with it, or just close
the window.


### xdt99

Once Python is running, we can proceed to install xdt99, which is just as
simple.

Download the latest release `xdt99.zip` from the [project page][3] and unzip the
archive somewhere on your disk, say `c:\xdt99`.

Again, open a command prompt (Start > Run ... > `cmd.exe`) and change to the
xdt99 directory by typing

    > cd c:\xdt99

Don't type the `>`, though.  This character (like the Linux `$` used in the
xdt99 manual) merely represents the command prompt presented to you by Windows.

To check if xdt99 is working type

    > xas99.py -h

You should see the usage information of the xas99 assembler:

    usage: xas99.py [-h] [-v] [-i | -c | --embed-xb | --jumpstart] [-s]
                    [-n <name>] [-R] [-C] [-L <file>] [-S] [-I <paths>]
                    [-D <sym=val> [<sym=val> ...]] [-o <file>]
                    <source>
	
    TMS9900 cross-assembler
    ....

To finalize the installation you need to add xdt99 to your "command search path"
by opening Control Panel > System > Advanced System Settings > Environment
Variables.  In the upper window called "User Variables" search for a `PATH`
entry.  If there is one, double-click on it and append

    ;c:\xdt99

to the "Variable Value" line (use the installation directory you chose above).
If there is no `PATH` entry, create one by clicking "New" and entering

    PATH
    c:\xdt99

into the popup window (again, use the installation directory from above).  In
both cases you need to close all `cmd.exe` windows for the changes to take
effect.

That's it -- you're ready to start developing with xdt99!


First Steps with `xas99`
------------------------

Let's take xdt99 for a spin by assembling our first program.

The `example` folder in the xdt99 installation directory contains some sample
programs.  Change to this folder and compile the assembly program `ashello.asm`
by typing:

    > cd example
    > xas99.py -R ashello.asm

The `-R` option corresponds to the `R` option of the original TI assembler and
tells `xas99` to use register symbols `R0`, `R1`, ... instead of `0`, `1`, ....

Assembly will generate an object code file `ashello.obj` that is suitable for
the Editor/Assembler cartridge option 3.  You can have a look at the file by
typing

    > type ashello.obj

but it's just gibberish intended for the E/A loader.  (Note, however, that it's
plain ASCII text, not binary data as an `.exe` file on Windows would be.)

To run the program in an emulator such as Classic99 you need to copy it onto a
virtual disk or convert it to a format that Classic99 understands.  File
operations are handled by the Disk Manager `xdm99` tool that is part of xdt99:

    > xdm99.py -T ashello.obj -n ASHELLO -f DF80

This command tells `xdm99` to convert the object code file `ashello.obj` to a
FIAD file in `TIFiles` format that Classic99 and even a real TI 99 will
understand.  The `-n` option sets the TI filename to `ASHELLO` and the `-f`
option sets the file format to `DIS/FIX 80`.

Start Classic99 with the Editor/Assembler cartridge and assign the folder
`c:\xdt99\example` to `DSK1`.  Select the Editor/Assembler from the TI main menu
and load and run program `DSK1.ASHELLO` using E/A Option 3.  The start name of
the program is `START`.

You should see the canonical greeting of programmers world-wide.

    HELLO WORLD   hit any key!

If you're using the MESS emulator you need to create a floppy disk image instead
of a `TIFiles` file.  This is also easily done with `xdm99`:

    > xdm99.py hello.dsk --initialize SSSD -a ashello.obj -f DF80

This command creates a new single-sided, single-density disk image `hello.dsk`
and adds the file `ashello.obj` in format `DIS/FIX 80` using the default TI file
name `ASHELLO`.  You can catalog the disk image just created by typing

    > xdm99.py hello.dsk

You'll see that the disk contains a single file `ASHELLO` with our program.

    HELLO     :     6 used  354 free   90 KB  1S/1D  40 TpS
    ----------------------------------------------------------------------------
    ASHELLO        4  DIS/FIX 80     752 B    9 recs  2015-09-22 20:15:24    

You can look at the contents of any file by using the `-p` print option:

    > xdm99.py hello.dsk -p ASHELLO

will print the familiar gibberish.  If you want to save the file instead simply
use `-e` for "extract" instead:

    > xdm99.py hello.dsk -e ASHELLO

Now start the MESS emulator with the TI 99 emulation and insert the disk image
`hello.dsk` using the on-screen menu.  Alternatively, you could supply the image
on the command line, for example

    > mess64 ti99_4a -peb:slot2 32kmem -peb:slot8 tifdc
                                     -cart editor-assembler.rpk -flop1 hello.dsk

You may have to adjust this line to match the name of your E/A cartridge.

From here on it's the same as Classic99 -- start the Editor/Assembler and select
option 3 to load and run `DSK1.ASHELLO`.

You've just assembled and run your first assembly program!


Working with BASIC
------------------

If you prefer BASIC to assembly you can use the `xbas99` tool to work with TI
BASIC and TI Extended BASIC programs.

You've probably noticed that TI BASIC programs are not saved as plain text
files.  In other words, if you try to load the sample file `colors.b99` in
Classic99 you'll get an I/O error:

    >OLD DSK1.COLORS.B99
     * I/O ERROR 50

BASIC programs need to be "tokenized" for the TI 99 to understand.  One way of
doing that is to copy and paste the text file into Classic99 or MESS and let the
BASIC interpreter do the tokenization.

For program development, where you frequently need to test and run updated
versions of your code, using a conversion tool such `xbas99` is often more
efficient:

    > xbas99.py colors.b99

This will tokenize the BASIC program `colors.b99` and create a program file
`colors.prg` that the TI BASIC and TI Extended BASIC interpreters will
understand.

To run the tokenized program, we first use `xdm99` to prepare the file for
Classic99

	> xdm99.py -T colors.prg -o COLORS

or for MESS

    > xdm99.py hello.dsk -a colors.prg

The BASIC program can now be loaded in your emulator (or on a real TI 99):

    RUN "DSK1.COLORS"

Of course, `xbas99` also supports the other way around.  Let's edit the Colors
program by changing the patterns.  Within the emulator, replace line 130 by

    130 CALL CHAR(24+I*8,"010307
    0F1F3F7FFF80C0E0F0F8FCFEFFFF
	00FF00FF00FF00"):: CALL COLO
	R(I,I+1,I+2)

and save the modified program

    SAVE DSK1.DIZZY

To get at the listing in Windows we first extract it from the TIFiles file

    > xdm99.py -F DIZZY -o dizzy.prg

or the disk image

    > xdm99.py hello.dsk -e DIZZY -o dizzy.prg

and then use `xbas99` to list it in the command prompt window:
	
    > xbas99.py -l dizzy.prg

If you want to save the listing instead of displaying it simply replace `-l` by
`-d` (for decode).

You may have noticed that it takes two steps to list a BASIC program that is
stored on a disk: First you need to extract it using `xdm99`, and then you need
to decode it using `xbas99`.  It would seem like a sensible idea to include the
`xbas99` functionality into `xdm99` to simplify these steps, but this is against
the Unix philosophy of "Doing one thing and doing it well".

xdt99 follows the Unix philosophy for its command-line tools, even on Windows,
as it offers great flexibility in combining tools in ways that their creators
did not foresee.  For example, to list a BASIC program that is stored on a disk
image we can use the pipe operator `|` to chain the extraction and the listing
steps together:

    > xdm99.py hello.dsk -p DIZZY | xbas99.py -l -

This tells `xdm99` to print the contents of `DIZZY` not to the screen (where it
would show up as gibberish) but to the command behind the pipe symbol, i.e., the
`xbas99` command.  The special filename `-` tells `xbas99` that it should use
the pipe instead of a file as input.

Using pipes is powerful but requires practice.  Fortunately, there's an
alternative way.  To combine multiple steps into one single command or to cut
down on the amount of typing required for commands you use over and over again
you can create batch files that will automate the tediousness for you.

For example, like the pipe example above, this simple batch file `list.bat`

    @echo off
    xdm99.py %1 -e %2 -o _tempfile_
    xbas99.py -l _tempfile_
    del _tempfile_

will list a BASIC program stored on a disk image to the screen:

    > list.bat hello.dsk COLORS
    100 REM COLORS
    110 CALL CLEAR :: CALL SCREEN(1)
    120 FOR I=2 TO 14
    ....

Check the `help` command available on the Windows command line.  The section
`help set` will tell you quite a bit about batch programming, and of course
there are also many tutorials available on the Web.

Investing some time on learning the command line will save you a lot of
development time in the long run!


Further Reading
---------------

This tutorial covered the first steps of getting up and running with xdt99.  The
main manual `MANUAL.md` (or `manual.html` if you prefer a nicely rendered copy)
contains another tutorial section that will walk you more thoroughly through the
xdt99 tools and their major features.

The `ide/` folder contains plugins for the GNU Emacs editor and the IntelliJ
IDEA development environment that assist developers in writing assembly or TI
BASIC programs.  Features include colored syntax highlighting, navigation to
symbol declarations and usages, and semantic renaming, to name just a few.
Please check the `EDITORS.md` file for additional information.

If you've found a bug or would like to provide feedback, or simply if you're
stuck at some point, feel free to send an email to <xdt99dev@gmail.com>.


[1]: https://en.wikipedia.org/wiki/Python_%28programming_language%29
[2]: https://www.python.org/downloads/
[3]: https://github.com/endlos99/xdt99/releases
