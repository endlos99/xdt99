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

; optional label colons

colon1  data 1
colon2: data 2
colon3:
colon4:
        data 3
        data colon1, colon2, colon3, colon4

; local labels

glob1   data 1
        jmp  $:
        jmp  :$
glob2   data 2
        data 0
:       data 3
        jmp  $:
        jmp  $::
        jmp  $:::
        jmp  :$
        jmp  ::$
        jmp  :::$
        data 0
:       data 4
        jmp  :$
        jmp  $:
:       jmp  :$
:       jmp  $:
        b    @:$-2
        b    @$:+2
        mov  @:$(1),@$:(2)
glob3   data 5

        end
