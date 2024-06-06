from tkinter import *
'''@source of the class and CreateToolTip function: squareRoot17(stackoverflow username)'''
class Hover:
    def __init__(self,b,size=8,text=None):
        self.widget=b
        self.size=size
        self.x=0
        self.y=0
        self.text=text
        self.win=None
    def appear(self):
        if self.win or not self.text:
            return
        x=y=0
        x=x+self.widget.winfo_rootx()+25
        y=y+self.widget.winfo_rooty()+25
        self.x=x
        self.y=y
        self.win=tw=Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", str(self.size), "normal")) #we create the label
        label.pack(ipadx=1)
    def disappear(self):
        tw=self.win
        self.win=None
        if tw:
            tw.destroy()
def CreateToolTip(b,size,text):
    hover=Hover(b,size,text)
    def pop(event):
        hover.appear()
    def dip(event):
        hover.disappear()
    b.bind('<Enter>',pop)
    b.bind('<Leave>',dip)
def CreateHover(b,size,text):
    hover=Hover(b,size,text) 
    hover.appear()
    def leave(event):
        hover.disappear() 
    b.bind('<Button>',leave)

    

        
        