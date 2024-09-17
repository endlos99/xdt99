*  Hello World

       idt 'ashello'

       def sload, sfirst, slast, start

       jmp  start

workspace:
       equ  >8300
keymode:
       equ  >8374
keycode:
       equ  >8375
gpl_status:
       equ  >837c

t_message:
       text 'HELLO WORLD'
       text '   hit any key!'

start:
       limi 0
       lwpi workspace

       ; clear screen
       clr  r0
       li   r1, '* '
       li   r2, 24 * 32
!      bl   @vsbw
       inc  r0
       dec  r2
       jne  -!

       ; write welcome message
       li   r0, 2 * 32 + 3
       li   r1, t_message
       li   r2, s#t_message
       bl   @vmbw

       ; check key presses
       li   r8, >ff00
       clr  r9
next:
       limi 2
       nop
       limi 0
       movb r9, @gpl_status

!      movb r9, @keymode
       blwp @kscan
       cb   @keycode, r8
       jeq  -!

       movb @keycode, r0
       srl  r0, 8
       andi r0, >000f
       ori  r0, >0700
       bl   @vwtr

       jmp  next

       copy "vsbw.asm"
       copy "vmbw.asm"
       copy "vwtr.asm"
       copy "kscan_ea.asm"

       end
