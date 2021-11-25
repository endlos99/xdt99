* pragmas: timing
* s-/d- fast (unmuxed), s-/d- slow (muxed)

* part 1

       aorg >a000
       lwpi >8300
x      data 0

       a    *r1, @2(r2)
       a    *r1, @2(r2)   ;: s-
       a    *r1, @2(r2)
       a    *r1, @2(r2)   ;: d-
       a    *r1, @2(r2)
       a    *r1, @2(r2)   ;: s-d-
       a    *r1, @2(r2)

       cb   @x, *r1+
       cb   @x, *r1+   ;: s-
       cb   @x, *r1+   ;: d-
       cb   @x, *r1+   ;: s-d-

       mov  r1, r2
       mov  r1, r2   ;: s-
       mov  r1, r2   ;: d-
       mov  r1, r2   ;: s-d-

       inc  *r1+
       inc  *r1+   ;: s-
       inc  *r1+   ;: d-
       inc  *r1+   ;: s-d-

       dec  @x
       dec  @x   ;: s-
       dec  @x   ;: d-
       dec  @x   ;: s-d-

       bl   @2(r1)
       bl   @2(r1)   ;: s-

       blwp r1
       blwp r1   ;: s-

       tb   0
       tb   0   ;: s-

       andi r1, 1
       andi r1, 1   ;: s-
       andi r1, 1   ;: d-
       andi r1, 1   ;: s-d-

       rtwp
       rtwp   ;: s-
       rtwp   ;: d-
       rtwp   ;: s-d-

       sla  r1, 3
       sla  r1, 3   ;: s-

       ldcr @2(r1), 5
       ldcr @2(r1), 5   ;: s-

       stcr *r1+, 10
       stcr *r1+, 10   ;: s-

       mov  r1, r2
       mov  r1, r2   ;: s+
       mov  r1, r2   ;: d+
       mov  r1, r2   ;: s+d+


* part 2

       xorg >8320
       lwpi >2000

       ; NOTE: the "unknown" memory accesses won't be not penelized by waitstates
       ;       just because default memory accesses have no waitstates

       a    *r1, @2(r2)
       a    *r1, @2(r2)   ;: s-
       a    *r1, @2(r2)   ;: d-
       a    *r1, @2(r2)   ;: s-d-
       a    *r1, @2(r2)   ;: s+
       a    *r1, @2(r2)   ;: d+
       a    *r1, @2(r2)   ;: s+d+

       end

