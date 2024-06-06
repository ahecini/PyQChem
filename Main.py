from tkinter import *
from functools import partial
import os
from QChemFile import browse,browse_xyz,back
if __name__=='__main__':
    w=Tk()
    w.geometry("300x200")
    b1=Button(w,text="import your file")
    b1.pack(padx=30,pady=30)
    b2=Button(w,text="USPEX File here",state='disabled')
    b2.place(x=90,y=90)
    b3=Button(w,text='❌',state='disabled')
    b3.place(x=200,y=90)
    b4=Button(w,text='select multiple files',command=browse_xyz)
    b4.place(x=95,y=150)
    path="C:\\Users\\br\\Desktop"
    os.chdir(path)
    b1['command']=partial(browse,b1,b2,b3,b4)
    b3['command']=partial(back,b1,b2,b3,b4)
    help_frame=Frame(w)
    help_label=Label(help_frame,text="what we see here")
    help_label.pack(side='top')
    # print(w.winfo_height(),w.winfo_width())
    w.mainloop()
    
