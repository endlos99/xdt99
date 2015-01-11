*  TEST XDT EXTENSIONS

	def data1		* comment

* lower case support

label1	equ 1			* comment
label2	equ 2

	clr r0

data1	data label1,label2
text1	text 'Hello World!'

	end
