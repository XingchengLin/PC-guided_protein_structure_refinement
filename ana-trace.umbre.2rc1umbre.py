####################################################################################
# This script will analyze the TRACE and qValue file and prepare it for the WHAM calculation
# It will organize the data according to their temperatures
#
# Written by Xingcheng Lin, 07/03/3015
####################################################################################

import math
import subprocess
import os
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
###########################################

# Get PC index
PCindex = int(sys.argv[1])
startID = int(sys.argv[2])
endID = int(sys.argv[3])
varofInterest = sys.argv[4]

# Get current working directory
pwd = os.getcwd()

# Clean the existing hist files;
deletefile = pwd + '/hist'
subprocess.call(['rm', '-r', deletefile])

# The list for temperatures;
lowT = 300
highT = 300
stepT = 10

# Here we start to bin the temperatures;
numoftBin = int((highT - lowT) / stepT + 0.5)

# Umbrella bias and reference list;
umbrelist1 = [5.0]
minPMF_PCbefore=0.0
reflist1 = []
for i in my_le_range(startID, endID, 1):
    ref = minPMF_PCbefore + 1.0*(i - 3)
    reflist1.append(round(ref, 3)) 
        
for i in my_le_range(0, numoftBin, 1):
    for j in umbrelist1:
        for k in reflist1:
            # Temperature representing each bin;
            temp = int(i * stepT + lowT)

            # mkdir folder for hist file;
            out_str = pwd + '/hist/T'
            out_str += repr(temp)
            out_str += '/umbre1.fc'
            out_str += str(j)
            out_str += '/r10_'
            out_str += str("{0:.3f}".format(k))
        
            # Create the corresponding empty histogram files;
            subprocess.call(['mkdir', '-p', out_str])
            os.chdir(out_str)
            open('hist.dat', 'a').close()
    
# go through energy and qValue file, sort the energy and Q according to each temperature;

for j in umbrelist1:
    for k in reflist1:

        # input data file;
        dir = pwd + '/dataFile'
        dir += '/umbre1.fc'
        dir += str(j)
        dir += '/r10_'
        dir += str("{0:.3f}".format(k))
    
        instrlist = [dir]
    
        for address in instrlist:
    
            print(address)
            # Get into the corresponding folder;
            os.chdir(address)
    
            in_str1 = address + '/tot.energy-good.xvg'
            in_str2 = address + '/pcarmsd_scaled-good.txt'
            if (varofInterest == 'rmsd'):
                in_str3 = address + '/rmsd-good.txt'
            elif (varofInterest == 'rmsdSq'):
                in_str3 = address + '/rmsd_sq-good.txt'
            elif (varofInterest == 'awsemEne'):
                in_str3 = address + '/potential-good.txt'
            elif (varofInterest == 'rwplus'):
                in_str3 = address + '/rwplus-good.txt'
            elif (varofInterest == 'PC2'):
                in_str3 = address + '/pcarmsd_scaled-good.txt'
    
            infile1 = open(in_str1, 'r')
            infile2 = open(in_str2, 'r')
            infile3 = open(in_str3, 'r')
    
            lines1 = [line.strip() for line in infile1]
            lines2 = [line.strip() for line in infile2]
            lines3 = [line.strip() for line in infile3]
    
            infile1.close()
            infile2.close()
            infile3.close()
    
            # The length should be the same for all of the files; at some crappy
            # runs, some will be one line longer than the other just because simulation
            # is not stopped well, in that case we choose the shortest length;
            lengthlist = [len(lines1), len(lines2), len(lines3)]
            length = min(lengthlist)
            print(length)
    
            # We need to delete some part of file that is still in the stage of non-equilibrium;
            # Here, the movining restraint before it goes to the final spring strength, first 5 ns;
            nonEquiliLen = 0
    
            for n in my_lt_range(nonEquiliLen, length, 1):
                line1 = lines1[n].split()
                line2 = lines2[n].split()
                line3 = lines3[n].split()
    
                energy = float(line1[1])
                q1Value = float(line2[PCindex])
                if (varofInterest == 'PC2'):
                    q2Value = float(line3[PCindex+1])
                else:
                    q2Value = float(line3[1])
                qUmbre1 = float(line2[PCindex])
    
                temperature = 300

                # Try to find which bin this temperature belongs to;
                tempIdentity = int((temperature - lowT) / stepT + 0.5)
                tempBin = int(lowT + tempIdentity * stepT)
    
                # Temperature representing each bin;
    
                # Output hist file;
                out_str = pwd + '/hist/T'
                out_str += repr(tempBin)
                out_str += '/umbre1.fc'
                out_str += str(j)
                out_str += '/r10_'
                out_str += str("{0:.3f}".format(k))
                out_str += '/hist.dat'
    
                # Output the hist file represented as different temperatures and different SBM bias;
                outfile = open(out_str, 'a')
    
                # print the energy and Q values into the hist file (white space separated instead of
                # tab separated, format required by the Jeff WHAM code);
    
                outfile.write(str(energy) + " " + str(q1Value) + " " + str(q2Value) + " " + str(qUmbre1) + "\n")
    
                outfile.close()
