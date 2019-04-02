####################################################################################
# This script will get the residue index of PHE, TYR, ASP residues

# Written by Xingcheng Lin, 03/03/2018
####################################################################################

import math
import subprocess
import os
import math
import numpy as np
import sys
import time

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


def getIndex(pdbFile, indexFile):

    in_pdbFile = open(pdbFile, 'r')
    out_indexFile = open(indexFile, 'w')

    # Read in lines from the file;

    lines_pdb = [line.strip() for line in in_pdbFile]
    in_pdbFile.close()

    length_pdb = len(lines_pdb)

    for i in my_lt_range(0, length_pdb, 1):

        line_pdb = lines_pdb[i].split()

        try:
            line_pdb[3]
        except IndexError:
            continue
        else:
            if ((line_pdb[3] == 'PHE' or line_pdb[3] == 'TYR' or line_pdb[3] == 'ASP') and (line_pdb[2] == 'CA')):
                out_indexFile.write(str(line_pdb[5]) + "\n")

    out_indexFile.close()
    return

############################################################################


if __name__ == "__main__":

    pdbFile = sys.argv[1]
    indexFile = sys.argv[2]

    getIndex(pdbFile, indexFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
