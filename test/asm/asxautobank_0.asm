* Banks and autos

       aorg >a000

       mov  @w_99, @>8300
       movb @b_99, @>8350
       a    @w_99, @>8304
       sb   @b_99, @>8380
       c    @>8300, @w_69

*      auto

b_99   byte 99
       byte 0
w_69   data 69
w_99   data 99
       end

