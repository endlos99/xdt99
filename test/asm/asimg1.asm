*  TEST IMAGE CREATION

        IDT 'ASIMG1'

        DEF SFIRST,SLAST,SLOAD

        TEXT 'PRE IMAGE DATA'

        RORG >0100
SFIRST
SLOAD   TEXT '**START IMAGE**'
        BSS 3
        BES 2
        BSS 1
        BES 5
        DATA SFIRST

        AORG >0200
L1      TEXT 'AORG SECTION'
        BSS 3
        BES 4
        DATA L1
        TEXT 'END AORG'

        RORG
L2      TEXT 'RORG RESUME'
        EVEN
        BSS 3
        DATA L2
        JMP $
        TEXT 'RORG RESUME END'

        RORG >0300
L3      TEXT 'RORG >0300 SECTION'
        DATA L3
        TEXT 'RORG >0300 END'

        TEXT '**END IMAGE**'
        EVEN
        BYTE >FF
        
SLAST   TEXT 'POST IMAGE DATA'
        END
