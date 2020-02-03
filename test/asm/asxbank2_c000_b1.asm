* SAVING BANKS

*      SAVE >C000,>C020

*      AORG >C000
       DATA >C100
       DATA >C1FF
       DATA 0,0,0,0,0,0

*      AORG >C010
       DATA >CF00
       DATA >CFFF
       DATA 0,0
*      AORG >C018
       DATA >C118
       DATA >C1EE
*      DATA 0,0           * NO PADDING

       END
