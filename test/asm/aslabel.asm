; valid labels

       aorg >2000

; legal symbols

$$$    data 1
[!@]   data 2
yes?   data 3
?no    data 4
$12    equ  5
_12    equ  6

       jmp  $$$
       data [!@]
       b    @[!@]
       mov  @yes?, @?no
       li   0, $12
       clr  @$12 + [!@]
       ai   _12, $12

a.b    data 0
a:b    data 0
a[]b   data 0


; unicode

ucl❤️   data 1
ucl💔  data 2
ucl❤️2  data 3
❧🥰☙   equ  4

       clr  @ucl❤️
       a    @ucl❤️2, @ucl💔 + ucl❤️
       data ucl❤️, ucl❤️2, ucl💔
       jmp  ucl💔
       li   1, ucl❤️2
       ai   ❧🥰☙, ucl💔^ucl❤️

       end
