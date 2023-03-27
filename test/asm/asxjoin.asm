* joined binary

       .ifdef saves

       save >4020,>4800
       save >5e00,>6000

       .endif

       bank all
       aorg >4040
       text 'COMMON'

       bank 0
       aorg >4060
       byte 1, 2, 3, 4, 5

       bank 1
       aorg >4090
       byte -1, -2, -3, -4, -5

       bank 0
       aorg >5000
       text 'INVALID'

       bank all
       aorg >5f00
       text 'FINI'

       end
