*  ERROR HANDLING (IMAGE): xdt99 extensions

       idt 'ASXERRSB'

* BANK SWITCHING

bank_main:
       data >0000
       data bank_main
       data bank_abs
       data bank_a1
       data bank_a2
       data bank_b1

       aorg >6000,1
bank_a1:
       data >6001
       data bank_main
       data bank_abs
       data bank_a1
       data bank_a2        ;ERROR
       data bank_b1

       aorg >6000,2
bank_a2:
       data >6002
       data bank_main
       data bank_abs
       data bank_a1        ;ERROR
       data bank_a2
       data bank_b1        ;ERROR

       aorg >6010,1
bank_b1:
       data >6011
       data bank_main
       data bank_abs
       data bank_a1
       data bank_a2        ;ERROR
       data bank_b1

       aorg >6000
bank_abs:
       data >6011
       data bank_main
       data bank_abs
       data bank_a1
       data bank_a2
       data bank_b1

       end
