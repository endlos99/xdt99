* arith expression with non-standard precedence

       rorg >1000

v1     equ  1
v2     equ  2

       clr  r0
       ci   r1, 1 + (2 * 3) * 4         ;WARN
       mov  r2, @>2000 + 2 * v1         ;WARN
       sla  r1, (2 + 3) * 4 + 5
       tb   v1 + (v2 + 9) * (v1 - 1)    ;WARN
       limi (2 * 2) + (3 + 3) * (4 + 4) ;WARN

       li   r0, -1 * 32
       li   r0, (1 + 1) + (1 + 2) * 3   ;WARN
       li   r0, -(-1 + 1) * 3
       li   r0, 1 * -32
       li   r0, +-+1 * +-+2
       li   r0, -1 + -1 * -2            ;WARN
       li   r0, -(-(-1 * -(1+2))*2)*-2
       end
