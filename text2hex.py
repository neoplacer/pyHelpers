# Text to Hex converter by Richard Gericke
# Decode any Text from Windows Clipboard to html %hex
# an copy it back to clipboard_append
print "Text to HTML Hex converter"
print "Version 1.0"
print "(C) Richard Gericke"
print ""
from Tkinter import Tk
r = Tk()
r.withdraw()
str = r.clipboard_get()
r.clipboard_clear()

c = str.encode('utf-8').encode('hex')
d = list(c)
a = u""
b = 1
for n in d:
	b+=1
	if b==2:
		a+=u"%"+n
		b=0
	else:
		a+=n 
print a
r.clipboard_append(a)
r.destroy()