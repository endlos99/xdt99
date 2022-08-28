; invalid symbols

       aorg >2000

!foo   equ  1   ;ERROR
@bar   equ  2   ;ERROR

!bar   data 3
a*b    data 4   ;ERROR
&ab    data 5   ;ERROR

123    equ  6   ;ERROR
123b   equ  7   ;ERROR

$      data 8   ;ERROR
@xyz   data 9   ;ERROR
-ab    data 10  ;ERROR
a#b    data 11  ;ERROR
a&b    data 12  ;ERROR
a,b    data 13  ;ERROR
a()b   data 14  ;ERROR
a^b    data 15  ;ERROR
a~b    data 16  ;ERROR
a%b    data 17  ;ERROR
a"b    data 18  ;ERROR
a'b    data 19  ;ERROR
a,b    data 20  ;ERROR

a.b    data 0
a:b    data 0
* a;b    data 0  (misinterpreted)
a[]b   data 0

       end
