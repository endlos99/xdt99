  aorg >2000
  jmp start

  text 'OIOIOIOIOIOIOIOI'

start:
  mov r1, *r2
  inc @2(r2)
  xor r1, r2
  jeq part2
  jmp start

  data 1, 2, 3, 4, 5, 6, 7, 8

part2:
  clr r1
  dec @>8300
  jne part2
  bl  @start
  a   r3, r4
  
  end

  
