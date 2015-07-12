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

        end
