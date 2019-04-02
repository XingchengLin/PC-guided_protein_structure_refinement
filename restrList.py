###########################################################################
# This script will help construct a contact restraint list based on the
# sequence-alignment file;
#
# We only add into the list when the sequence index are separated by
# at least 3 residues;
#
# Input: Alignment file:
# The first line is the alignment for target;
# The second line is the alignment for template;
# The third line is for the target;
# The fourth line is for the template;
#
# Output: map file with 4 colns: target_res, target_resid, template_res, template_resid;
# Output: Distance file 3 colns: target_resid_i, target_resid_j, distance;
#
# Written by Xingcheng Lin, 02/23/2018;
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


from splitString import splitString


def restrList(alignmentFile, mapFile, PDBFile, distFile):

    infile_alignment = open(alignmentFile, 'r')
    outfile_map = open(mapFile, 'w')

    lines_alignment = [line.strip() for line in infile_alignment]
    infile_alignment.close()

    # The first line is the alignment for target;
    # The second line is the alignment for template;
    # The third line is for the target;
    # The fourth line is for the template;

    target_alignment = splitString(lines_alignment[0])
    template_alignment = splitString(lines_alignment[1])
    start_resid_target = lines_alignment[2].split()[0]
    start_resid_template = lines_alignment[3].split()[0]

    length_target_alignment = len(target_alignment)

    resid_target = int(start_resid_target)
    resid_template = int(start_resid_template)

    for i in my_lt_range(0, length_target_alignment, 1):

        # Only if both the target and template are not gap, the bias can work
        if (target_alignment[i] != '-' and template_alignment[i] != '-'):
            outfile_map.write(target_alignment[i] + "\t" + str(
                resid_target) + "\t" + template_alignment[i] + "\t" + str(resid_template) + "\n")

        # Update the resid;
        if (target_alignment[i] != '-'):
            resid_target += 1

        if (template_alignment[i] != '-'):
            resid_template += 1

    outfile_map.close()

    # Using the generated map file to generate the distance constraint reference file based on the existing residues in the template (output in target index);
    infile_map = open(mapFile, 'r')
    infile_PDB = open(PDBFile, 'r')
    outfile_dist = open(distFile, 'w')
    lines_map = [line.strip() for line in infile_map]
    lines_PDB = [line.strip() for line in infile_PDB]

    infile_map.close()
    infile_PDB.close()

    length_lines_map = len(lines_map)
    length_lines_PDB = len(lines_PDB)

    # Loop through to find proper residue pairs;

    coord_1 = [0, 0, 0]
    coord_2 = [0, 0, 0]

    # Flag to see if the residue is existing in the homolog structure;
    residExistedFlag = 0;


    for i in my_lt_range(0, length_lines_map, 1):

        line_map1 = lines_map[i].split()

        for j in my_lt_range(0, length_lines_map, 1):

            line_map2 = lines_map[j].split()

            if (int(line_map2[3]) - int(line_map1[3]) >= 3):

                # Read into the PDB to find distance;
                
                # To avoid the case where there are redundant atoms, we added a sanity check;
                # We try to make sure that if there is a case like "ATHR, BTHR" both exist, we will only take the coordinate of BTHR into the calculation
                # of dist.txt;
                recordedResid = 0;

                for k in my_lt_range(0, length_lines_PDB, 1):

                    line_PDB = lines_PDB[k].split()

                    # Test if the corresponding entry is a number;
                    try:
                        int(line_PDB[5])
                    except (IndexError, ValueError) as e:
                        continue
                    else:
                        if(int(line_PDB[5]) == int(line_map1[3]) and line_PDB[2] == 'CA'):

                            if (recordedResid != line_PDB[5]):

                                # Not redundant;

                                residExistedFlag += 1;
    
                                coord_1[0] = line_PDB[6]
                                coord_1[1] = line_PDB[7]
                                coord_1[2] = line_PDB[8]

                            else:

                                # Redundant;

                                residExistedFlag += 0;
    
                                coord_1[0] = line_PDB[6]
                                coord_1[1] = line_PDB[7]
                                coord_1[2] = line_PDB[8]

                            
                            recordedResid = line_PDB[5];

                        if(int(line_PDB[5]) == int(line_map2[3]) and line_PDB[2] == 'CA'):

                            if (recordedResid != line_PDB[5]):

                                # Not redundant;
                                residExistedFlag += 1;

                                coord_2[0] = line_PDB[6]
                                coord_2[1] = line_PDB[7]
                                coord_2[2] = line_PDB[8]
                            else:
                                # Redundant;
                                residExistedFlag += 0;

                                coord_2[0] = line_PDB[6]
                                coord_2[1] = line_PDB[7]
                                coord_2[2] = line_PDB[8]


                            recordedResid = line_PDB[5];

                # Only if both of the two residues of the pair existing in the crystal structure, can we have the distance between them;
                if (residExistedFlag == 2):

                    # Calculate the distance
                    distance = math.sqrt((float(coord_2[0]) - float(coord_1[0]))**2 + (float(
                        coord_2[1]) - float(coord_1[1]))**2 + (float(coord_2[2]) - float(coord_1[2]))**2)
    
                    # Output to distance file; Note we need the indices of target PDB instead of the template PDB
                    outfile_dist.write(
                        str(line_map1[1]) + "\t" + str(line_map2[1]) + "\t" + str(distance) + "\n")

                # Reset the flag;
                residExistedFlag = 0;

    outfile_dist.close()

    return


############################################################################

if __name__ == "__main__":

    alignmentFile = sys.argv[1]
    mapFile = sys.argv[2]
    PDBFile = sys.argv[3]
    distFile = sys.argv[4]

    restrList(alignmentFile, mapFile, PDBFile, distFile)

    print("Beauty is truth\' smile")
    print("when she beholds her own face in")
    print("a perfect mirror.")
