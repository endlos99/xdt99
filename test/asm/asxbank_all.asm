* TAGGING CROSS-BANK ACCESS
* no relation with asxbank1/2

       idt  'ASXBANK'

       ref  vdpwa, vdpwd

       aorg >6000

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
