####################################################################################
# This script will normalize the sasa for each residue based on their residue
# identity
#
# Written by Xingcheng Lin, 09/30/2017
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


def compareforcommon(sasaFile, pdbFile, outputFile):

    # Get current working directory
    pwd = os.getcwd()

    in_sasaFile = open(sasaFile, 'r')
    in_pdbFile = open(pdbFile, 'r')
    outfile = open(outputFile, 'w')

    # Read in lines from the file;

    lines_sasa = [line.strip() for line in in_sasaFile]
    lines_pdb = [line.strip() for line in in_pdbFile]

    in_sasaFile.close()
    in_pdbFile.close()

    length_sasa = len(lines_sasa)
    length_pdb = len(lines_pdb)

    glyXgly = {'ALA': 64.9, 'ARG': 195.5, 'ASN': 114.3, 'ASP': 113.0, 'CYS': 102.3, 'GLU': 141.2, 'GLN': 143.7, 'GLY': 87.2, 'HIS': 154.6, 'ILE': 147.3,
               'LEU': 146.2, 'LYS': 164.5, 'MET': 158.3, 'PHE': 180.1, 'PRO': 105.2, 'SER': 77.4, 'THR': 106.2, 'TRP': 224.6, 'TYR': 193.1, 'VAL': 122.3}

    for i in my_lt_range(0, length_sasa, 1):

        line_sasa = lines_sasa[i].split()

        for j in my_lt_range(0, length_pdb, 1):

            line_pdb = lines_pdb[j].split()

            try:
                line_pdb[5]
            except IndexError:
                continue
            else:
                # If it is integer, we can compare to see if it is the corresponding residue number;
                try:
                    int(line_pdb[5])
                except ValueError:
                    continue
                else:
                    # Because we should only allow one line of each residue to compare with the resid, we select "CA"
                    if (line_pdb[5] == line_sasa[0] and line_pdb[2] == "CA"):

                        resname = line_pdb[3]

                        ref_area = float(glyXgly[resname])

                        # because the output from gmx sasa is in the unit of nm^2, and the glyXgly referenced area above is in the unit of A^2;

                        norm_area = float(line_sasa[1]) * 100 / ref_area

                        outfile.write(
                            line_sasa[0] + "\t" + str(norm_area) + "\n")

    outfile.close()
    return

############################################################################


if __name__ == "__main__":

    sasaFile = sys.argv[1]
    pdbFile = sys.argv[2]
    outputFile = sys.argv[3]

    compareforcommon(sasaFile, pdbFile, outputFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
