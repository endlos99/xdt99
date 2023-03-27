Changes Version 3.6.0
=====================

xas99 Cross-Assembler
---------------------

### Creating Binaries

The `-b` option will create one file per bank per `SAVE` directive.  To join
these files into a single file, we can use the _joined binary option_ `-B`.  
This option will also align the start address of the binary to a multiple of
`>2000`.  If the _minimize option_ `-M` is not supplied, the binary is also
padded to a multiple of `>2000`.


### Creating MAME Cartridges

If the source code does not contain a GPL header, `xas99` will automatically add
one.  In this case, the _name option_ `-n` can be used to set the program name
that will be displayed in the menu screen.

When adding a GPL header, `xas99` replaces bytes `>6000` through `>602F` with
the header data.  Thus, if we want to make use of this functionality, our
program should start at address `>6030` or higher.  `xas99` will issue a warning
if the GPL header overwrites any non-zero data.

If the program is entirely relocatable, i.e., using `RORG` but no `AORG`, a GPL
header is added if no header is found at relocatable addresses `>0000` or
`>6000`.  For `>0000`, the program is also relocated to base address `>6000`.

The first word in the code must be an executable instruction, or we need to
supply the start symbol as operand of the `END` directive, like was done in 
`ascart.asm`.


xga99 GPL Cross-Assembler
-------------------------

### Assembling Source Code

The _pad option_ `-B` pads each GROM with zero bytes so that it starts at
address _G_ * `>2000` and is >2000 bytes in size.

The _cartridge option_ `-c` generates an RPK cartridge file suitable for the 
MAME emulator.  The option implies `GROM 6` and will create a GPL header in the
lowest GROM of the program automatically if no header is found at `>6000`,
`>8000`, ..., or `>E000`.

    $ xga99.py -c gahello.gpl

`xga99` will issue a warning if the generated GPL header overwrites any non-zero
data.



Changes Version 3.5.5
=====================

xbas99 TI BASIC and TI Extended BASIC Tool
------------------------------------------

### xdt99 Extensions

`xbas99` also supportes _local labels_ starting with `%`, which are not visible
outside the subprogram in which they are defined.

    MAIN:
     CALL A(X) :: CALL B(X)
     GOTO MAIN
     SUB A(X)
    %LABEL:
     X=INT(RND*10) :: IF X=5 THEN %LABEL
     SUBEND
     SUB B(X)
    %LABEL:
     PRINT X :: X=X-1 :: IF X>=0 THEN %LABEL
     SUBEND

Internally, `xbas99` prepends each local label with the surrounding subprogram
name, making each local label globally unique.

Local labels cannot be defined or used outside of subprograms.

The _shorten label option_ `-S` takes a BASIC program with labels and creates an
equivalent BASIC program with labels where no label is longer than 6 chars.
This is achieved by shortening original label names to 6 chars and resolving any
conflicts by replacing conflicting label suffixes by increasingly large numbers.

This resulting program with default extension `.xbc` is a valid input for the
Extended BASIC compiler by senior_falcon.



Changes Version 3.5.4
=====================

xbas99 TI BASIC and TI Extended BASIC Tool
------------------------------------------

### xdt99 Extensions

Currently, `xbas99` supports only one extension to the standard BASIC syntax.

In quoted strings (delimited by `"`) and unquoted strings (used, e.g., in `DATA`
values without quotes), we can include non-ASCII characters by specifying their
code point with `\x`_nn_ and `\d`_nnn_.  `\x` takes a two-digit hex value, and
`\d` a three-digit decimal value.

For example, both lines

    200 PRINT "- \xa1 ... 10 POINTS"
    200 PRINT "- \d161 ... 10 POINTS"

are equivalent to line

    200 PRINT "- "&CHR$(161)&" ... 10 POINTS"

but while the former generates a single literal, the latter only generates an
expression that is evaluated at run-time.  Thus, using `\d` and `\x` is faster
(and more concise) than using `CHR$`.

An invalid escape code, such as `\x1foo` or `\d\x`, yields an error.

If we want to include either `\x` or `\d` in a string verbatim, we need to write
`\\x` or `\\d`, resp.  Note, however, that `\\` still yields `\\`.

To disable character escape codes entirely, we can use the strict option `-s`.



Changes Version 3.5.2
=====================

Installation
------------

All xdt99 files should be placed somewhere in the `$PATH` or where the
command-line interpreter will find them.  Windows users will find Windows-
specific instructions in the [Windows Guide][4].


Tutorial
--------

### Includes and Filename Handling

Please note that both path separators `/` and `\` are supported by `xas99`,
independent of the platform used.  If both separators occur within one path,
however, only the platform-native char is used as separator.


### Options with List Arguments

As we explained in the tutorial, for options with multiple arguments, individual
arguments may be separated by `,` or space.  When using spaces, however, Python
is not able to determine where the list of arguments ends:

    $ xas99.py -I lib helper sample.asm

Is `sample.asm` an include path, or a source file?  What about `helper`?

In general, non-options like the source file (or the disk name for `xdm99`)
should never occur after multi-argument options.  In the case of options in
`XAS99_CONFIG`, however, this is not possible, as environment options are
prepended to the command line.

To allow multi-argument options in the environment, the list argument
terminator `;` was introduced.  The statements

    $ xas99.py -I incl1 incl2; source.asm
    $ xas99.py -I incl1 incl2 ; source.asm

both define include paths `incl1` and `incl2` with source file `source.asm`
without errors.  The terminator is still required if only one argument is given:

    $ xas99.py -I incl; source.asm

Please be aware that on Linux and macOS platforms, a `;` on the command line
has special meaning, so the `;` has to be enclosed in parentheses.

    $ xas99.py -I incl1 "incl2;" source.asm
    $ xas99.py -I incl1 incl2 ";" source.asm

This restriction does *not* apply to `XAS99_CONFIG`, though.

Having said all that, it is rather unfortunate that the built-in help for
`xas99` shows the source files after all list options without termination.

    usage: xas99.py [...]
                    [-I <path> [<path> ...]] [-D <sym[=val]> [<sym[=val]> ...]]
                    [...]
                    [<source> ...]

We regret that we were unable to include this particular aspect of list options.


xas99 Cross-Assembler
---------------------

### New directives [new summary]

In additional to the directives supported by E/A, `xas99` add some new
directives that simplify some tasks or control advanced functionality.

    BCOPY STRI FLOA WEQU REQU XORG BANK SAVE AUTO

The `BCOPY` directive includes an external binary file as a sequence of `BYTE`s.
For example, if `sprite.raw` is a raw data file containing the sprite pattern

    00000000  18 3c 7e ff ff 7e 3c 18                           |.<~..~<.|

then including this file with `BCOPY`

    sprite  bcopy "sprite.raw"

is equivalent to statement

    sprite  byte >18,>3c,>7e,>ff,>ff,>7e,>3c,>18

The `STRI` directive is similar to `TEXT`, but prepends a length byte, so

    stri 'HELLO WORLD'

is equivalent to

    byte 11
    text 'HELLO WORLD'

Note that both `TEXT` and `STRI` also support hex strings of arbitrary lengths

    text >183c7effff7e3c18

so non-ASCII characters can easily be included withinin a text string:

    text 'THIS ', >a2, ' IS YOUR PLAYER.'

When multiple arguments are provided to `STRI`, they are contatenated before
prepending the length byte, so the following two instructions are equivalent:

    stri 'hello', >40, 'world'
    text >0b, 'hello@world'

The `FLOA` directive stores a _floating point number_ in the 8-byte RADIX-100
format used by the TI 99.  Note that digits exceeding the accuracy of RADIX-100
are silently ignored.

    floa 123.456789012

The exponent notation `1e9` is currently not supported.

The `WEQU` directive defines a _weak `EQU`_ that works like a normal `EQU`, but
its value may be redefined.  For each rededinition, a warning is issued.

Please note that `WEQU` is still experimental, and its behavior might change in
a future version of `xas99`.

The `REQU` directive defines a _register alias_, which can give registers `R0`
through `R15` more expressive names.  While any symbol can be used in a register
position as long as its value is valid, `REQU` highlightes which symbols are
used instead of `R`_n_.

    val  equ  1
    reg  requ 2
         clr  reg        ; intended usage
         inc  val        ; also valid to keep compatibility with E/A
         dec  @reg       ; valid, but issues usage warning

A symbol and a register alias cannot have the same name.

Note that register aliases can be used without specifying the `-R` option.

Using `REQU` for register aliases instead of plain `EQU` helps pruning the
suggestions for code completion in register positions when using the [IDEA
plugin][8].  Unlike `xas99`, the plugin clearly separates between aliases and
regular symbols and only considers one symbol type in any given context.


### Pragmas

Comments and pragmas can occur on the same line in arbitrary order

    inc 0   ; advance to next item ;: warnings = off
    inc 0   ;: warnings = off ; advance to next item

but they cannot be split.

    inc 0   ;: s+d- ; advance to next item ;: warnings = off
    inc 0   ; advance to next item ;: warnings = off ; disable all warnings


xdm99 Disk Manager
------------------

### Disk geometry

The size of the disk image is given by the number of sectors.  You may also use
a disk geometry string, which is a string `<m>S<n>D` or `<m>S<n>D<t>T`, where
`<m>` is the number sides, `<n>` the density and `<t>` the number of tracks.
`<m>` and `<n>` can be one of `1`, `2`, `S`, or `D`.  If the number of tracks
is not provided, 40 tracks are assumed.
