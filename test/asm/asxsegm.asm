* MERGING SEGMENTS
* RELOC SEGMENTS REBASED ON >A000 FOR IMAGES!

       DATA >1001, >1002             ; 1

       AORG >B000                    ; 2
       DATA >2001, >2002

       AORG >B008
       DATA >2005, >2006, >2007      ; 2

       AORG >B004                    ; 2
       DATA >2003, >2004

       RORG
       DATA >1003, >1004             ; 1

       AORG >B010                    ; 3
       DATA >3001

       AORG >B012                    ; 3
       DATA >3002, >3003, >3004

       AORG >A010                    ; 1 (!)
       DATA >1009, >1010

       RORG                          ; 1
       DATA >1005, >1006

       XORG >8300                    ; 1
       DATA >1007

       RORG                          ; 1
       DATA >1008 

       END
