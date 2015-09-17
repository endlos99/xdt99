*  TEST XDT MACROS

MAIN   LWPI >8300

PROG   DATA 0
       BYTE 1
       EVEN
       DATA >3333
       DATA 0
       BYTE 1
       EVEN
       DATA >3333

       DATA 1
       LI   1,1
       LI   2,'#1'->2
       LI   3,'#2'
       DATA 1
       LI   1,-1
       LI   2,PROG+2-MAIN
       LI   3,'#2'

       DATA 2
LOC1   DEC  1
       JNE  LOC1

       DATA 3
       CLR  @PROG
       NOP
       DATA 3
       CLR  @PROG

       DATA 4
LOC2   DEC  2
       JNE  LOC2

       DATA 5
       DATA 5

       DATA 6
       DATA 1
       CLR  2
       NOP
       CLR  @2
       DATA -1

       DATA 7
       MOV  @MAIN,@>8300

       LI   1,'#1'

       RTWP
       END
