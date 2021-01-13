* Banks and autos

       bank 0, >a000

       mov  w#99, @>8300
       movb b#99, @>8350
       a    w#>63, @>8304
       sb   b#'c', @>8380
       c    @>8300, w#69
       auto

       bank 1

       ab   b#'a', @>8380
       mov  w#97, @>8300
       a    w#>97, @>8304
       movb b#97, @>8350
       c    @>8302, w#69
       auto

       bank all
*      auto   ;ERROR

       end

