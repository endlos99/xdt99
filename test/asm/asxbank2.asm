* SAVING BANKS

       SAVE >C000,>C020
       SAVE >D000,>D020
       SAVE >E000,>E020

       DATA >AFFE      ; IGNORED

       BANK 0, >C000
       DATA >C000
       DATA >C0FF

       BANK 1
       DATA >C100
       DATA >C1FF

       BANK ALL
       DATA >CF00
       DATA >CFFF

       BANK 1, >C018
       DATA >C118
       DATA >C1EE

       BANK 0
       AORG
       DATA >C018
       DATA >C0EE

       BANK 0, >D008
       DATA >D008
       DATA >D0FF

       BANK 1, >E018
       DATA >E108
       DATA >E1FF

       END
