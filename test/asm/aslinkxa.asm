* linker and xorg

    def a1, x1
    ref b1, y1

    rorg 
a1  data x1
    data b1
    data a2

    xorg >2000
x1  data a1
x2  data x1

    rorg
a2  data x1
    data y1

    end
