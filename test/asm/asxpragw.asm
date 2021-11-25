* pragmas: warnings

symbol byte 1, 2, 3

start  clr 0            ; WARN

       clr 1            ;: warn-usage = off  ; turn usage warnings off
       mov 1, 2

       b   @start       ;: warn-opts = off, usage=on

loop   clr 9            ; WARN
       b   @loop

       seto 2           ; WARN  ;: warn-usage=on, warn-opts=on
                        ;: warnings= off

       end
