    ref vmbw

    .defm fill
    li   r0, 768
    li   r1, #2
    li   r2, #1 * 32
    s    r2, r0
    bl   @vmbw
    .endm

    .fill 10, '* '

    end
