* SAVE with null expression

  save ,e
  save s,

  aorg >2000
  data 9, 9, 9
e data -1,-1          ; not saved

  aorg >5ffe
  data -1
s data 1, 1, 1, 1

  aorg >6010
  data 2, 2, 2, 2

  end
