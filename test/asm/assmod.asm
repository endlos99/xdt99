    aorg >2000

;const:
;   equ  s#text2          ;ERROR
value:
    equ  >2010

    ; s# terms
    data >1111
    li  r1, s#text1
    ai  r2, s#text2
    ai  r3, -s#text3
    data s#pad
    ;data s#value         ;ERROR

    ; self-#s
l1  data s#l1
    byte 1, 2, 3, 4, 5
l2  data >ffff

    ; s# expressions
    data s#text1 + 10
    data s#text1 + s#text2
    data s#text4
    data >aaaa

    ; s# and padding bytes
    data s#pad

text1 text 'HELLO WORLD'
text2 data 1, 2
      data 3, 4
text3 stri 'FOOBAR'
text4 text >1234567890    ;WARN

pad   byte 1
      byte 2
      byte 3
padend

    end

