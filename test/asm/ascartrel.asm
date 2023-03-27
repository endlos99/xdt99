* reloc cart with GPL header

       .ifdef SIXM
       rorg >6000
       .else
       rorg
       .endif

       data >aa01, 0, 0, m, 0, 0, 0, 0
m      data 0, s
       stri 'E'

s      jmp  $

       text '********************************'

       end  s
