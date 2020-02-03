* linker and xorg

    ref a1, x1
    def b1, y1

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
