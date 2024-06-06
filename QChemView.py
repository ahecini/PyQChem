import os
from ase.io import read
from ase.visualize import view
from ase.io.res import Res,SinglePointCalculator
from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar

def read_resx(fn, index=-1): #fonction pour lire une chaine de caractères en tant que .res
    images = []
    res = Res.from_string(fn)
    if res.energy:
        calc = SinglePointCalculator(res.atoms,energy=res.energy)
        res.atoms.calc = calc
    images.append(res.atoms)
    return images[index]
def letmesee_poscar(n,l_poscar): #fonction pour visualiser une structure specifique avec un index donné
    # mol=view(read_resx(l[n]))
    poscar = Poscar.from_str(l_poscar[n])
    # print(poscar.structure)
    w = CifWriter(poscar.structure, symprec=1e-6)
    w.write_file('ouioui.cif')
    x=read('ouioui.cif')
    view(x)
    os.remove('ouioui.cif')
def letmesee_res(n,l_res): #fonction pour visualiser une structure specifique avec un index donné
    view(read_resx(l_res[n]))
def view_xyz(path):
    try:
        y=read(path)
        view(y)
    except:
        print('no')
        return
def view_xyz2(p,value_inside):
    s=str(p)+'/'+value_inside.get()
    view_xyz(s) 