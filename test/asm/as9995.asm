* 9995 instructions

a1 clr r0
   mpys @a1
   mpys r9
   divs @a1(r2)
   divs *r3+
   stst r0
   lst r0
   stwp r1
   lwp r1

   end
