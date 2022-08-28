* register alias

       aorg >f000

va     equ  7
vr     requ 15
vb     equ  0

       clr  vr
       li   VR, va + vb
       clr  va                ; valid for compatibility
       inc  @va(vr)

       .ifdef err

       clr  vr + 1            ;ERROR
       clr  va + 1            ;ERROR

       li   vr, vr            ;WARN
       li   va, va            ;OK!
       ai   va, vr + 2        ;WARN

vrr    requ 99                ;ERROR
vr     equ  2                 ;ERROR:  cannot redefine
va     requ 3                 ;ERROR:  cannot redefine
vr     data 1                 ;ERROR:  cannot redefine

       .endif

       .ifdef bin

       li   1, 2 * vr + vr

       .endif

       end
