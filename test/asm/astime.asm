* TIMING

START  LWPI >8300

       MOV  R1,R2
       MOV  *R1,@0
       MOV  @0,*R1+
       MOVB @0,*R1+

       A    @0,@2
       SB   @0(R1),@2(R2)
       ANDI R1,0
       XOR  @0,R1

       BLWP *R1+
       BLWP @0
