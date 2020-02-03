* linker and xorg

    def a1, x1, b1, y1

    rorg >e000
a1  data x1
    data b1
    data a2

    xorg >2000
x1  data a1
x2  data x1

    rorg
a2  data x1
    data y1

    aorg >e008
b1  data y1
    data a1
    data b2

    xorg >3000
y1  data b1
y2  data y1

    aorg
b2  data y1
    data x1

    end

