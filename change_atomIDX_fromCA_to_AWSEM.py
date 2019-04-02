####################################################################################
# This script will change the indices of atoms in the PDB from CA to AWSEM format
#
# Input: CA PDB
#
# Written by Xingcheng Lin, 10/12/2017
####################################################################################

import math
import subprocess
import os
import math
import numpy as np
import sys
import time
from Bio.PDB import *
################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step


def my_le_range(start, end, step):
    while start <= end:
        yield start
        start += step
###########################################


def change_atomIDX_fromCA_to_AWSEM(pdbFile, converted_pdbFile):
    parser = PDBParser()

    CAstruct = parser.get_structure('CAstruct', pdbFile)   
    atom_list = Selection.unfold_entities(CAstruct, 'A')

    atom_indices=[]

    for f in atom_list:
        atom_indices.append(f.get_serial_number())

    atom_indices = np.asarray(atom_indices)

    # The CA index of AWSEM format will be CA_index * 3 - 2;
    converted_atom_indices = atom_indices * 3 - 2

    for i in my_lt_range(0, len(atom_indices), 1):
        atom_list[i].set_serial_number(converted_atom_indices[i])
 
    Selection.unfold_entities(CAstruct, 'A') = atom_list
    
    io = PDBIO()
    io.set_structure(CAstruct)
    io.save(converted_pdbFile)

    return

############################################################################


if __name__ == "__main__":

    pdbFile = sys.argv[1]
    converted_pdbFile = sys.argv[2]

    change_atomIDX_fromCA_to_AWSEM(pdbFile, converted_pdbFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
