from tkinter import *
from functools import partial
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from HoverObject import CreateToolTip
from QChemView import letmesee_poscar,letmesee_res,view_xyz,view_xyz2
def str_ab(s):
    try:
        t=s.split("-")
        return [int(t[0]),int(t[1])]
    except:
        return



#JUPYTER COORDINATES
# def coordinate_calcul(x,y,minx,maxx,miny,maxy):
#     new_xy=[]
#     new_xy.append(167+(((x-minx)/(maxx-minx))*1059))
#     new_xy.append(681-(((y-miny)/(maxy-miny))*580))
#     return(new_xy)
# def reverse_coordinate_calcul(x,y,minx,maxx,miny,maxy):
#     new_xy=[]
#     new_xy.append(((x-167)/1059)*(maxx-minx)+minx)
#     new_xy.append(((681-y)/580)*(maxy-miny)+miny)
#     return(new_xy)
def coordinate_calcul(x,y,minx,maxx,miny,maxy):
    new_xy=[]
    new_xy.append(167+(((x-minx)/(maxx-minx))*1059))
    new_xy.append(669-(((y-miny)/(maxy-miny))*580))
    return(new_xy)
def reverse_coordinate_calcul(x,y,minx,maxx,miny,maxy):
    new_xy=[]
    new_xy.append(((x-167)/1059)*(maxx-minx)+minx)
    new_xy.append(((669-y)/580)*(maxy-miny)+miny)
    return(new_xy)
def new_xlim_ylim(x,y,minx,maxx,miny,maxy):
    a,b=reverse_coordinate_calcul(x,y,minx,maxx,miny,maxy)
    xx=(maxx-minx)*0.1
    yy=(maxy-miny)*0.1
    return [a-xx,a+xx,b-yy,b+yy]
def sortir(w):
    w.destroy() 
def srt(event,win):
    sortir(win)
#win.bind('<Motion>', motion)
def raise_frame(frame):
    frame.tkraise()
def motion(a1,a2,b1,b2,event,win,frame,ph,nrj,xy,l_poscar,phx):
    x, y = event.x, event.y
    print(x,y)
    bornes=reverse_coordinate_calcul(x,y,a1,a2,b1,b2)
    if bornes[0]>a1 and bornes[0]<a2 and bornes[1]>b1 and bornes[1]<b2:
        win.bind('<Button-1>',nothing)
        xa1,xa2,xb1,xb2=new_xlim_ylim(x,y,a1,a2,b1,b2)
        print(xa1,xa2,xb1,xb2)
        fig1,ax1=plt.rcParams['figure.figsize'] = [15, 15] #reglage pour que la figure occupe toute la fenetre
        fig1,ax1=plt.subplots() #creation de la figure vierge
        ax1.set_xlim([xa1,xa2]) #l'axe des abscices de la figure
        ax1.set_ylim([xb1,xb2])
        ax1.set_xlabel('generation number') #l'axe des ordonnées
        ax1.set_ylabel('energy[eV/Atom]')
        fig1.suptitle('classification des différentes structures par énergie et génération [pour quitter click souris ensuite click <enter>]')
        frame1=Frame(win,width=1500,height=700)
        frame1.place(relheight=1.0, relwidth=1.0) 
        #frame1.pack(side="top")
        canvax=FigureCanvasTkAgg(fig1,master=frame1) #creation du canva qui permet d'impregner la figure sur tkinter
        canvax.get_tk_widget().pack(side="top",fill='both',expand=True)
        x2=0
        button_list2=[]
        new_xyx=[]
        # if len(xy)<=10:
        #     r=len(begining_index)
        # else:
        #     r=10
        # for i in range(a,b+1):
        #     new_xyx.append(coordinate_calcul(xy[i][0],xy[i][1],a,b,np.min(nrj),np.max(nrj)))
        for i in range(0,len(xy)):
            new_xyx.append(coordinate_calcul(xy[i][0],xy[i][1],xa1,xa2,xb1,xb2))
        xxa1,xxb1=coordinate_calcul(xa1,xb1,xa1,xa2,xb1,xb2)
        xxa2,xxb2=coordinate_calcul(xa2,xb2,xa1,xa2,xb1,xb2)
        print(xxa1,xxa2,xxb1,xxb2)
        for i in range(len(new_xyx)):
             if new_xyx[i][0]>xxa1 and new_xyx[i][0]<xxa2 and new_xyx[i][1]>xxb2 and new_xyx[i][1]<xxb1:
             #if 1:
                button_list2.append(Button(frame1,image=phx,height=10,width=10,borderwidth=0)) #creation d'un bouton qui permet de visualiser une structure
                button_list2[x2]['command']=partial(letmesee_poscar,i+a1,l_poscar) #fonction de visualisation
                button_list2[x2].place(x=new_xyx[i][0],y=new_xyx[i][1]) #coordonnées du bouton
                CreateToolTip(button_list2[x2],12,text="l'énergie:"+str(nrj[i+a1]))
                # print(real_nrj[i+a][1])
                x2+=1
        b2x=Button(frame1,text='back',command=lambda:raise_frame(frame))
        b2x.place(x=650,y=50)
        frame['cursor']='arrow'
        raise_frame(frame1)  
    else:
        return
def zoom(frame,win,a1,a2,b1,b2,ph,nrj,xy,l_poscar,phx):
    frame['cursor']='target'
    if 1:
        win.bind('<Button-1>',lambda event: motion(a1,a2,b1,b2,event,win,frame,ph,nrj,xy,l_poscar,phx))
def normal_cursor(frame,win):
    frame['cursor']='arrow'
    win.bind('<Button-1>',nothing)
def normal_cursor_event(event,frame,win):
    normal_cursor(frame,win)
def nothing(event):
    print('xxx')
    return
def sortir(w):
    w.destroy() 
def generate_plot_generation(xy,nrj,begining_index,l_poscar,value_inside):
    img=Image.open('here.gif')
    ph=ImageTk.PhotoImage(img)
    imgx=Image.open('here2.gif')
    phx=ImageTk.PhotoImage(imgx)
    interval=value_inside.get()
    #ab=str_ab(interval[2:len(interval)-3])
    ab=str_ab(interval)
    try:
        a=ab[0]
        b=ab[1]+1
    except:
        return
    new_xyx=[]
    if len(xy)<=10:
        r=len(begining_index)
    else:
        r=10
     # for i in range(a,b+1):
     #     new_xyx.append(coordinate_calcul(xy[i][0],xy[i][1],a,b,np.min(nrj),np.max(nrj)))
    for i in range(0,len(xy)):
        new_xyx.append(coordinate_calcul(xy[i][0],xy[i][1],0,r,np.min(nrj),np.max(nrj)))
    win=Toplevel()
    win.title("Rounded Button") 
    fig,ax=plt.rcParams['figure.figsize'] = [15, 15] #reglage pour que la figure occupe toute la fenetre
    fig,ax=plt.subplots() #creation de la figure vierge
    ax.set_xlim([a, b]) #l'axe des abscices de la figure
    ax.set_ylim([np.min(nrj),np.max(nrj)])
    ax.set_xlabel('generation number') #l'axe des ordonnées
    ax.set_ylabel('energy[eV/Atom]')
    fig.suptitle('classification des différentes structures par énergie et génération [pour quitter click souris ensuite click <enter>]')
    win.geometry("1500x900") #la taille de la fenetre
    win.attributes('-fullscreen', True)
    win.bind('<Button-3>',lambda event:normal_cursor_event(event,frame,win))
    win.bind('<Return>',lambda event:srt(event,win))
    frame=Frame(win,width=1500,height=700)
    frame.place(relheight=1.0, relwidth=1.0)
    canva=FigureCanvasTkAgg(fig,master=frame) #creation du canva qui permet d'impregner la figure sur tkinter
    canva.get_tk_widget().pack(side="top",fill='both',expand=True)
    button_list=[]
    x=0
    for i in range(len(new_xyx)):
        button_list.append(Button(frame,image=ph,height=5,width=5,borderwidth=0)) #creation d'un bouton qui permet de visualiser une structure
        button_list[x]['command']=partial(letmesee_poscar,i+a,l_poscar) #fonction de visualisation
        button_list[x].place(x=new_xyx[i][0],y=new_xyx[i][1]) #coordonnées du bouton
        CreateToolTip(button_list[x],12,text="l'énergie:"+str(nrj[i+a]))
        x+=1
    b1xx=Button(frame,text='zoom',command=lambda:zoom(frame,win,a,b,np.min(nrj),np.max(nrj),ph,nrj,xy,l_poscar,phx))
    b1xx.place(x=650,y=50)
    win.update()
    win.mainloop()
def generate_plot_index(xy,nrj,l_res,value_inside):
    img=Image.open('herex.gif')
    ph=ImageTk.PhotoImage(img)
    interval=value_inside.get()
    ab=str_ab(interval[2:len(interval)-3])
    try:
        a=ab[0]
        b=ab[1]
    except:
        return
    win=Toplevel()
    win.title("Rounded Button")
    fig,ax=plt.rcParams['figure.figsize'] = [15, 15]
    plt.rcParams['font.weight'] =1000          
    #reglage pour que la figure occupe toute la fenetre
    fig,ax=plt.subplots() #creation de la figure vierge
    ax.set_xlim([a, b]) #l'axe des abscices de la figure
    ax.set_ylim([np.min(nrj),np.max(nrj)])
    ax.set_xlabel('index') #l'axe des ordonnées
    ax.set_ylabel('energy[eV/Atom]')
    fig.suptitle('classification des différentes structures par energie et index [pour quitter click souris ensuite click <enter>]')
    win.geometry("1500x900") #la taille de la fenetre
    win.attributes('-fullscreen', True)
    win.bind('<Button-3>',lambda event:normal_cursor_event(event,frame,win))
    win.bind('<Return>',lambda event:srt(event,win))
    frame=Frame(win,width=1500,height=700)
    frame.place(relheight=1.0, relwidth=1.0)
    canva=FigureCanvasTkAgg(fig,master=frame) #creation du canva qui permet d'impregner la figure sur tkinter
    canva.get_tk_widget().pack(side="top",fill='both',expand=True)
    button_list=[]
    x=0
    real_nrj=[]
    nrj2=nrj.copy()
    index=0
    for axx in nrj2:
        real_nrj.append([axx,index+1])
        index+=1
    real_nrj.sort()
    nrj2.sort()
    new_xyx=[]
    xyx=[]
    for i in range(len(xy)):
        xyx.append([xy[i][0],nrj2[i]])
    for i in range(a,b+1):
        new_xyx.append(coordinate_calcul(xyx[i][0],xyx[i][1],a,b,np.min(nrj),np.max(nrj)))
    for i in range(len(new_xyx)):
        button_list.append(Button(frame,image=ph,height=5,width=5,borderwidth=0)) #creation d'un bouton qui permet de visualiser une structure
        button_list[x]['command']=partial(letmesee_res,i+a,l_res) #fonction de visualisation
        button_list[x].place(x=new_xyx[i][0],y=new_xyx[i][1]) #coordonnées du bouton
        CreateToolTip(button_list[x],12,text="l'énergie:"+str(nrj2[i+a])+"\n"+"l'index:"+str(real_nrj[i+a][1]))
        x+=1
    win.update()
    win.mainloop()
def generate_plot_xyz(xy,nrj,datalist,file_list,path,value_inside):
    os.chdir("C:\\Users\\br\\Desktop")
    img=Image.open('herex.gif')
    ph=ImageTk.PhotoImage(img)
    interval=value_inside.get()
    try:
        try:
            a,b=str_ab(interval[2:len(interval)-3])         
        except:
            a,b=str_ab(interval)
    except:
        return
    win=Toplevel()
    win.title("Rounded Button")
    fig,ax=plt.rcParams['figure.figsize'] = [15, 15]
    plt.rcParams['font.weight'] =1000          
    #reglage pour que la figure occupe toute la fenetre
    fig,ax=plt.subplots() #creation de la figure vierge
    ax.set_xlim([a, b]) #l'axe des abscices de la figure
    ax.set_ylim([np.min(nrj),np.max(nrj)])
    ax.set_xlabel('index') #l'axe des ordonnées
    ax.set_ylabel('energy[eV/Atom]')
    fig.suptitle('classification des différentes structures par energie et index [pour quitter click souris ensuite click <enter>]')
    win.geometry("1500x900") #la taille de la fenetre
    win.attributes('-fullscreen', True)
    win.bind('<Button-3>',lambda event:normal_cursor_event(event,frame,win))
    win.bind('<Return>',lambda event:srt(event,win)) 
    frame=Frame(win,width=1500,height=700)
    frame.place(relheight=1.0, relwidth=1.0)
    canva=FigureCanvasTkAgg(fig,master=frame) #creation du canva qui permet d'impregner la figure sur tkinter
    canva.get_tk_widget().pack(side="top",fill='both',expand=True)
    button_list=[]
    x=0
    real_nrj=[]
    nrj2=nrj.copy()
    index=0
    for axx in nrj2:
        real_nrj.append([axx,file_list[index]])
        index+=1
    real_nrj.sort()
    nrj2.sort()
    new_xyx=[]
    xyx=[]
    for i in range(len(xy)):
        xyx.append([xy[i][0],nrj2[i]])
    for i in range(a,b+1):
        new_xyx.append(coordinate_calcul(xyx[i][0]-1,xyx[i][1],a,b,np.min(nrj),np.max(nrj)))
    os.chdir(path)
    for i in range(len(new_xyx)):
        button_list.append(Button(frame,image=ph,height=5,width=5,borderwidth=0)) #creation d'un bouton qui permet de visualiser une structure
        button_list[x]['command']=partial(view_xyz,real_nrj[i+a][1]) #fonction de visualisation
        button_list[x].place(x=new_xyx[i][0],y=new_xyx[i][1]) #coordonnées du bouton
        CreateToolTip(button_list[x],12,text="l'énergie:"+str(nrj2[i+a])+"\n"+"nom fichier:"+str(real_nrj[i+a][1])+"\n"+"le groupe espace:"+datalist[i+a][2])
        x+=1
    win.update()
    win.mainloop()