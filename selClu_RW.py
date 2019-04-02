####################################################################################
# This script will help sort and select the structures according to the RW value
#
# Written by Xingcheng Lin, 06/11/3017
####################################################################################

import math
import subprocess
import os
import time
import numpy as np
import shutil
import sys

################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step


def my_le_range(start, end, step):
    while start <= end:
        yield start
        start += step


def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
###########################################


def selClu_RW(inputFile, numFilter):

    # Name of the folder for the selected structures;
    selFolder = inputFile + '.selStructure'
    if os.path.exists(selFolder):
        shutil.rmtree(selFolder)
        os.makedirs(selFolder)
    else:
        os.makedirs(selFolder)
    # Get current working directory
    pwd = os.getcwd()

    in_str = pwd + '/' + inputFile + '.short.txt'

    # Load in RW output file;
    rwScore = np.loadtxt(in_str)

    # Sort according to the RW score;
    # Here we need top lowest score instead of the highest, so we add a minus sign before the rwScore array;
    sortIndex = np.argsort(-rwScore[:, 1])

    # Get the index of the filtered structures;
    FilteredStructureIndex = rwScore[sortIndex[-numFilter:], 0].astype(int)

    # output the rw plus score of the selected structures;
    # REMEMBER to FLIP the order so that it is the same as the ranking structures!
    np.savetxt(selFolder + '/rwplusScore.short.txt',
               np.flip(rwScore[sortIndex[-numFilter:], 1], 0))
    # output the rw plus score of the starting structure;
    np.savetxt(selFolder + '/rwplusScore.short.start.txt',
               np.array(rwScore[0, 1]).reshape(1,))

    # The ranking of the structure based on rw value, from large RW to low RW (because of the minus sign here, it reverses);
    rank = numFilter
    for i in np.nditer(FilteredStructureIndex):
        rank -= 1
#        print i;
        # Copy the selected file into a new folder;
        # Note lowTstrcture is 0 based, while rwplusScore.short.txt is 1 based!
        selected = 'lowTstructure' + str(i - 1) + '.pdb'
        dst = selFolder + '/rwranked.' + str(rank) + '.pdb'
        shutil.copyfile(selected, dst)


############################################################################

if __name__ == "__main__":
    # Output from the CalcRW program;
    inputFile = sys.argv[1]
    # Number of filtered structure we want to have;
    numFilter = int(sys.argv[2])

    selClu_RW(inputFile, numFilter)

    print("Beauty is truth\'s smile")
    print("when she beholds her own face in")
    print("a perfect mirror.")
