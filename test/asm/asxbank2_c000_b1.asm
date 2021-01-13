* SAVING BANKS

*      SAVE >C000,>C020

       AORG >C000
       DATA >C100   ; bank 1
       DATA >C1FF
       DATA >CF00   ; bank all
       DATA >CFFF
       BSS  >10

*      AORG >C018
       DATA >C118
       DATA >C1EE

       END
