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

# Clean the existing hist files;
deletefile = pwd + '/hist'
subprocess.call(['rm', '-r', deletefile])

# The list for temperatures;
lowT = 300
highT = 300
stepT = 10

# Here we start to bin the temperatures;
numoftBin = int((highT - lowT) / stepT + 0.5)

# mkdir the directory for each temperature and sbm bias;
# Two umbrella coordinate
umbrelist1 = [125.0]
reflist1 = [0.2, 0.4, 0.6, 0.8]
umbrelist2 = [125.0]
reflist2 = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

for i in my_le_range(0, numoftBin, 1):
    for j in umbrelist1:
        for k in reflist1:
            for l in umbrelist2:
                for m in reflist2:                    
                    # Temperature representing each bin;
                    temp = int(i * stepT + lowT)
    
                    # mkdir folder for hist file;
                    out_str = pwd + '/hist/T'
                    out_str += repr(temp)
                    out_str += '/umbre1.fc'
                    out_str += str(j)
                    out_str += '/r10_'
                    out_str += str(k)
                    out_str += '/umbre2.fc'
                    out_str += str(l)
                    out_str += '/r20_'
                    out_str += str(m)
        
                    # Create the corresponding empty histogram files;
                    subprocess.call(['mkdir', '-p', out_str])
                    os.chdir(out_str)
                    open('hist.dat', 'a').close()
    
# go through energy and qValue file, sort the energy and Q according to each temperature;

for j in umbrelist1:
    for k in reflist1:
        for l in umbrelist2:
            for m in reflist2:

                # input data file;
                dir = pwd + '/dataFile'
                dir += '/umbre1.fc'
                dir += str(j)
                dir += '/r10_'
                dir += str(k)
                dir += '/umbre2.fc'
                dir += str(l)
                dir += '/r20_'
                dir += str(m)
    
                instrlist = [dir]
    
                for address in instrlist:
    
                    print(address)
                    # Get into the corresponding folder;
                    os.chdir(address)
    
                    in_str1 = address + '/tot.energy-good.xvg'
                    in_str2 = address + '/pcarmsd-good.txt'
    
                    infile1 = open(in_str1, 'r')
                    infile2 = open(in_str2, 'r')
    
                    lines1 = [line.strip() for line in infile1]
                    lines2 = [line.strip() for line in infile2]
    
                    infile1.close()
                    infile2.close()
    
                    # The length should be the same for all of the files; at some crappy
                    # runs, some will be one line longer than the other just because simulation
                    # is not stopped well, in that case we choose the shortest length;
                    lengthlist = [len(lines1), len(lines2)]
                    length = min(lengthlist)
                    print(length)
    
                    # We need to delete some part of file that is still in the stage of non-equilibrium;
                    # Here, the movining restraint before it goes to the final spring strength, first 5 ns;
                    nonEquiliLen = 0
    
                    for n in my_lt_range(nonEquiliLen, length, 1):
                        line1 = lines1[n].split()
                        line2 = lines2[n].split()
    
                        energy = float(line1[1])
                        q1Value = float(line2[1])
                        q2Value = float(line2[2])
                        qUmbre1 = float(line2[1])
                        qUmbre2 = float(line2[2])
    
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
                        out_str += str(k)
                        out_str += '/umbre2.fc'
                        out_str += str(l)
                        out_str += '/r20_'
                        out_str += str(m)
                        out_str += '/hist.dat'
    
                        # Output the hist file represented as different temperatures and different SBM bias;
                        outfile = open(out_str, 'a')
    
                        # print the energy and Q values into the hist file (white space separated instead of
                        # tab separated, format required by the Jeff WHAM code);
    
                        outfile.write(str(energy) + " " + str(q1Value) +
                                      " " + str(q2Value) + " " + str(qUmbre1) + " " + str(qUmbre2) + "\n")
    
                        outfile.close()
