###########################################################################
# This script will replace one line of one file with another line of
# another file;

# Input: target File name; index of line wanted to be replaced in target file;
# template file name; index of line that will replace the target line;
#
# Written by Xingcheng Lin, 04/22/2018;
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


def replaceLine(targetFile, targetLine, templateFile,
                templateLine, outputFileName):

    targetFile = open(targetFileName, 'r')
    templateFile = open(templateFileName, 'r')
    outputFile = open(outputFileName, 'w')

    # Read in lines from the file;
    lines_targetFile = [line.strip() for line in targetFile]
    lines_templateFile = [line.strip() for line in templateFile]

    targetFile.close()
    templateFile.close()

    length_targetFile = len(lines_targetFile)
    length_templateFile = len(lines_templateFile)

    for i in my_lt_range(0, length_targetFile, 1):
        
        # Remember the zero-based python
        if i != (targetLine - 1):
            outputFile.write(lines_targetFile[i] + "\n")
        else:
            # Remember the zero-based python
            outputFile.write(lines_templateFile[templateLine - 1] + "\n")

    outputFile.close()
    return


############################################################################

if __name__ == "__main__":

    targetFileName = sys.argv[1]
    targetLine = int(sys.argv[2])
    templateFileName = sys.argv[3]
    templateLine = int(sys.argv[4])
    outputFileName = sys.argv[5]

    replaceLine(
        targetFileName,
        targetLine,
        templateFileName,
        templateLine,
        outputFileName)

    print("Beauty is truth\' smile")
    print("when she beholds her own face in")
    print("a perfect mirror.")
