 REM BASLAB1
 RANDOMIZE
 CALL CLEAR
LOOP:
 GOSUB SUBPROG
 IF A>10 THEN RESET
 A=A+1
 GOTO LOOP
RESET:
 A=A-5
 B=B+1
 GOTO @LOOP
SUBPROG:
 A=INT(RND*10)
 RETURN
