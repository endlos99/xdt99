* VDP write byte text: write hex value of r1 (MSB) to r0

       def  vwbt
       ref  vdpwa, vdpwd

       even

vwbt:
       ori  r0, >4000
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa

       li   r0, 2             ; number of nybbles to show
       srl  r1, 4             ; move top nybble in -X-- position
!next:
       mov  r1, r2            ; copy for printing
       andi r2, >0f00
       ai   r2, '0 '
       ci   r2, '9 '
       jle  !
       ai   r2, '@ ' - '9 '
!      movb r2, @vdpwd

       sla  r1, 4             ; next nybble
       dec  r0
       jne  -!next

       rt
