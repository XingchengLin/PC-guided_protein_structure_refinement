####################################################################################
# This script will generate the plumed format to do secondary structural bias based
# on Jpred results;
# The "processed.pdb" file is converted from trjconv, and it should have a format that
# the last atom of each residue is O here; Also, the line after the last atom information
# should be "TER", 3 characters;
# For each helical peptide, the first and the last residue is not considered into the
# hbond, thus giving it more flexibility;
#
# Written by Xingcheng Lin, 11/20/3015
####################################################################################

import math
import subprocess
import os
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


# Get current working directory
pwd = os.getcwd()

instr1 = pwd + '/processed.pdb'
instr2 = pwd + '/ssbias.dat'

outstr1 = pwd + '/hbonds1.dat'
outstr2 = pwd + '/hbonds2.dat'

infile1 = open(instr1, 'r')
infile2 = open(instr2, 'r')
outfile1 = open(outstr1, 'w')
outfile2 = open(outstr2, 'w')

lines1 = [line.strip() for line in infile1]
lines2 = [line.strip() for line in infile2]
infile1.close()
infile2.close()

length1 = len(lines1)
length2 = len(lines2)

# Flag for alpha helix;
alphaflag = 0
alphastartID = 0
alphaendID = 0
# Flag for recording one peptide of alpha helix;
peptideFlag = 0
# For recording the location of 'O' and 'N' in alpha peptide;
alphaO = [0] * length2
alphaN = [0] * length2

# We only loop until the last but one line, for the sake of
# the "next line checking" later on; The line after the last atom line should
# be a 3 characters "TER";
for i in my_lt_range(0, length1 - 1, 1):
    line1 = lines1[i].split()
    # The line for checking if it is the last residue;
    lengthlineNext = len(lines1[i + 1])

    # Check if there is column 1;
    try:
        line1[10]
    except:
        continue

    # Check for the *last* atom of each residue, if it is alpha helix;
    # Here the last atom is O;
    if line1[2] == 'O':
        resid = int(line1[5])
        # ssbias.dat file is zero based;
        line2 = lines2[resid - 1].split()
        # If it is alpha, change the flag;

        if alphaflag == 0 and line2[1] == '1.0':
            alphaflag = 1
            # We don't consider the first residue into the alpha peptide hbond bias;
            alphastartID = int(line2[0]) + 1
            peptideFlag += 1
        # Two possibilities: The end of one helical peptide, or the end of fragment;
        # Check if it is the last atom of this fragment;
        elif alphaflag == 1 and line2[1] == '0.0':
            alphaflag = 0
            # end ID is the ID one before this one;
            # We don't consider the last residue into the alpha peptide hbond bias;
            alphaendID = int(line2[0]) - 2
            peptideFlag += 1
        elif peptideFlag == 1 and lengthlineNext == 3:
            # end ID is the ID of this one;
            # We don't consider the last residue into the alpha peptide hbond bias;
            alphaendID = int(line2[0]) - 1
            peptideFlag = 2

        if peptideFlag == 2:
            print((int(alphastartID), int(alphaendID)))
            # Revert flag back to zero;
            peptideFlag = 0
            for j in my_lt_range(0, length1, 1):
                lineAlpha = lines1[j].split()
                try:
                    lineAlpha[11]
                except:
                    continue

                if int(lineAlpha[5]) >= (alphastartID) and int(lineAlpha[5]) <= (alphaendID - 4) and lineAlpha[2] == 'O':
                    outfile1.write(lineAlpha[1] + "\n")
                elif int(lineAlpha[5]) >= (alphastartID + 4) and int(lineAlpha[5]) <= (alphaendID) and lineAlpha[2] == 'N':
                    outfile2.write(lineAlpha[1] + "\n")

outfile1.close()
outfile2.close()
