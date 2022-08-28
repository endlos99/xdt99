* assembly target

       data >1111

       .ifdef _xas99_obj
       data >2222
       .endif

       .ifdef _xas99_bin
       data >3333
       .endif

       .ifeq _xas99_image, 1
       data >4444
       .endif

       data >ffff

       end
