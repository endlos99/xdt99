* HOW FAR CAN YOU GO?

       AORG >2000

       DEF START
START  JMP  L1      ; limit -> larger BSS -> error
       BSS  254     ; disp max. 2 * 127 = 254
L1     NOP
       BSS  252     ; disp min. 2 * -128 = -256  ------+
       JMP  L1      ; limit -> larger BSS -> error     |
                    ; <- base - 256 = L1  <------------+
       JMP  L2      ;ERROR
       BSS  256
L2     NOP

L3     NOP
       BSS  254
       JMP  L1      ;ERROR

       END
