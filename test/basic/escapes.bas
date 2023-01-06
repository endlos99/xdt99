100 REM \x and \u char code escapes
110 PRINT "11\x9344":"77\d16788"
120 DATA \xcd\d200,"\d001\x00"
130 REM plain ASCII codes
140 INPUT "\x41\d066\x22?":A$
150 REM escaped codes
160 PRINT "xx\\x40\\d999\\xx","\\\\\\"
170 REM unrelated strings
180 DATA xxx\rxx\\xx\,\
190 END
