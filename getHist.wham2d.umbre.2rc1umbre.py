#################################################################################
# This script help prepare the config file for the WHAM code;
#
# Written by Xingcheng Lin, 05/13/3014;
#################################################################################

import math
import subprocess
import os
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

###########################################

# Get PC index
PCindex = int(sys.argv[1])
startID = int(sys.argv[2])
endID = int(sys.argv[3])
varofInterest = sys.argv[4]


dir = os.environ['PWD']
histName = dir + "/hist"
whamdirName = dir + "/wham2d"
# Delete the previously existing wham file;
subprocess.call(["rm", "-rf", whamdirName])
# create a new wham file;
subprocess.call(["mkdir", "-p", whamdirName])

outfile = open("config", 'w')

# Temperature step in the hist file, Note highT and lowT should be the intersection of high/low ends of all simulations;
lowT = 300
highT = 300
stepT = 10
# Here we start to bin the temperatures;
numoftBin = int((highT - lowT) / stepT + 0.5) + 1

# Umbrella bias and reference list;
umbrelist1 = [5.0]
minPMF_PCbefore=0.0
reflist1 = []
for i in my_le_range(startID, endID, 1):
    ref = minPMF_PCbefore + 1.0*(i - 3)
    reflist1.append(round(ref, 3)) 

numDimensions = 4
outfile.write("numDimensions" + "\t" + str(numDimensions) + "\n")

# Need two umbrella types!
outfile.write("umbrellaType" + "\t" + "harmonic" + "\n")

numUmbrella = 1
outfile.write("numUmbrella" + "\t" + str(numUmbrella) + "\n")

threads = 8
outfile.write("threads" + "\t" + str(threads) + "\n")

kB = 0.008314
outfile.write("kB" + "\t" + str(kB) + "\n")

# For setting up the WHAM options;
maxIterations = 100000
tolerance = 0.0001

outfile.write("maxIterations" + "\t" + str(maxIterations) + "\n")
outfile.write("tolerance" + "\t" + str(tolerance) + "\n")

# For calculating density of states;
outfile.write("\n")
outfile.write("run_wham" + "\n")

dosFile = whamdirName + "/dos"
outfile.write("dosFile" + "\t" + dosFile + "\n")

# For calculating free energy
freeName = whamdirName + "/free"
subprocess.call(["mkdir", "-p", freeName])

outfile.write("\n")
outfile.write("run_free" + "\n")

run_free_out = whamdirName + "/free/"
outfile.write("run_free_out" + "\t" + run_free_out + "\n")

startTF = lowT
deltaTF = stepT
ntempsF = numoftBin

outfile.write("startTF" + "\t" + str(startTF) + "\n")
outfile.write("deltaTF" + "\t" + str(deltaTF) + "\n")
outfile.write("ntempsF" + "\t" + str(ntempsF) + "\n")

# For calculating the heat capacity;
outfile.write("\n")
outfile.write("run_cv" + "\n")

run_cv_out = whamdirName + "/cv"
outfile.write("run_cv_out" + "\t" + run_cv_out + "\n")

startT = lowT
deltaT = stepT
ntemps = numoftBin

outfile.write("startT" + "\t" + str(startT) + "\n")
outfile.write("deltaT" + "\t" + str(deltaT) + "\n")
outfile.write("ntemps" + "\t" + str(ntemps) + "\n")

# For calculating Q2(Q1)
outfile.write("\n")
outfile.write("run_coord" + "\n")

run_coord_out = whamdirName + "/coord"
outfile.write("run_coord_out" + "\t" + run_coord_out + "\n")

startT = lowT

outfile.write("startTC" + "\t" + str(startT) + "\n")

# energy and Q bins;
outfile.write("\n")

leastEne = 100000
mostEne = -5000000
leastQ1 = 500
mostQ1 = -500
leastQ2 = 50000
mostQ2 = -50000
leastUm1 = 500
mostUm1 = -500

# Here we calculate the number of files used;
numFiles = 0

for i in my_le_range(lowT, highT, stepT):
    for j in umbrelist1:
        for k in reflist1:
            histfile = histName + '/T' + str(i) + '/umbre1.fc' + str(j) + '/r10_' + str("{0:.3f}".format(k)) + '/hist.dat'
            numFiles += 1
            with open(histfile, 'r') as infile:
                for line in iter(infile.readline, ''):
                    line = line.rstrip()
                    tmp = line.split()
                    if float(tmp[0]) < leastEne:
                        leastEne = float(tmp[0])
                    if float(tmp[0]) > mostEne:
                        mostEne = float(tmp[0])
                    if float(tmp[1]) < leastQ1:
                        leastQ1 = float(tmp[1])
                    if float(tmp[1]) > mostQ1:
                        mostQ1 = float(tmp[1])
                    if float(tmp[2]) < leastQ2:
                        leastQ2 = float(tmp[2])
                    if float(tmp[2]) > mostQ2:
                        mostQ2 = float(tmp[2])
                    if float(tmp[3]) < leastUm1:
                        leastUm1 = float(tmp[3])
                    if float(tmp[3]) > mostUm1:
                        mostUm1 = float(tmp[3])

print(str(leastEne) + "\t" + str(mostEne) + "\t" + str(leastQ1) + "\t" + str(mostQ1) + "\t" + str(leastQ2) + "\t" + str(mostQ2) + "\t" + str(leastUm1) + "\t" + str(mostUm1))
stepE = 100.0
stepQ1 = 0.05
if (varofInterest == 'rmsd'):
    stepQ2 = 0.01
elif (varofInterest == 'rmsdSq'):
    stepQ2 = 0.01
elif (varofInterest == 'awsemEne'):
    stepQ2 = 10.0
elif (varofInterest == 'rwplus'):
    stepQ2 = 10.0
elif (varofInterest == 'PC2'):
    stepQ2 = 0.05
stepUm1 = 0.05

# energy binning;
outfile.write("\n")
numEneBins = int((mostEne - leastEne) / stepE + 0.5)
outfile.write("numBins" + "\t" + str(numEneBins) + "\n")
outfile.write("start" + "\t" + str(leastEne) + "\n")
outfile.write("step" + "\t" + str(stepE) + "\n")

# Q binning;
precision = 3

outfile.write("\n")
leastQ1 = round(leastQ1, precision)
numQ1Bins = int((mostQ1 - leastQ1) / stepQ1 + 0.5)
outfile.write("numBins" + "\t" + str(numQ1Bins) + "\n")
outfile.write("start" + "\t" + str(leastQ1) + "\n")
outfile.write("step" + "\t" + str(stepQ1) + "\n")

outfile.write("\n")
leastQ2 = round(leastQ2, precision)
numQ2Bins = int((mostQ2 - leastQ2) / stepQ2 + 0.5)
outfile.write("numBins" + "\t" + str(numQ2Bins) + "\n")
outfile.write("start" + "\t" + str(leastQ2) + "\n")
outfile.write("step" + "\t" + str(stepQ2) + "\n")

# Umbrella binning;
outfile.write("\n")
leastUm1 = round(leastUm1, precision)
numUmBins = int((mostUm1 - leastUm1) / stepUm1 + 0.5)
outfile.write("numBins" + "\t" + str(numUmBins) + "\n")
outfile.write("start" + "\t" + str(leastUm1) + "\n")
outfile.write("step" + "\t" + str(stepUm1) + "\n")

# list of histogram filenames and their temperatures;
outfile.write("\n")
outfile.write("numFiles" + "\t" + str(numFiles) + "\n")

for i in my_le_range(lowT, highT, stepT):
    for j in umbrelist1:
        for k in reflist1:
            histfile = histName + '/T' + str(i) + '/umbre1.fc' + str(j) + '/r10_' + str("{0:.3f}".format(k)) + '/hist.dat'
            outfile.write("name" + " " + histfile + " " + "temp" + " " + str(i) + " " + "umbrella_k" + " " + str(j) + " " + "umbrella_0" + " " + str("{0:.3f}".format(k)) + "\n")

outfile.close()

# copy the config file into the wham folder;

shutil.copy("config", whamdirName)






