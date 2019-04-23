*  NEW FEATURES

        idt 'ASXNEW'

start   blwp @0

; binary literals

binval  equ  :1010
        data :01011010,:11110000
        byte binval

; binary include_path

bininc  byte >AA
        bcopy "asxnew.bin"
        byte >BB
        bcopy "asxnew.bin"
        byte >CC

; text bytes

txtbyt  text >1234567890abcdef
        text >123
        text ->123456

; local labels

glob1   data 0
!       data 1
        jmp  !
        jmp  +!
        jmp  -!
        jmp  --!
        jmp  -+!
        jmp  +-+!
glob2   data 0
!       data 2
        jmp  !
        jmp  !!
        jmp  !!!
        jmp  -!
        jmp  -!!
        data 0
!       data 3
        jmp  -!
        jmp  !
!       jmp  -!
!       jmp  !
!       b    @-!-2
        b    @!+2
        mov  @-!!(1), @!(2)
ambi    data 0
        jmp  ambi
        jmp  !ambi
!ambi   data 4
!loc1   data 5
!       data 6
!loc11  data 7
        jeq  -!
        jeq  -!loc1
        jeq  -!loc11
        mov  @!loc1, @-!loc1
!loc1   data 8
        jeq  -!!loc1

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

; label continuations (edge case, keep at end)

!:
        jmp !
!       nop
        jmp -!
        jmp -!!

; F18A GPU support

f18a:
        call @f18a
        call *1
        ret

        push 1
        push @>2222
        pop  *2+
        pop  @>3(4)

        slc  1, 2
        slc  2, 0

        pix  1, 2
        pix  @>1234(5), 0

        end
