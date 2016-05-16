This directory contains some utilities.

 * `vsbw.a99`: single-byte write to VDP memory
 * `vmbw.a99`: multi-byte write to VDP memory
 * `vsbmw.a99`: single-byte multiple write to VDP memory
 * `vsbr.a99`: single-byte read to VDP memory
 * `vmbr.a99`: multi-byte read to VDP memory
 * `vwtr.a99`: write to VDP register
 * `memset.a99`: set memory area to word value
 * `memcpy.a99`: copy memory area (non-overlapping)
 * `dsrlnk.a99`: call DSR routine (self-modifying)
 * `dsrlnks.a99`: call DSR routine
 * `gpllnk.a99`: call GPL routine (self-modifying)

To include one of these files add the following directive to your assembly
program:

    COPY "vsbw.a99"

If the files are not in the same directory as your assembly program you will
have to specify their location with the `-I` option, e.g.,

    xas99.py source.a99 -I <xdt99>/lib

where `<xdt99>` refers to your xdt99 installation directory.
