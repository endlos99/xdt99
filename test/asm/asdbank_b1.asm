* BANK directive

       save >6000,>6020
       aorg >6000
       
*      bank 1

       data >ffff

*      bank all

       data >1111
       data >2222
       data >3333

*      bank 1
  
       data >bbbb
       data >bbbc
       data 0

*      bank 1

       ; nothing here
       data 0

*      bank all

       data >4444
       data >5555

       end

