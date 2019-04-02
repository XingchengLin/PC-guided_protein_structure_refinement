###########################################################################
# This script will help build .ali file for modeller to fill in missing
# residues;
# input: .seq file from buildseq.py and .fasta file for a complete sequence
# Or: two .seq file from buildseq.py, that is for the purpose of adding
# side chains;
#
# Written by Xingcheng Lin, 05/28/2017;
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


def forAli(firstFile, secondFile, outputFile):

    from splitString import splitString

    # Get current working directory
    pwd = os.getcwd()

    infile1 = open(firstFile, "r")
    infile2 = open(secondFile, "r")
    outfile = open(outputFile, "w")

    # Read in lines from the file;

    lines1 = [line.strip() for line in infile1]
    lines2 = [line.strip() for line in infile2]

    infile1.close()
    infile2.close()

    # Length1 should equals to lenght2;
    length1 = len(lines1)
    length2 = len(lines2)

    # Flags for recording outputs;
    flag1 = 0
    flag2 = 0

    for i in my_lt_range(0, length1, 1):

        line1 = lines1[i].split()

        try:
            line1[0]
        except IndexError:
            continue
        else:
            line1_0 = list(line1[0])

            if (line1_0[0] == ">"):
                flag1 = 1
            else:
                flag1 = 0

            # For the first input file, the sequence is in the next two lines
            # of ">" label;
            if (flag1 == 1):
                recordLine1 = lines1[i]
                recordLine2 = lines1[i + 1]
                # In case the sequences are written in multiple lines;
                count = 2
                seq1 = splitString(lines1[i + count])
                while (seq1[-1] != '*'):
                    count += 1
                    seq1.extend(splitString(lines1[i + count]))
                break

    # Separate between the cases whether one .fasta file is provided or same
    # .seq file is provided as the second input file;
    if (''.join(secondFile[-3:]) == 'sta'):

        for i in my_lt_range(0, length2, 1):

            line2 = lines2[i].split()

            try:
                line2[0]
            except IndexError:
                continue
            else:
                line2_0 = list(line2[0])

                if (line2_0[0] == ">"):
                    flag2 = 1
                else:
                    flag2 = 0

                # For the second input file, the sequence is in the next one
                # lines of ">" label;
                if (flag2 == 1):
                    seq2 = splitString(lines2[i + 1])
                    # Fasta format does not have asterisk in the end, but it is
                    # required here;
                    seq2.append("*")
                    break

        # Compare seq1 and seq2, whenever seq1 missed the same entry as in
        # seq2, we insert a gap;
        length = len(seq2)
        for i in my_lt_range(0, length, 1):
            if (seq1[i] != seq2[i]):
                seq1.insert(i, "-")

        # Output to file;
        outfile.write(recordLine1 + "\n")
        outfile.write(recordLine2 + "\n")
        recordLine3 = ''.join(seq1)
        outfile.write(recordLine3 + "\n")
        outfile.write(recordLine1 + "_fill" + "\n")
        outfile.write("sequence:::::::::" + "\n")
        recordLine6 = ''.join(seq2)
        outfile.write(recordLine6 + "\n")

    elif (''.join(secondFile[-3:]) == 'seq'):

        for i in my_lt_range(0, length2, 1):

            line2 = lines2[i].split()

            try:
                line2[0]
            except IndexError:
                continue
            else:
                line2_0 = list(line2[0])

                if (line2_0[0] == ">"):
                    flag2 = 1
                else:
                    flag2 = 0

                # For the second input file, the sequence is in the next two
                # lines of ">" label;
                if (flag2 == 1):
                    # In case the sequences are written in multiple lines;
                    count = 2
                    seq2 = splitString(lines1[i + count])
                    while (seq2[-1] != '*'):
                        count += 1
                        seq2.extend(splitString(lines1[i + count]))
                break

        # Output to file;
        outfile.write(recordLine1 + "\n")
        outfile.write(recordLine2 + "\n")
        recordLine3 = ''.join(seq1)
        outfile.write(recordLine3 + "\n")
        outfile.write(recordLine1 + "_fill" + "\n")
        outfile.write("sequence:::::::::" + "\n")
        recordLine6 = ''.join(seq2)
        outfile.write(recordLine6 + "\n")

    return


############################################################################
if __name__ == "__main__":
    firstFile = sys.argv[1]
    secondFile = sys.argv[2]
    outputFile = sys.argv[3]

    forAli(firstFile, secondFile, outputFile)

    print("Beauty is truth\'s smile")
    print("when she beholds her own face in")
    print("a perfect mirror.")
