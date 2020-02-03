*  TEST XDT EXTENSIONS

	def data1		* comment

sym1    equ 1

        aorg >a000
aa1     data >1111
aa2     data >2222
        rorg
ar1     data >3333
ar2     data >4444

* lower case support

label1	equ 1			* comment
label2	equ 2

	clr r0

data1	data label1,LABEL2
text1	text 'Hello World!'

* long labels

longlabel1 data longlabel2-longlabel1
longlabel2 mov @longlabel1,@longlabel2
_funky? data _funky?                       extended char set

* relaxed whitespace

  ; comments anywhere
ws1 ;comment
ws2 equ >1 + -2 * >3 + '4'  comment
ws3     equ     >1  + 2 ignored
 inc @data1  comment
        inc @data1 + 2;comment
        mov @data1 , @data1 + 2
        mov @data1 + 2 , @data1 ; comment
        clr @data1 (r6)
        inc @data1 + >2 (r4)
        mov  @text1 ( r7 ) , @ text1 (r9)  comment
        mov @>10 , @>20
        mov *r10+ , *r9  +
        mov *r0 , *r9+  comment
        mov  @2 + data1,@data1 + >2 - text1

ws4     byte 1, 2 , 3 ,4, 5  , 999    ; 999 is comment
        text '   ,'',   '  comment
        even  comment
        rtwp  comment
        rt  comment
        data ws1, ws2, ws3, ws4

*        data >DEAD,>DEAD
* advanced expressions

expr1   equ >1 + >2 * >3 % 4 - -5                   ; == 6
expr2   equ 30-((18-(15-(11-(7+-1))))*2)            ; == 14
expr3   equ (1+(4-3)*+-(10%3))-+(8)                 ; == -10
expr4   equ (((10)))                                ; == 10
expr5   equ ( - ( + ( ~ ( ( 1 ) ) ) ) * 13)% 10     ; == 6
expr6   equ -(-(~~(---(~(((-1))-2)-3)-4)-5)-6)-7    ; == -9
expr7   equ ('AZ')/(>10)-10*>2                      ; == >816
expr8   equ >100|>FF&>AAA^>FFF                      ; == >F55
expr9   equ ~(-2) | (~1-~~2-(~(-+~(+(1-~+3))) --1)*-~1) & ~~~ >A0 ; == 5
expr10  equ >aA+ >bB ->Ff                           ; == 102
expr11  equ - expr1 +~ expr2^~expr3 % ( expr4 - (expr5 ) )  ; == 2

        data >1 + >2 * >3 % 4 - -5 , (( ( 10 )) )  , 999
        byte ~0, ~>FF, -1
        data >10|~>FF&(>AAA^>FFF) , >a , ~0 , - 0    ; >510
        data (-+~EXPR2 +-~ Expr3) % expr1            ; 0

        clr @ expr1 - expr2 + 1 (r1)                 ; @-7(R1)
        inc @ expr1 & >000ffc                        ; @4
        dec @ >999 ^ expr2 + 2 ( 2 )                 ; @2457(R2)
        clr @~0                                      ; @>FFFF
        li 1 , ~ (>A | expr1 )^ >F + ( 3 )           ; 1

expr20  equ aa1 + (ar1 - ar2)
expr21  equ (aa1 + ar1) - ar2

        data expr1, expr2, expr3, expr4, expr5
        data expr6, expr7, expr8, expr9, expr10
        data expr11, expr20, expr21

        data aa1 + ar1 + ~ar2
        data (aa1-ar2)+(ar1-aa1)
        data >1000 | (aa1 & >FFF)
        data ~aa1

* unsupported due to ambiguity

*       clr @a+(x-y)(r1)
*    l1 equ 1 * comment

* conditional assembly

cond1   data >1111
        .ifdef sym1
        data >2001
        .else
        data >2002
        .endif
	.ifndef sym2
	data >2003
	.endif

	.ifdef sym3
cond2   data >3001
        .ifdef sym2
        data >300f
        .endif
        .else
        data >3002
        .ifdef sym2
        data >3101
        .else
        data >3102
        .endif
        data >3003
        .endif
        data >ffff

cond3   data >1111
        .ifeq sym2
        data >2222
        .endif
        .ifne sym2
        data >3333
        .endif
	.ifgt sym2
	data >4444
	.endif

        .ifeq sym1 + sym2 + sym3, 3
cond4   data >2222
        .endif
        .ifne sym2 * sym3, 4
        data >3333
        .endif
	.ifgt sym2, sym1
	data >4444
	.endif
	.ifge sym2, sym3
	data >5555
	.endif

        .ifndef _version_
cond5   data >fefe
        .endif

	end longlabel1
