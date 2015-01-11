*  TEST XDT EXTENSIONS

	DEF DATA1		* comment

* lower case support

LABEL1	EQU 1			* comment
LABEL2	EQU 2

	CLR R0

DATA1	DATA LABEL1,LABEL2
TEXT1	TEXT 'Hello World!'

	END
