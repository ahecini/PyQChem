# PyQChem:Python modules for Quantum Chemistry
This Python application is made to visualize and analyze crisallographic structures by using as an input various types of files used in quantum chemistry.
What this application enables:\n
-visualization of molecule structure.
-interactive plots: structures are classified by their energy and index or group number in a scatter plot with clickable points to enable visualization and a zoom feature (for the energy/group number plot).
-read one file at a time: cif,xyz and vasp: can only be visualized.
                          res: can generate an energy/index plot.
                          gathered poscar file+USPEX file: can generate an energy/generation plot.
-read multiple files contained in folder: cif and vasp: can only be visualized.
                                          xyz: if the energy is mentionned in the file an energy/index plot can be generated. 
