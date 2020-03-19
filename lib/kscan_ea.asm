* key scan

       def  kscan
       ref  scan

kscan:
       data >2094
       data !kscan

!kscan:
       lwpi >83e0
       mov  r11, @>20aa
       bl   @scan
       lwpi >2094
       mov  r11, @>83f6
       rtwp
