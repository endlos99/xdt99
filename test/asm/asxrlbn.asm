* l#Rn for @ws + 2*n + 1

      aorg >2000

      ab   @>83e0 + 1, r15

      lwpi >8300
      movb @>8300 + 19, r0
      movb r0, @>8300 + 31
      cb   @>8300 + 1, @>8300 + 23
      socb @>8300 + 3, @>8300 + 5

      aorg >3000

      lwpi >8320
      movb @>8320 + 3, @>8320 + 11

      lwpi >83e0
      cb   @>83e0 + 1, @>83e0 + 3

      end

