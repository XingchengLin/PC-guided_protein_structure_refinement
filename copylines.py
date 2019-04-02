##############################################################
# This script will help copy lines after and before several
# word patterns from one file into another file

# Written by Xingcheng Lin, 04/24/3017
##############################################################

import math
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

###########################################


infilename = sys.argv[1]
outfilename = sys.argv[2]

patternStart = sys.argv[3]
patternEnd = sys.argv[4]


infile = open(infilename, 'r')
outfile = open(outfilename, 'w')

lines = [line.strip() for line in infile]

infile.close()

length = len(lines)

# flag for recording into output file;
recordFlag = 0

for i in my_lt_range(0, length, 1):
    line = lines[i].split()

    try:
        line[0]
    except IndexError:
        continue
    else:
        # From the next line AFTER pattternStart, start recording;
        if (recordFlag == 1 and lines[i] != patternEnd):
            outfile.write(lines[i] + "\n")

        # If patternStart matched, change the flag to copy into another file;
        if (lines[i] == patternStart):

            recordFlag = 1

        # If patternEnd matched, change the flag to stop copying;
        if (lines[i] == patternEnd):

            recordFlag = 0
            break


outfile.close()
