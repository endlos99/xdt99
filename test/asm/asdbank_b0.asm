* BANK directive

*      save >6000,>6020
       aorg >6002

*      data 0             ; no padding 

*      bank all

       data >1111
       data >2222
       data >3333

*      bank 0

       data >aaaa
       data >aaab
       data >aaac

*      bank 0
    
       data >aaad

*      bank all

       data >4444
       data >5555

       end

