* multiple output files

X      EQU  1
Y      EQU  2
Z      EQU  3

       AORG >2000
       BYTE X,X,X,X,X,X,X,X,X,X

       AORG >A000
       BYTE Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y

       AORG >E000
       BYTE Z,Z,Z,Z,Z,Z,Z,Z
       BYTE Z,Z,Z,Z,Z,Z,Z,Z
       BYTE Z,Z,Z,Z,Z,Z,Z,Z
       BYTE Z,Z,Z,Z,Z,Z,Z,Z

       END
