*  TEST DIRECTIVES

        IDT 'ASDIRS'

        DEF L1,L2
        DEF B1,D1,S1,T1,V1,Z1
        DEF SFIRST,SLOAD,SLAST
        DEF E1,ZX,ZZ

        REF Q1,Q2,Q0
        REF Q1                * IGNORED

* LABELS

SFIRST
SLOAD
L1      NOP
        NOP                   * COMMENT
L2
L3      JMP L2

L4      UNL                   * COMMENT
L5      PAGE                  * COMMENT
L6      TITL 'XDTTEST'
L7      LIST                  * COMMENT

        EVEN
L8
L9      BYTE 1
L10
L11     BYTE 2,3
L12
L13     DATA 4
        BYTE 5
L14
L15     EVEN
L16

LX      DATA L1,L2,L3,L4,L5
        DATA L6,L7,L8,L9,L10
        DATA L11,L12,L13,L14,L15
        DATA L16,LX
        
* EQU

E1      EQU >10
E2      EQU 10
E3      EQU '1'
E4      EQU '10'
E5      EQU ''''
E6      EQU L1
E7      EQU E1

EX      DATA E1,E2,E3,E4,E5
        DATA E6,E7,EX

* DATA

D1      DATA 10
        DATA 20
D2      DATA >10,>20,>30
D3      DATA E1,E2
D4      DATA 'AB','A'
D5      DATA -'AB',-'A'
D6      DATA '','''',''''''
D7      DATA -'',-'''',-''''''
D8      DATA D8
D9      DATA -10,->10

DX      DATA D1,D2,D3,D4,D5
        DATA D6,D7,D8,D9,DX
        
* BYTE

B1      BYTE 10,20
B2      BYTE >10
B3      BYTE >20
B4      BYTE >30
B5      BYTE 'A','B'
B6      BYTE -'A',-'B'
B7      BYTE '','''',-''''
B8      BYTE -2,->02

BX      DATA B1,B2,B3,B4,B5
        DATA B6,B7,B8,BX
        
* TEXT

T1      TEXT '1234'
T2      TEXT 'A'
T3      TEXT 'BC'
T4      TEXT 'D'
T5      TEXT -'9'
T6      TEXT -'999'
T7      TEXT ''               * >00 BYTE
T8      TEXT -''
T9      TEXT 'Aa !_|""''\n\\'
T10     TEXT 'A+1-2+''*'' ''/-1*"~ '
T11     TEXT '1+-2-3--4,-5+6'
T12     TEXT ''''

TX      DATA T1,T2,T3,T4,T5
        DATA T6,T7,T8,T9,T10
        DATA T11,T12,TX

* BSS/BES

S1      BSS 10
S2      BSS >10
S3      BES 10
S4      BES >10
S5      BSS 1
S6      BSS 2
S7      BES 1
S8      BES 1

SX      DATA S1,S2,S3,S4,S5
        DATA S6,S7,S8,SX
        
* EVEN

V1      BYTE 1
V2      EVEN
V3      BYTE 2
V4      EVEN
V5      EVEN
V6      TEXT 'A'
V7      EVEN
V8      TEXT 'AA'
V9      EVEN
V10     BSS 1
V11     EVEN
V12     BES 1
V13     EVEN
V14     DATA 1
V15     EVEN
V16     BYTE >FF

VX      DATA V1,V2,V3,V4,V5
        DATA V6,V7,V8,V9,V10
        DATA V11,V12,V13,V14,V15
        DATA V16,VX

* XOPS

X1      XOP @X1,1
X2      DXOP NEWOP,2
X3      NEWOP @X2
XX      DATA X1,X2,X3,XX

* OUT OF SPEC

Y1      EQU 1,2,3
Y2      BSS 2,4,6
Y3      BES 4,6,8
Y4      EVEN 1,2
YX      DATA Y1,Y2,Y3,Y4,YX

* REF

        DATA Q1
        DATA Q2
        
* END

Z0      DATA Z1
SLAST
Z1      END T1
Z2      DATA >DEAD
Z3      DATA >C0DE
ZX      DATA Z1,Z2,Z3

ZZ      EQU Z1
