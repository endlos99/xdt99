xdt99 Utilities
===============

This directory contains some assembly utility functions for `xas99`, including
the functions provided by Editor/Assembler.


Utilities
---------

The utilities provided by E/A are always called by `BLWP`.  The utilities listed
here, however, are universally called by `BL`, and modify registers `R0` and
potentially up to `R3`.


### `vsbw.asm` - VDP single byte write

Writes the MSB of `R1` to VDP memory address `R0`.


### `vmbw.a99` - VDP multi byte write

Writes `R2` bytes starting from CPU memory address `R1` to starting at VDP
memory address `R0`.


### `vsbr.asm` - VDP single byte read

Reads single byte from VDP memory address `R0` and stores it in MSB of `R1`.


### `vmbr.asm` - VDP multi byte read

Reads `R2` bytes starting from VDP memory address `R0` and stores them starting
at CPU memory address `R1`.


### `vwtr.asm` - VDP write to register

Writes the byte value in LSB of `R0` to VDP register MSB of `R0`.


### `vsbmw.asm` - VDP single byte multi-write

Writes the MSB of `R1` for `R2` times to starting at VDP memory address `R0`.


### `vwzw.asm` - VDP multi-byte zero-terminated write

Write bytes starting from CPU memory address `R1` to starting at VDP memory
address `R0`, until a zero byte is read, which is not written.


### `vwwt.asm` - VDP write word as text

Writes the word value in `R1` as text in hexadecimal starting from VDP memory
address `R0`.  Also uses `R2` internally.  `R0` not stable.


### `vwbt.asm` - VDP write byte as text

Writes the byte value in MSB of `R1` as text in hexadecimal starting from VDP
memory address `R0`.  Also uses `R2` internally.  `R0` not stable.


### `memset.asm` - set memory

Set `R2`/2 words in CPU memory starting at address `R0` to `R1`.  `R0` not
stable.


### `memcpy.asm` - copy memory

Copies `R2`/2 words starting from CPU memory address `R1` to starting at CPU
memory address `R0`.  `R0` not stable.


Compatibility Utilities
-----------------------

`xas99` also provides E/A-compatible versions of some of the utilities above:

    vsbw_ea.asm
    vmbw_ea.asm
    vsbr_ea.asm
    vmbr_ea.asm
    vwtr_ea.asm
    kscan_ea.asm

There utilities are called by `BLWP` and can be used as drop-in replacements for
E/A utilities.  All of these functions use the workspace starting at `>2094`.

Note that even the filename ends in `_ea`, the actual function name does _not_
do so, i.e., `vwtr_ea.asm` still defines function `vwtr`.

There is no non-compatible `kscan.asm` utility, since we can call `SCAN`
directly.


Usage
-----

There are two ways to use these functions (both compatible and non-compatible):

(1)  We can include any function with a `COPY` directive, e.g.,

    COPY "vsbw.asm"
    
`xas99` will search the `lib/` directory automatically.

(2)  We can supply any function on the command line, e.g.,

    $ xas99.py myprog.asm vsbw_ea.asm
    
In `myprog.asm`, each function additionally must be imported by `REF`, e.g.,
`ref vsbw`.  We don't need to prefix `vsbw.asm` by `lib/`.
