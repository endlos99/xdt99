       ref  vdpwa, vdpwd

       aorg >6024

       b    @>601c
*bank1:
       li   r0, >4158
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       li   r0, '2 '
       movb r0, @vdpwd

       limi 2
       jmp  $
