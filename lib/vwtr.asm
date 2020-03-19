* write VDP register

       def  vwtr
       ref  vdpwa

       even

vwtr:
       ori  r0, >8000
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa

       rt
