* cross-bank with shared section

       bank all, >a000

l_all
       data >aaaa
       b    @l_1
       b    @l_b

       bank 1
       data >1111
       b    @x#l_all           ;x
       b    @l_1
       b    @x#l_0 + 2         ;x

       bank 0
       data >0000
       b    @l_all
       b    @l_0
       b    @x#l_1(r1)         ;x

       bank all
l_b    data >bbbb
       data >cccc

       bank 0
l_0    data >f000

       bank 1
l_1    data >f111

       end
