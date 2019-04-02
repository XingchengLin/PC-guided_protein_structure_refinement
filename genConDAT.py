####################################################################################
# This script will generate the contacts.dat file for gkuh based on the given structure
#
# Input: PDB structure
#
# Written by Xingcheng Lin, 07/25/2018
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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

###########################################


def genConDAT(GROfile, conDAT):

    inFile = open(GROfile, 'r')
    outFile = open(conDAT, 'w')

    lines_infile = [line.strip() for line in inFile]

    length = len(lines_infile)

    for i in my_lt_range(0, length, 1):

        line1 = lines_infile[i].split()

        # For relevant regions;

        try:
            line1[5]
        except:
            print("it is a trash line")
        else:
            if (is_number(line1[3])):

                # Calculate and output pair distance, only write down pairs with i<j-2;
                for j in my_lt_range(i + 3, length, 1):
                    line2 = lines_infile[j].split()
                    
                    try:
                        line2[5]
                    except:
                        print("it is also a trash line")
                    else:

                        # Only output the one with native distance smaller than 0.95 nm;

                        distance = math.sqrt((float(line1[3]) - float(line2[3]))**2 + (
                            float(line1[4]) - float(line2[4]))**2 + (float(line1[5]) - float(line2[5]))**2)

                        if (distance <= 0.95):
                            outFile.write(
                                str(line1[2]) + "\t" + str(line2[2]) + "\t" + str(0.95) + "\n")

    
    outFile.close()
    return

############################################################################


if __name__ == "__main__":

    GROFile = sys.argv[1]
    conDAT = sys.argv[2]

    genConDAT(GROFile, conDAT)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
