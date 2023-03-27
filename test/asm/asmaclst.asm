* macro call in list file

       aorg >2000

       .defm push
       dect r10
       mov  #1, *r10
       .endm

start  limi 0
lab    .push r2  ; save register
       limi 2
       data lab

       end
