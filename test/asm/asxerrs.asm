*  ERROR HANDLING: xdt99 extensions

       idt 'ASXERRS'

       ; binary includes

bininc ibyte "nonexisting"    ;ERROR

       ; text bytes

text1  text >123456
       text >12x34            ;ERROR
       
       ; label continuations

label1:
label2:                       ;ERROR
       clr  0

label3:
       clr  0
label3 clr  1                 ;ERROR

label4 clr  0
label4:
       clr  1                 ;ERROR
       
       end

* NO ERRORS

good1:
       ; comment
       clr  0

       end
