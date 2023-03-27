* references and built-ins

       ref  vdpwa
       ref  extzz

a:
       equ  >8300

s:
       mov  @a, @vdpwa
       dec  @extzz
       jne  s
       rt

       end
