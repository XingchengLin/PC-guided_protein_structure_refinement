####################################################################################
# This script will convert PDB into fasta
#
# Input: PDB file
#
# Written by Xingcheng Lin, 04/21/2018
####################################################################################

import math
import subprocess
import os
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

def pdb2fasta(inPDBID, numResidue):

    infile = open(inPDBID + '.pdb', 'r');
    outfile = open (inPDBID + '.fasta', 'w');

    if len(sys.argv) <= 1:
        print('usage: python pdb2fasta.py file.pdb file.fasta')
        exit()

    letters = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H',
           'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
           'TYR': 'Y', 'VAL': 'V'}
    
    outfile.write('>P1;' + inPDBID + "\n");
    outfile.write('structureX:' + inPDBID + "::::::::\n");
    
    prev = 0
    resid = 0
    for line in infile:
        toks = line.split()
        if len(toks) < 1:
            continue
        if toks[0] != 'ATOM':
            continue
        # If it is increased by 1, we print out the token;
        if int(toks[5]) == (prev+1):
            outfile.write('%c' % letters[toks[3]])
            # Keep rolling on the current resid;
            resid += 1
            # update prev
            prev = int(toks[5])
        # If it is the same as previous token, just keep looping
        elif int(toks[5]) == prev:
            continue;
        # If it is more than two of previous, it indicates a missing residue, we print out a gap;
        else:
            numGap = (int(toks[5])-prev-1);
            outfile.write('-'*numGap);
            resid += numGap
            prev = prev + 1*numGap;

    # If there are still some residues missing by the end of the template file, we add in gap to fill it up;
    outfile.write('-'*(numResidue-resid))
    outfile.write('\n')
    infile.close()


############################################################################


if __name__ == "__main__":

    inPDBID = sys.argv[1]
    numResidue = int(sys.argv[2])

    pdb2fasta(inPDBID, numResidue)

    print("Done.")
