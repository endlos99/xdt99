* JUMPSTART DISK

       idt  'ASJSDISK'

ws:
       equ  >8300
ws_r0lb:
       equ  ws + 1

       aorg >c000

       copy "../../lib/vsbw.a99"
       copy "../../lib/vmbw.a99"

start:
       limi 0
       lwpi ws

       clr  r0
       li   r1, '  '
       li   r2, 768
!      bl   @vsbw
       inc  r0
       dec  r2
       jne  -!

       clr  r0
       li   r1, '> '
       bl   @vsbw

       bl   @segment1
       bl   @segment2
       bl   @segment3
       bl   @segment4
       bl   @segment5
       bl   @segment6
       bl   @segment7

       inc  r0
       li   r1, '< '
       bl   @vsbw

       limi 2
       jmp  $

       ; check if r4 == r5 and write result to vdp *r0
compare:
       inc  r0
       c    r4, r5
       jeq  !
       li   r1, 'X '
       b    @vsbw
!      li   r1, 'O '
       b    @vsbw

       aorg >b000
segment1:
       mov  r11, r9
       li   r4, segment1
       li   r5, >b000
       bl   @compare
       b    *r9

       aorg >2000
segment2:
       mov  r11, r9
       li   r4, segment2
       li   r5, >2000
       bl   @compare
       b    *r9

       aorg >fa00
segment3:
       mov  r11, r9
       li   r4, segment3
       li   r5, >fa00
       bl   @compare
       b    *r9

       aorg >a000
segment4:
       mov  r11, r9
       li   r4, segment4
       li   r5, >a000
       bl   @compare
       b    *r9

       aorg >a800
segment5:
       mov  r11, r9
       li   r4, segment5
       li   r5, >a800
       bl   @compare
       b    *r9

       aorg >d000
segment6:
       mov  r11, r9
       li   r4, segment6
       li   r5, >d000
       bl   @compare
       b    *r9

       aorg >3100
segment7:
       mov  r11, r9
       li   r4, segment7
       li   r5, >3100
       bl   @compare
       b    *r9

       end  start
