* cycle timing

* part 1

       aorg >a000
       lwpi >8300
s      data 0

       limi 0

       mov  r1, r2
       movb @s, *r1
       a    @s, @2(r2)
       ab   *r1+, @s
       szcb @2(r1), *r2+
       c    *r1, *r2+

       mpy  *r1+, r2
       div  @s, r2

       seto @s
       clr  r1
       swpb *r1+
       inv  @2(r1)
       abs  *r1

       jne  $
       b    r1
       bl   @2(r1)
       blwp *r1+
       rtwp

       tb   1
       sbz  0
       ldcr r1, 8
       ldcr @2(r1), 0
       stcr r2, 8
       stcr @s, 0
       stcr *r2+, 15

       andi r1, 0
       ci   r1, 0
       li   r1, 0

       sla  r1, 3
       src  r1, 0

* part 2

       lwpi >2000
       xorg >8300
y      data 0

       limi 0

       mov  r1, r2
       movb @y, *r1
       a    @y, @2(r2)
       ab   *r1+, @y
       szcb @2(r1), *r2+
       c    *r1, *r2+

       mpy  *r1+, r2
       div  @y, r2

       seto @y
       clr  r1
       swpb *r1+
       inv  @2(r1)
       abs  *r1

       jne  $
       b    r1
       bl   @2(r1)
       blwp *r1+
       rtwp

       tb   1
       sbz  0
       ldcr r1, 8
       ldcr @2(r1), 0
       stcr r2, 8
       stcr @y, 0
       stcr *r2+, 15

       andi r1, 0
       ci   r1, 0
       li   r1, 0

       sla  r1, 3
       src  r1, 0

       aorg
       end
