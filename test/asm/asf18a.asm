* F18A instructions

    jmp  b2
b1  push *r1
    pop  @b1(r2)
    slc  r9, 4
    ret

b2  call @b1
    end

