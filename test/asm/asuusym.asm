s1  byte 1
u1  byte 2
s3  data 5

    movb @s1, r0
    mov  @s2, r1

s2  data 3
u2  data 4

u3  data s3

s4  data s5
s5  data s4

n1  nop
s6  data s6

u4  text 'HELLO'
u5  stri 'WORLD'

    end

