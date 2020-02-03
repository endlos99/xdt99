* standard library example

    rorg

    def start
    ref vmbw, vsbr, vwbt

start:
    limi 0
    lwpi >8300

    li   r0, 74
    li   r1, text1
    li   r2, 10
    bl   @vmbw

    li   r0, >3fff
    bl   @vsbr

    li   r0, 86
    bl   @vwbt

    limi 2
    jmp  $

text1:
    text 'HIGH BYTE:'

    end

