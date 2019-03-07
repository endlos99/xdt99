* SAVING BANKS

       SAVE >B000,>B010
       SAVE >B020,>B030
       SAVE >B030,>B040
       SAVE >B080,>B090   ; EMPTY
       
L1     DATA >1111      ; TO BASE
       DATA >111F

       AORG >B008
L2     DATA >2222
       DATA >222F

       AORG >B023
L3     BYTE >33,>33
       BYTE >33,>3F

       AORG >B02E      ; SPILLED
L4     DATA >4444
       DATA >444F

       AORG >B038
L5     DATA >5555
       DATA >555F

       AORG >C000      ; NOT SAVED
L6     DATA >6666
       DATA >666F

       END
