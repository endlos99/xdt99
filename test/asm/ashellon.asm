*  HELLO WORLD

       IDT 'ASHELLO'

       DEF SLOAD,SFIRST,SLAST,START
       REF VSBW,VMBW,VWTR
       REF KSCAN

SLOAD
SFIRST JMP  START
        
WRKSP  EQU  >8300
KMODE  EQU  >8374
KCODE  EQU  >8375
GPLST  EQU  >837C

MESSG  TEXT 'HELLO WORLD'
       TEXT '   hit any key!'
MESSGL EQU  $-MESSG

START  LIMI 0
       LWPI WRKSP

* CLEAR SCREEN

       CLR  R0
       LI   R1,'* '
       LI   R2,24*32

CLS    BLWP @VSBW
       INC  R0
       DEC  R2
       JNE  CLS

* WRITE WELCOME MESSAGE
        
       LI   R0,2*32+3
       LI   R1,MESSG
       LI   R2,MESSGL
       BLWP @VMBW       

* CHECK KEY PRESSES

       LI   R8,>FF00
       CLR  R9
NEXT   LIMI 2
       NOP
       LIMI 0
       MOVB R9,@GPLST
KEYSC  MOVB R9,@KMODE
       BLWP @KSCAN
       CB   @KCODE,R8
       JEQ  KEYSC

       MOVB @KCODE,R0
       SRL  R0,8
       ANDI R0,>000F
       ORI  R0,>0700
       BLWP @VWTR

       JMP  NEXT

SLAST  END
