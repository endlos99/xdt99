* TAGGING CROSS-BANK ACCESS
* no relation with asxbank1/2

       idt  'ASXBANK'

       ref  vdpwa, vdpwd

       bank all, >6000

       data >aa01
       data 0, 0
       data menu
       data 0, 0, 0, 0

menu:
       data 0
       data start
       byte 6
       text 'X-BANK'

start:
       limi 0
       lwpi >8300

       bank 0

       li   r0, >4150
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       li   r0, '1 '
       movb r0, @vdpwd

       b    @x#bank1

       bank 1

       b    @x#start
bank1:
       li   r0, >4158
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       li   r0, '2 '
       movb r0, @vdpwd

       limi 2
       jmp  $

