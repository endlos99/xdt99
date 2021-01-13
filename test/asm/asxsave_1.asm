* SAVING BANKS

*      SAVE >B020,>B030
       
       AORG >B023
       DATA 0
       BYTE 0
L3     BYTE >33,>33
       BYTE >33,>3F
       BYTE 0
       DATA 0,0,0

*      AORG >B02E      ; SPILLED
L4     DATA >4444
*      DATA >444F

       END
