######################################################################################
# This script will help match the TRACE file with the reaction coordinate file provided;
# i.e., the same time frame of TRACE file will be printed according to the same time
# frame of reaction coordinate file;
#
# Written by Xingcheng Lin, 03/06/3015;
#######################################################################################

import time
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
#############################################

def biasMatchEne(inputFile1, inputFile2, outputFile1, outputFile2):

    infile1 = open(inputFile1, "r")
    infile2 = open(inputFile2, "r")
    
    outfile1 = open(outputFile1, "w")
    outfile2 = open(outputFile2, "w")
    
    # Read in lines from both files;
    
    lines1 = [line1.strip() for line1 in infile1]
    lines2 = [line2.strip() for line2 in infile2]
    
    infile1.close()
    infile2.close()
    
    length1 = len(lines1)
    length2 = len(lines2)
    
    
    # Do a loop to check if the time frames overlap;
    
    for i in my_lt_range(0, length1, 1):
    
        print(i)
    
        line1 = lines1[i].split()
    
        # The number of times in recording frequency between infile1 and infile2;
        factor = 0.99
        jst = int(i * factor)
    
        for j in my_lt_range(jst, length2, 1):
            line2 = lines2[j].split()
    
            # If time frame matches, print it out;
            # Here, we want to get rid of the initial non-equilibrated region, the first 5 ns of moving restraint;
            if (int(float(line1[0])) == int(float(line2[0])) and float(line1[0])>7500):
                outfile1.write(lines1[i] + "\n")
                outfile2.write(lines2[j] + "\n")
    
                break
    
    outfile1.close()
    outfile2.close()

############################################################################


if __name__ == "__main__":

    inputFile1 = sys.argv[1]
    inputFile2 = sys.argv[2]
    outputFile1 = sys.argv[3]
    outputFile2 = sys.argv[4]

    biasMatchEne(inputFile1, inputFile2, outputFile1, outputFile2)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
