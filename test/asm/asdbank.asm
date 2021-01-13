* BANK directive

       save >6000,>6020

       bank 1, >6000

       data >ffff

       bank all

       data >1111
       data >2222
       data >3333

       bank 0

       data >aaaa
       data >aaab
       data >aaac

       bank 1
  
       data >bbbb
       data >bbbc

       bank 0
    
       data >aaad

       bank 1

       ; nothing here

       bank all

       data >4444
       data >5555

       end
