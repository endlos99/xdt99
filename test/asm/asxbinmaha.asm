* max/min binary

       save >2000,

       aorg >2004
       data 1, 2, 3
       bss  5
       byte 1, 2, 3, 4
       text 'HELLO!'
       data -1

       aorg >2010
       data -1, -2, -3

       aorg >2008
       data >affe

       end
