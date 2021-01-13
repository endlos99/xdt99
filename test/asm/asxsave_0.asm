* SAVING BANKS

*      SAVE >B000,>B010

       AORG >B000
*L1     DATA >1111      ; TO BASE
*       DATA >111F
*       DATA 0,0

*      AORG >B008
L2     DATA >2222
       DATA >222F
*      DATA 0,0        ; NO PADDING BEFORE AND AFTER

       END
