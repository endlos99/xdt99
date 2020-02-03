*  TEST BSS/BES DIRECTIVE

        IDT 'ASBSS'

        DEF A1,AX
        DEF D1,D10,DX
        DEF B1,B10,BX
        DEF T1,T10,TX
        DEF E1,E10,EX
        DEF Z1
        
* LABELS

SFIRST
SLOAD
L1      NOP

* BASICS

A1      DATA >FFF0
A2      BSS 1
A3      DATA >1111
A4
A5      DATA >2222
A6      BES 1
A7
A8      BSS 2
A9
A10     DATA >3333

AX      DATA A1,A2,A3,A4,A5
        DATA A6,A7,A8,A9,A10
        DATA AX

* BSS WITH DATA

        DATA >FFF1
D1      BSS 2
D2      DATA >1111
D3      BSS 2
D4      BSS 2
D5      DATA >2222
D6      BSS 1
D7      DATA >3333
D8      BSS 3
D9      DATA >4444
D10     BSS 1
D11     BSS 1
D12     BSS 1
D13     DATA >5555
D14     BSS 3
D15     BSS 1
D16     DATA >6666
D17     BSS 2
D18     BSS 1
D19     BSS 2
D20     DATA >7777
D21     BSS 3
D22     BSS 3
D23     DATA >8888

DX      DATA D1,D2,D3,D4,D5
        DATA D6,D7,D8,D9,D10
        DATA D11,D12,D13,D14,D15
        DATA D16,D17,D18,D19,D20
        DATA D21,D22,D23,DX
        
* BSS WITH BYTE

        DATA >FFF2
B1      BSS 1
B2      BYTE >11
B3      BYTE >22
B4      BSS 1

B5      BYTE >33
B6      BSS 3
B7      BYTE >44
B8      BSS 2
B9      BSS 1
B10     BYTE >55
B11     BYTE >66

B12     BSS 3
B13     BYTE >77
B14     BSS 1
B15     BSS 2
B16     BYTE >88
B17     BYTE >99
B18     BYTE >AA

B19     BYTE >BB
B20     BSS 2
B21     BYTE >CC
B22     BSS 1
B23     BYTE >DD
B24     BSS 2
B25     BYTE >EE
B26     BSS 1
        
BX      DATA B1,B2,B3,B4,B5
        DATA B6,B7,B8,B9,B10
        DATA B11,B12,B13,B14,B15
        DATA B16,B17,B18,B19,B20
        DATA B21,B22,B23,B24,B25
        DATA B26,BX

* BSS WITH TEXT

        DATA >FFF3
T1      TEXT '@'
T2      BSS 1
T3      TEXT '@@'
T4      BSS 1
T5      TEXT '@@@'
T6      BSS 1
T7      TEXT '@@'
T8      BSS 3
T9      TEXT '@@@'
T10     BSS 3
T11     TEXT '@'
T12     TEXT '@'

TX      DATA T1,T2,T3,T4,T5
        DATA T6,T7,T8,T9,T10
        DATA T11,T12,TX

* BES

        DATA >FFF4
E1      BES 1
E2      BES 1
E3      BES 3
E4      BES 1
E5      BYTE >11
E6      BES 1
E7      BYTE >22
E8      BES 4
E9      BYTE >33
E10     BES 1
E11     BES 1
E12     BES 1
E13     BYTE >44
        
E14     DATA >5555
E15     BES 1
E16     BSS 1
E17     BSS 3
E18     BES 1
E19     BYTE >66
E20     BES 1
E21     BSS 1
E22     BES 3

EX      DATA E1,E2,E3,E4,E5
        DATA E6,E7,E8,E9,E10
        DATA E11,E12,E13,E14,E15
        DATA E16,E17,E18,E19,E20
        DATA E21,E22,EX

* END

SLAST
Z1      END
