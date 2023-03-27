; executable cart image

       idt  'ascarthd'

       ref  vdpwa, vdpwd

wrksp  equ  >8300              ; workspace memory in fast ram
r0lb   equ  wrksp + 1          ; register zero low byte address

       aorg >6000

       data >aa01
       data 0
       data 0
       data menu
       data 0
       data 0
       data 0
       data 0

menu   data 0
       data main
       stri 'HELLO'

msg1   text 'HELLO CART'

main   limi 0                  ; disable interrupts
       lwpi wrksp              ; load the workspace pointer to fast ram

;                                write the text message to the screen
       li   r0, 395            ; screen location to display message
       li   r1, msg1           ; memory location of source data
       li   r2, s#msg1         ; length of data to write

       movb @r0lb, @vdpwa      ; send low byte of vdp ram write address
       ori  r0, >4000          ; set read/write bits 14 and 15 to write (01)
       movb r0, @vdpwa         ; send high byte of vdp ram write address

disp   movb *r1+, @vdpwd       ; write a byte of the message to the vdp
       dec  r2                 ; byte counter
       jne  disp               ; check if done

       limi 2                  ; enable interrupts
       jmp  $                  ; infinite loop

       end  main
