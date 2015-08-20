*  NEW FEATURES

        idt 'ASXNEW'

start   blwp @0

; binary literals

binval  equ  :1010
        data :01011010,:11110000
        byte binval

; binary includes

bininc  byte >AA
        ibyte "asxnew.bin"
        byte >BB
        ibyte "asxnew.bin"
        byte >CC

; text bytes

txtbyt  text >1234567890abcdef
        text >123
        text ->123456

; local labels

glob1   data 1
        jmp  !
        jmp  +!
        jmp  -!
        jmp  --!
glob2   data 2
        data 0
!       data 3
        jmp  !
        jmp  !!
        jmp  !!!
        jmp  -!
        jmp  -!!
        jmp  -!!!
        data 0
!       data 4
        jmp  -!
        jmp  !
!       jmp  -!
!       jmp  !
        b    @-!-2
        b    @!+2
        mov  @-!(1),@!(2)
glob3   data 5

; label continuations

lreg1   data 1
lreg2
lreg3   data 2
lreg4
lreg5   equ  3
lreg6
        aorg >a200
lreg7   data 4

        data lreg1, lreg2, lreg3
        data lreg4, lreg5, lreg6
        data lreg7

lcont1: data 1
lcont2:
        data 2
lcont3:

        data 3
lcont4: equ  4
lcont5:
        equ  5
lcont6:
        aorg >a200
lcont7:
        bes  10

        data lcont1, lcont2, lcont3
        data lcont4, lcont5, lcont6
        data lcont7

        end
