* .rept

r:
       equ  2
n:
       equ  0

       rorg

       data >1111

       .rept r + 1
       data >2222
       .endr

       data >8888

       .rept n
       data >eeee
       .endr

       data >ffff

       end
