       aorg >6000

ws:
       equ  >8300
ws_r0lb:
       equ  >8301
gplws:
       equ  >83e0

keymode:
       equ  >8374
keycode:
       equ  >8375
gplst:
       equ  >837c

fg99_restart:
       equ  >6020

input_buf:
       equ  >8320
next_find:
       equ  >833e
pager_pos:
       equ  >8340
text_lines:
       equ  >8342

* GPL header
       
       data >aa01
       data >0000
       data >0000             ; power-up list
       data menu              ; program list
       data >0000             ; DSR list
       data >0000             ; subprogram list
       data 0
       data 0

menu:
       data 0
       data help
       data 0

help:
       limi 0
       lwpi ws

       ; clear screen
       li   r0, 0
       li   r1, >3333
       li   r2, 960
       bl   @vsbmw

       ; define charset >20->7F
       li   r0, >a00
       li   r1, font_data
       li   r2, >158
       bl   @vmbw

       ; set text mode
       movb @cb_text, @>83d4
       li   r0, >01f0
       bl   @vwtr

       ; init
       clr  @input_buf
       clr  @pager_pos
       clr  @next_find

       ; reset SCAN
       li   r0, >9e7e
       mov  r0, @>8372
       li   r0, >05ff
       mov  r0, @keymode

       ; prepare text to show
       mov  @c_920, @text_lines  ; number of text lines shown at once
       li   r3, help_text     ; r3 = text at top of screen
       mov  r3, r4            ; r4 = end of text
zz:
       mov  *r4, r0
       jeq  eot               ; >0000 signals end of text
       ai   r4, 40
       jmp  zz

       ; no text found
no_text:
       li   r0, 440
       li   r1, t_nohelptext
       li   r2, 18
       bl   @vmbw
       clr  @next_find
       jmp  page_key

       ; end of text reached
eot:
       mov  @>0002(r4), r0        ; color after end of text
       bl   @vwtr

       c    r3, r4            ; text found?
       jeq  no_text

       ai   r4, >fe01
       c    r4, r3
       jhe  page
       ai   r4, 822
       s    r3, r4
       mov  r4, @text_lines   ; display less
       mov  r3, r4            ; stay at top

       ; show current text block
page:
       clr  r0                ; fill entire screen w/o footer
       mov  r3, r1
       mov  @text_lines, r2
       bl   @vmbw

       ; show navigation (restore after find)
       li   r0, 920
       li   r1, t_navigation
       li   r2, 40
       bl   @vmbw

       ; show scroll bar
       mov  @pager_pos, r0    ; delete old marker
       li   r1, >2020
       bl   @vsbw

       mov  r3, r0            ; offset position
       ai   r0, >2345

       mpy  @c_23, r0         ; percent in 1/23s
       mov  r4, r2
       ai   r2, >f938
       div  r2, r0

       inc  r0
       mpy  @c_40, r0
       dec  r1
       mov  r1, @pager_pos
       mov  r1, r0
       li   r1, >7e00
       bl   @vsbw

       ; reader navigation: E X < > SPACE B F Q
page_key:
       bl   @key              ; return key code in r0

       ; check key pressed
       ci   r0, >0520         ; FCTN-=
       jne  qq
       clr  @>83c4            ; no interrupt routine
       clr  @>837a            ; fix automotion sprites
       blwp @>0000
       ci   r0, >6120
       ai   r0, >e000
qq:
       ci   r0, >2020
       jeq  page_fwd
       ci   r0, >3000
       jeq  page_fwd
       ci   r0, >4200
       jeq  page_back
       ci   r0, >2300
       jeq  page_back
       ci   r0, >4500
       jeq  line_back
       ci   r0, >5500
       jeq  line_fwd
       jne  page_key
       b    @quit

       ; do navigation
page_fwd:
       ai   r3, 823
       jmp  new_pos

page_back:
       ai   r3, >f231
       jmp  new_pos

line_fwd:
       ai   r3, 40
       jmp  new_pos

line_back:
       ai   r3, >ff80

       ; make sure text remains in visible area
new_pos:
       ci   r3, help_text     ; before top?
       jhe  l1
       li   r3, help_text     ; reset to top
       jmp  page
l1:
       c    r3, r4            ; beyond bottom?
       jle  page
       mov  r4, r3
       jmp  page

       ; find text
find:
       li   r0, 920
       li   r1, t_find
       li   r2, 40
       bl   @vmbw

       li   r0, 929
       li   r1, input_buf
       li   r2, 28
       bl   @input

       li   r0, help_text_data
       mov  r0, @next_find

       ; search for next ocurrence
next:
       mov  @next_find, r5    ; restart after last ocurrence ...
       jeq  page_key          ; no previous find
       c    r5, r3

next_reset:
       li   r6, input_buf
       clr  r2                ; number of found characters
next_compare:
       movb *r5+, r0          ; check at text position
       jeq  wrap_around
       movb *r6+, r1          ; check at input buffer
       jeq  found
       c    r5, r8
       jeq  not_found         ; search wrapped around
       inc  r2
       jeq  next_compare
       s    r2, r5            ; reset to next search position
       inc  r5
       jmp  next_reset

       ; found search text
found:
       s    r2, r5            ; revert to beginning of found text
       mov  r5, @next_find    ; next search pos
       clr  r6
       mov  r5, r7
       div  @c_40, r6
       s    r7, r5            ; move to beginning of line
       mov  r5, r3
       jmp  new_pos

wrap_around:
       movb *r6, r1           ; found in last word?
       jeq  found
       jmp  next_reset              ; (-1 to avoid endless loop)

not_found:
       li   r0, 920           ; finally not found
       li   r1, t_notfound
       li   r2, 40
       bl   @vmbw
       b    @page_key

       ; prompt for input
input:
       mov  r11, r9
       mov  r0, r5            ; position
       mov  r1, r6            ; input buffer
       mov  r2, r7            ; save buffer length
input_char:
       mov  r5, r0
       li   r1, >7f00         ; print cursor
       bl   @vsbw
input_key:
       bl   @key
       ci   r0, >0820         ; FCTN-S
       jeq  input_del
       ci   r0, >0320         ; FCTN-1
       jeq  input_del
       ci   r0, >0320         ; FCTN-3
       jeq  input_clear
       ci   r0, >0d20         ; ENTER
       jeq  input_done
       mov  r2, r2            ; buffer full?
       jeq  input_key
       ci   r0, >4200
       mov  r0, r1
       mov  r5, r0
       bl   @vsbw
       inc  r5
       dec  r2
       jmp  input_char
input_del:
       c    r2, r7            ; buffer already empty?
       jeq  input_key
       dec  r6                ; delete last char in buffer
       mov  r5, r0            ; move cursor back
       bl   @vsbw
       dec  r5
       inc  r2
       jmp  input_char
input_clear:
       mov  r7, r0
       s    r2, r0            ; number of chars to clear
       s    r0, r5
       s    r0, r6
       mov  r5, r0
       li   r1, >2020
       mov  r7, r2
       bl   @vsbmw
       mov  r7, r2
       jmp  input_char
input_done:
       movb @cb_00, *r6        ; mark end of buffer
       b    *r9

       ; wait for new key
key:
       lwpi gplws
       clr  r0
       mov  r0, @gplst
       bl   @scan
       movb @gplst, r0
       coc  @c_newkey, r0     ; new key pressed?
       jne  key
       lwpi ws
       li   r0, >2020
       movb @keycode, r0
       rt

       ; return to FinalGROM 99 menu
quit:
       ; move return code to scratchpad RAM so that cart RAM can be overwritten
       li   r0, input_buf
xx:
       mov  *r1+, *r0+
       dect r2
       jne  xx

       ; restore graphics
       clr  r0                ; clear screen
       li   r2, 960
       bl   @vsbmw
       movb @cb_gfx1, @>83d4  ; graphics 1 mode
       li   r0, >01e0
       bl   @vwtr
       li   r0, >0717         ; black on cyan
       bl   @vwtr

       ; reload menu browser
       b    @send

       ; send for menu image
send:
       lwpi gplws             ; adjust to browser menu

       clr  @>6000            ; send one byte signal
       clr  @>7000
       clr  @>6000

       ; jump back to menu browner
       b    @>0060

       ; subroutines
vsbw:
       rt
vmbw:
       rt
vwtr:
       rt
vsbmw:
       rt
scan:
       rt

       ; constants
c_newkey:
       data >0020
c_23:
       data >0023
c_40:
       data >0040
c_920:
       data 920
cb_text:
       data >000f
cb_gfx1:
       data >00ee
cb_00:
       data >0000
t_navigation:
       data >0011
t_nohelptext:
       data >0022
t_find:
       ;text 'aaaaaa'
       data >0001
       data >0002
t_notfound:
       ;text 'bbbbbb'
       data >0003
       data >0004

       ; graphics
font_data:
       data >0000
       data >0001
       data >0028
       data >0028

       ; generated data
help_text:
       data >0028

help_text_data:
       equ  $

       end
       
