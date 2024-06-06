from tkinter import *
from tkinter import filedialog
from functools import partial
import os
import numpy as np
from ase.io import read
from ase.visualize import view
from ase.io.res import read_res
from pymatgen.io.vasp import Poscar
from QChemPlot import generate_plot_generation,generate_plot_index,generate_plot_xyz,coordinate_calcul
from HoverObject import CreateHover
from QChemView import view_xyz2

def find_ending(s,start=0):
    end='-------------------------- Local optimization finished -------------------------'.split()
    for i in range(start,len(s)):
        if s[i]==end[0] and s[i+1]==end[1] and s[i+2]==end[2]:
            return i
    else:
        return -1
def merge_coordinates(s):
    s1=s
    s2=''
    start=0
    i=0
    while i<=(len(s1)-1):
        if s1[i][0]=='[':
            start=i
            while s1[i][-1]!=']':
                s2=s2+s1[i]
                del(s1[i])  
            else:
                s2=s2+s1[i]
                del(s1[i])
                s1.insert(start,s2)
        i+=1
        s2=''
    return s1
def is_poscar(file):
    try:
        poscar = Poscar.from_file(file)
        return True
    except:
        return False
def is_res(file):
    try:
        res=read_res(file)
        return True
    except:
        return False
def is_cif(file):
    try:
        cif=read(file)
        return True
    except:
        return False
def browse_txt(s11):
    p=filedialog.askopenfile()
    path=str(p)
    s=path.split("'")
    s1=s[1]
    s1=list(s1)
    s12=''
    x="/"
    for a in s1:
        if a == x :
            s12=s12+'/'
        s12=s12+a
    s2=s[1].split('.')
    if len(s2)<2 or s2[1]!='txt':
        print("wrong file")
    else:
        f=open(s12)
        l_poscar=f.read().split()
        l_poscar=merge_coordinates(l_poscar)
        ending_index=[]
        begining_index=[]
        start=0
        while find_ending(l_poscar,start)!=-1:
            ending_index.append(find_ending(l_poscar,start))
            start=find_ending(l_poscar,start)+1
        start=1
        while "ID" in l_poscar[start:]:
            begining_index.append(l_poscar.index("ID",start))
            start=l_poscar.index("ID",start)+1
        g=[]
        for i in range(len(begining_index)):
            g.append([])
            for j in range(begining_index[i]+7,ending_index[i],7):
                g[i].append(float(l_poscar[j+3]))
        index_number=0
        for i in range(len(g)):
            index_number=index_number+len(g[i])
        xy=[]
        for i in range(len(g)):
            for j in range(len(g[i])):
                xy.append([i+1,g[i][j]])              
        file = s11
        f=open(file)
        l_poscar=f.read().split('EA')
        s1='EA'
        for i in range(len(l_poscar)):
            s1=s1+l_poscar[i]
            l_poscar[i]=s1
            s1='EA'
        del(l_poscar[0])

        nrj=[]
        for i in range(len(xy)):
            nrj.append(xy[i][1])
        # xy=[]
        # for i in range(len(l)):
        #     xy.append([i,nrj[i]])
        if len(xy)<=10:
            r=len(begining_index)
        else:
            r=10
        new_xy=[]
        for i in range(0,len(xy)):
            new_xy.append(coordinate_calcul(xy[i][0],xy[i][1],0,r,np.min(nrj),np.max(nrj)))
        path="C:\\Users\\br\\Desktop"
        os.chdir(path)
        fen=Tk()
        fen.title('liste des générations existantes')
        fen.geometry("300x300")
        options_list=list_index(len(begining_index)-1)
        value_inside=StringVar(fen)
        value_inside.set('choisir')
        question_menu =OptionMenu(fen, value_inside, *options_list) 
        question_menu.pack() 
        def print_answers(): 
            s=value_inside.get()
            #print(s[1:len(s)-2]) 
            print(s)
            return None
        submit_button = Button(fen, text='generate plot') 
        submit_button.pack() 
        # ph=PhotoImage(file='here.png') #motif des points cliquable
       
        submit_button["command"]=partial(generate_plot_generation,xy,nrj,begining_index,l_poscar,value_inside)
        #submit_button["command"]=print_answers
        fen.mainloop()  
def browse(b1,b2,b3,b4):
    p=filedialog.askopenfile()
    path=str(p)
    s=path.split("'")
    try:
        s1=s[1]
    except:
        return
    s1=list(s1)
    s11=''
    x="/"
    for a in s1:
        if a == x :
            s11=s11+'/'
        s11=s11+a
    if is_poscar(s11):
        print("c'est un poscar")
        b1['state']='disabled'
        b2['state']='active'
        b3['state']='active'
        b4['state']='disabled'
        b2['command']=partial(browse_txt,s11)
    elif is_res(s11):
        print("c'est un res")
        f=open(s11)
        l_res=f.read().split('\nEND\n') #lecture du fichier.res et separation des structures en listes
        del(l_res[-1]) #suppression d'un vide eventuel
        for i in range(len(l_res)): #ajout de END qui etait perdu en separation
            l_res[i]=l_res[i]+'\nEND\n'

        nrj=[]
        for i in range(len(l_res)):
            nrj.append(float(l_res[i].split(' ')[4]))
        xy=[]
        for i in range(len(l_res)):
            xy.append([i,nrj[i]])
        if len(xy)<=105:
            r=len(xy)
        
        else:
            r=100
        new_xy=[]
        for i in range(0,r):
            new_xy.append(coordinate_calcul(xy[i][0],xy[i][1],0,r-1,np.min(nrj),np.max(nrj)))
        path="C:\\Users\\br\\Desktop"
        os.chdir(path)
        fen=Tk()
        fen.title('liste des index existant')
        fen.geometry("300x300")
        options_list=list_index(len(nrj)-1)
        value_inside=StringVar(fen)
        value_inside.set('choisir')
        question_menu =OptionMenu(fen, value_inside, *options_list) 
        question_menu.pack() 
        submit_button = Button(fen, text='generate plot') 
        submit_button.pack() 
        # ph=PhotoImage(file='here.png') #motif des points cliquable      
        submit_button["command"]=partial(generate_plot_index,xy,nrj,l_res,value_inside)
        fen.mainloop()
    elif is_cif(s11):
        print("c'est un cif")
        cif=read(s11)
        view(cif)
    else:
        print("c'est pas un fichier lisible")
        CreateHover(b1,8,text='wrong file!')
    s2=s[1].split('.')
    if len(s2)<2:
        print("no extension")
    else:
        print(s2[1])
def back(b1,b2,b3,b4):
    b1['state']='active'
    b2['state']='disabled'
    b3['state']='disabled'
    b4['state']='active'
# def coordinate_calcul(x,y,minx,maxx,miny,maxy):
#     new_xy=[]
#     new_xy.append(167+(((x-minx)/(maxx-minx))*1063))
#     new_xy.append(669-(((y-miny)/(maxy-miny))*577))
#     return(new_xy)

def list_index(x):
    if x==0:
        return []
    elif x<=105:
        return [str(0)+"-"+str(x)]
    else:
        x2=x
        li=[]
        a1=0
        a2=99
        while x2>105:            
            li.append([str(a1)+"-"+str(a2)])
            x2-=100
            a1+=100
            a2+=100
        a2=a1+x2
        li.append([str(a1)+"-"+str(a2)])
        return li
def readable(x):
    try:
        y=read(x)
        return True
    except:
        return False 
def browse_xyz():
    data=[]
    datalist=[]
    p=filedialog.askdirectory()
    path=str(p)
    file_list=os.listdir(path)
    track=0
    to_delete=[]
    for a in file_list:
        path2=path+'/'+a
        track+=1
        if readable(path2) and (path2.split('.')[1]!='tar' and path2.split('.')[1]!='zip' and path2.split('.')[1]!='tgz' and path2.split('.')[1]!='rar') :    
            f=open(path2)
            f=f.read().split()
            x=0
            space_found=False
            energy_found=False
            for b in f:
                if 'spacegroup=' in b and not space_found:
                    data.append(b.split('=')[1])
                    x+=1
                    space_found=True
                if 'energy=' in b and not energy_found:
                    data.append(b.split('=')[1])
                    x+=1
                    energy_found=True
                if x==2:
                        datalist.append(data)
                        data=[]
                        break 
            else:
                if not space_found and not energy_found:
                    datalist.append(['0.0','no spacegroup'])
                elif not space_found:
                    data.append('no spacegroup')
                    datalist.append(data)
        else:
            to_delete.append(a)
    for a in to_delete:
        file_list.remove(a)
    for i in range(len(datalist)):
        try:
            datalist[i][0]=float(datalist[i][0])
            here=1
        except:
            datalist[i][1]=float(datalist[i][1])
            here=2
        datalist[i].insert(0,i+1)
    xy=[]
    for i in range(len(datalist)):
        xy.append(datalist[i][0:2])
    if len(xy)<=105:
        r=len(xy)
    else:
        r=100
    new_xy=[]
    nrj=[]
    for i in range(len(datalist)):
        nrj.append(datalist[i][here])
    if np.max(nrj)!=0.0 or np.min(nrj)!=0.0:
        for i in range(0,r):
            new_xy.append(coordinate_calcul(xy[i][0],xy[i][1],0,r-1,np.min(nrj),np.max(nrj)))
    path="C:\\Users\\br\\Desktop"
    os.chdir(path)
    if np.max(nrj)==0.0 and np.min(nrj)==0.0:
        fen1=Tk()
        fen1.title('liste des fichiers trouvés')
        fen1.geometry("300x300")
        options_list=file_list.copy()
        value_inside=StringVar(fen1)
        value_inside.set(options_list[1])
        question_menu =OptionMenu(fen1, value_inside, *options_list) 
        question_menu.pack() 
        submit_button = Button(fen1, text='view structure')           
        submit_button['command']=partial(view_xyz2,p,value_inside)
        submit_button.pack()  
    else:
        fen=Tk()
        fen.title('liste des index existant')
        fen.geometry("300x300")
        options_list=list_index(len(nrj)-1)
        value_inside=StringVar(fen)
        value_inside.set('choisir')
        question_menu =OptionMenu(fen, value_inside, *options_list) 
        question_menu.pack() 
        submit_button = Button(fen, text='generate plot') 
        submit_button.pack()  
        submit_button["command"]=partial(generate_plot_xyz,xy,nrj,datalist,file_list,str(p),value_inside)
        fen.mainloop() 
    