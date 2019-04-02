####################################################################################
# This script will help sort the cluster generated from CST according to cluster.log file
# It will then output the biggest clusters accumulated to 90% of the total entries;
#
# Written by Xingcheng Lin, 12/10/3015
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

in_str = pwd + '/cluster.log'

infile = open(in_str, 'r')

lines = [line.strip() for line in infile]
infile.close()

length = len(lines)

# Number for each cluster;
sizeCluster = []
noCluster = []
timestampCluster = []
# Total number of snapshots;
totCount = 0
# flag for starting cluster counting;
flag = 0

for i in my_lt_range(0, length, 1):
    line = lines[i].split()

    # Check if there is column 1;
    try:
        line[0]
    except:
        continue

    if flag == 0 and line[0] == "cl.":
        flag = 1
    # Start after the line "cl.";
    if flag == 1:
        # We select only the case where there are more than one entries in a cluster;
        if line[2].isdigit() and line[2] != "1":
            noCluster.append(int(line[0]))
            sizeCluster.append(int(line[2]))
            timestampCluster.append(float(line[5]))
            totCount += float(line[2])
# Make a tuple for the clusters;
tupleCluster = list(zip(noCluster, sizeCluster, timestampCluster))

# Sort the cluster tuples according to its cluster size, from largest to smallest;
sorted_tupleCluster = sorted(
    tupleCluster, key=lambda cluster: cluster[1], reverse=True)

# The ratio of number considered;
ratio = 1.0
upperLimit = ratio * totCount

print((upperLimit, totCount))
print(sorted_tupleCluster)
time.sleep(1)

# Print the cluters accumulated to a certain ratio of the total amount;
accuCount = 0

# Unzip the cluster tuple;
sorted_noCluster, sorted_sizeCluster, sorted_timestampCluster = list(
    zip(*sorted_tupleCluster))

listLength = len(sorted_noCluster)

for i in my_lt_range(0, listLength, 1):

    accuCount += sorted_sizeCluster[i]

    # If the accumulated sizes of cluster is less than the upperlimit, we select it;
    if accuCount <= upperLimit:
        # We just need rough picosecond integer time stamp;
        timeStamp = int(sorted_timestampCluster[i])
        # Output the corresponding central pdb of that cluster;
        subprocess.call("echo 0 | /home/xl23/bin/mpigmx463-v5.0-plu/bin/trjconv -s nativeHeavy.pdb -f lowtemp.xtc -o clustersize." +
                        str(sorted_sizeCluster[i]) + ".t." + str(timeStamp) + ".pdb -dump " + str(timeStamp), shell=True)
