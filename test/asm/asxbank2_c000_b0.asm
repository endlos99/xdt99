* SAVING BANKS

*      SAVE >C000,>C020

*      AORG >C000
       DATA >C000
       DATA >C0FF
       DATA 0,0,0,0,0,0
*      AORG >C010
       DATA >CF00
       DATA >CFFF
       DATA 0,0
*      AORG >C018
       DATA >C018
       DATA >C0EE
*      DATA 0,0           * NO PADDING

       END
