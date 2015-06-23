# UUID GEN
import uuid
import string
import tkMessageBox
import os
from Tkinter import *
c=""

for x in range(0, 10):
	y= str(uuid.uuid1())
	print y.upper()
	c += y.upper() + os.linesep
	
#tkMessageBox.showinfo(title="Greetings", message=c)
root = Tk()
T = Text(root, height=80, width=40)
T.pack()
T.insert(END, c)
mainloop()