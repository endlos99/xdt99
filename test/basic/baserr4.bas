 ! unknown label with @
 INPUT "START NUMBER? ":N
LOOP:
 IF N-INT(N/2)*2=0 THEN @EVEN
 N=3*N+1
OUT:
 PRINT N;
 GOTO @LOOP
EVEN:
 N=N/2
 GOTO @LOOX
DONE:
 END
