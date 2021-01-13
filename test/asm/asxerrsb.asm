*  ERROR HANDLING (IMAGE): xdt99 extensions

       idt 'ASXERRSB'

* BANK SWITCHING

       bank all, >6000
bank_all:
       data >0000
       data bank_all
       data bank_a1
       data bank_a2
       data bank_b1
       data bank_b2

       bank 1
bank_a1:
       data >1001
       data bank_all
       data bank_a1
       data bank_a2        ;ERROR
       data bank_b1
       data bank_b2        ;ERROR

       bank 2
bank_a2:
       data >1002
       data bank_all
       data bank_a1        ;ERROR
       data bank_a2
       data bank_b1        ;ERROR
       data bank_b2

       bank 1, >6020
bank_b1:
       data >2001
       data bank_all
       data bank_a1
       data bank_a2        ;ERROR
       data bank_b1
       data bank_b2        ;ERROR

       bank 2
bank_b2:
       data >6011
       data bank_all
       data bank_a1        ;ERROR
       data bank_a2
       data bank_b1        ;ERROR
       data bank_b2

       end
