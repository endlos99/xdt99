  def a1, a2, b1, b2, c1, c2

a1 equ >1001
a2 equ >1002
b1 equ >2001
b2 equ >2002
c1 equ >3001
c2 equ >3002

  rorg >10
  data 1
  data b1
  rorg >1c
  data 1
  data c1

  aorg >100
  data 2
  data a1
  aorg >10c
  data 2
  data c2

  rorg >30
  data 3
  data a2
  rorg >3c
  data 3
  data b2
  
  end
