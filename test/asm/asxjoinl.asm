* large joined binary

       bank all
       aorg >bff0

       data 1, 2, 3, 4, 5, 6, 7, 8

       bank 0
       data 9, 10, 11, 12, 13, 14, 15, 16

       bank 1
       bss 8
       byte -1

       end
