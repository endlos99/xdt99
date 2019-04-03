* l#Rn for @ws + 2*n + 1

      aorg >2000

      ab   l#r0, r15

      lwpi >8300
      movb l#r9, r0
      movb r0, l#r15
      cb   l#r0, l#r11
      socb l#1, l#2      ;WARN

      aorg >3000

      lwpi >8320
      movb l#r1, l#r5

      lwpi >83e0
      cb   l#r0, l#r1

      end

