* SPLIT IMAGE


WRKSP  EQU  >8300
VDPWD  EQU  >8C00            VDP WRITE DATA
VDPWA  EQU  >8C02            VDP R/W ADDRESS


       AORG >A000
       LIMI 0
       LWPI WRKSP

       LI   R1,'* '          CLEAR SCREEN
       BL   @VCLS

       LI   R0,33            WRITE MESSAGE
       LI   R1,M0
       LI   R2,4
       BL   @VWRT

       B    @PART1

VCLS
       CLR  R0
       LI   R2,768           SUBROUTINE CLEAR SCREEN
       MOVB @WRKSP+1,@VDPWA
       ORI  R0,>4000
       MOVB R0,@VDPWA
VCLSL  MOVB R1,@VDPWD
       DEC  R2
       JNE  VCLSL

       RT

VWRT
       MOVB @WRKSP+1,@VDPWA  SUBROUTINE WRITE TO SCREEN
       ORI  R0,>4000
       MOVB R0,@VDPWA
VWRTL  MOVB *R1+,@VDPWD
       DEC  R2
       JNE  VWRTL

       RT

M0     TEXT 'MAIN'


       AORG >B000
PART1
       LI   R0,65            WRITE MESSAGE
       LI   R1,M1
       LI   R2,5
       BL   @VWRT

       B    @PART2

M1     TEXT 'PART1'


       AORG >D000
PART2
       LI   R0,97            WRITE MESSAGE
       LI   R1,M2
       LI   R2,5
       BL   @VWRT

       B    @PART3

M2     TEXT 'PART2'


       AORG >C000
PART3
       LI   R0,129           WRITE MESSAGE
       LI   R1,M3
       LI   R2,5
       BL   @VWRT

       LIMI 2                DONE
DONE   JMP  DONE

M3     TEXT 'PART3'


       END
