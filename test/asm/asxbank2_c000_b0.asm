* SAVING BANKS

*      SAVE >C000,>C020

       AORG >C000
       DATA >C000  ; bank 0
       DATA >C0FF
       DATA >CF00  ; bank all
       DATA >CFFF
       BSS  >10

*      AORG >C018
       DATA >C018
       DATA >C0EE

       END
