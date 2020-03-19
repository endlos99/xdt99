* set memory to word value

* set <r2> bytes at <r0> to word <r1>
* NOTE: <r2> must be even and not equal 0!

       ref memset
memset:
       mov  r1, *r0+
       dect r2
       jne  memset
       rt
