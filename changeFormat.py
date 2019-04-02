###########################################################################
# This script will help change the format of .gro file for the sake of
# mapIndex.py;
#
# Written by Xingcheng Lin, 05/03/2017;
###########################################################################

import time
import subprocess
import os
import math
import sys
import numpy as np

################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step


def my_le_range(start, end, step):
    while start <= end:
        yield start
        start += step
#############################################


def changeFormat(inputFile, outputFile):

    # Get current working directory
    pwd = os.getcwd()

    infile = open(inputFile, 'r')
    outfile = open(outputFile, 'w')

    # Read in lines from the file;

    lines = [line.strip() for line in infile]

    infile.close()

    length = len(lines)

    # Flag for output records;
    flag = 0

    for i in my_lt_range(0, length, 1):

        line = lines[i].split()

        # Second line of .gro tells you the number of residues;

        if i == 1:
            noResidue = int(line[0])
        # We don't need the last line;
        elif (i > 1 and i < (length - 1)):

            # Split the number from string for the first entry;
            import re
            firstEntry = re.findall('\d+|\D+', line[0])

            if (i == 2):
                # Print the first residue ID, for calculating residueOffset in bash;
                print(firstEntry[0])

            outfile.write(str(firstEntry[0]) + "\t" + str(firstEntry[1]) + "\t" + "A" + "\t" +
                          line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\n")

    # In order to pass the python variable to bash;
    print(noResidue)

    return


############################################################################

if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    changeFormat(inputFile, outputFile)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
