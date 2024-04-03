 mov r0,@2(r1
 mov @0(r1,r0
 mov r0,@2(r1))
 mov @(r1,@2)
 mov r0,@r2)
 mov @2(r1,r2)
 mov r1,r2(r3)
 mov @(r2),r0   ;WARN
 end
