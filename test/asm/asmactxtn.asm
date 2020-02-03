    li   r0, 768
    li   r1, '* '
    li   r2, 10 * 32
    s    r2, r0
    bl   @vmbw

    copy "vmbw.a99"

    end
