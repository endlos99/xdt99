*  TEST XDT MACROS

main   lwpi >8300

       .defm mac0     comment #1
       byte 1         comment #1 '
       even           comment #11
       copy "DSK2.ASCOPY3"
       .endm

       .defm mac3
       li   1, #1     comment #11
       li   2, #3 - #2
       li   3, '#2'
       .endm

       .defm mac1a
       clr  #1
       nop
       .endm

       .defm mac1b
       clr  @#1
       .endm

       .defm macj
!loc   dec  #1
       jne  -!loc
       .endm

       .defm macnull
       .endm

       .defm macnest
       data #1
       .mac1a #2
       .mac1b #2
       data -#1
       .endm

       .defm macglob
       mov @main, #1
       .endm

       .defm macif
       .ifdef doesnotexist
       inc #1
       .else
       dec #1
       .endif
       .endm

prog   data 0
       .mac0
       data 0
       .mac0

       data 1
       .mac3 1, >2, '#1'
       data 1
       .mac3 -1, main, prog + 2

       data 2
       .macj 1

       data 3
       .mac1a @prog
       data 3
       .mac1b prog

       data 4
       .macj 2

       data 5
       .macnull
       data 5
       .macnull 1, 2, 3, 4

       data 6
       .macnest >1, 2

       data 7
       .macglob @>8300

       data 8
l0
l1     .mac1b >1234
l2     .mac1b l2
       data l0, l1, l2

       data 9
       .macif 9

       li   1, '#1'

       rtwp
       end
