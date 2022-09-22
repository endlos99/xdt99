* cont labels

foo:
bar    clr 0                  ;ERROR

baz
quux:  clr 1
       clr 2

       .ifeq baz, quux
       .error                 ;ERROR
       .endif

       end
