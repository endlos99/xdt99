* Banks and autos

       bank 0, >a000

       mov  w#99, @>8300
       c    @>8302, w#96

       bank 1

       mov  w#97, @>8300
       c    @>8302, w#69
       auto

       bank all
       auto

       end

