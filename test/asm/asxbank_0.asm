       ref  vdpwa, vdpwd

       aorg >6024

       li   r0, >4150
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       li   r0, '1 '
       movb r0, @vdpwd

       b    @>6028
