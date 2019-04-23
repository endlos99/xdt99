* warnings

n      equ 0
val    equ 2

       aorg >3000

       ; B/JMP
       b @l1        ;WARN
l1     nop
       b @l1        ;WARN

       ; missing R
       clr 0        ;WARN
       inc 4        ;WARN
       li r1, 0
       li 1, 0      ;WARN

       ; @0 vs. *R
       clr @0(r1)   ;WARN
       clr @1(r1)
       clr @n(r2)   ;WARN

       ; B/JMP
       b @l2
       b @l2        ;WARN
       bss 254      ; note that B has two words, but JMP only one!
l2     nop
       bss 252
       b @l2        ;WARN
       b @l2

       ; Rn as immediate value
       ci r1, 1
       ci r1, r1    ;WARN
       andi r1, r2  ;WARN
       sla r1, r2   ;WARN
       sla r1, val
       tb r2        ;WARN
       tb val

       ; for shifts, r0 is OK instead of 0
       sla r1, 0
       sla r2, r0
       sla r3, r1   ;WARN

       end
