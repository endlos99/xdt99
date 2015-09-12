*  TEST RELOCATABLE ADDRESSES

        IDT 'ASRELOC'

        DEF A1,A2,A3,A4,A5,A6,A7
        DEF SFIRST,SLAST,SLOAD

        AORG >A080
SFIRST
SLOAD
        DATA 1
A1      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 1

        AORG >A060
        DATA 2
A2      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 2

        AORG >A040
        DATA 3
A3      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 3

        RORG
        DATA 4
A4      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 4

        AORG >A0A0
        DATA 5
A5      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 5

        AORG >A0C0
        DATA 6
A6      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 6

        RORG
        DATA 7
A7      B   @A1
        B   @A2
        B   @A3
        B   @A4
        B   @A5
        B   @A6
        B   @A7
        DATA 7

        AORG >A0E0
SLAST   END
