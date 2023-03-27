* SYMBOLS GENERATION TEST

       REF  VDPWA,SCAN
       REF  Z

S1     EQU  1

START  LIMI 0
       LI   R0,1
       MOV  R0,R1
       MOVB R2,@VDPWA

       BL   @S2

       LIMI 2
       JMP  $

S2     CLR  R1
       BLWP @SCAN
       RT

       END
