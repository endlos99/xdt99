*  TEST MISC OPCODES

        IDT 'ASOPCS'

        DEF SFIRST,SLOAD,SLAST

* LABELS

L1      JMP L2
L2      JMP L1

* ALIGNMENT

        BYTE 0
L3      JMP L3
        BYTE 0
        JMP $

* ADDRESS MODES

        MOVB 1,@2
        MOVB @3,4
        MOVB >A,@>B
        MOVB @1(2),@3(4)
        MOVB @>A(>2),@>B(>4)
        MOVB *1,*2+
        MOVB *0+,*3
        MOVB @L1(1),@L2(2)

        LI 0,-1
        LI >A,>B
        LI 0,L1

        SLA 0,1
        SLA 1,>2

* PSEUDO OPCODES

        BYTE 0
P1      NOP
P2      RT
        DATA 0
        NOP
        RT
        DATA P1,P2

* XOPS

        EVEN
        BYTE 0
X1      DXOP XXX,1
X2      XXX @X1
XX      DATA X1,X2,XX

* END

SLAST
Z       END
