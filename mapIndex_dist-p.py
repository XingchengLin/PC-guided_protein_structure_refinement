##############################################################
# This script will help map heavy atom index from SMOG to
# Gromacs all-atom index and change the GDD.cont chopped from
# SMOG .top file;
# Before executing it, we need to modify .gro file such that
# the resid and resname column are separated and both of them
# contain a chain id column as their 3rd column, and get rid
# of the first long verbal line; Also note the cap residues have
# been deleted in SMOG file (The reason is I don't want these
# residues affecting the original contacts in post-fusion file), but
# the processed.gro *can* have these cap residues;
#
# Here we just convert the contacts from residue 54 to 76 (The
# non-harmonic constraint ones);

# Written by Xingcheng Lin, 12/18/3014
##############################################################

import math
import sys

################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step
###########################################


def mapIndex_dist(origIDFile, targetIDFile, residOffset, inputFile, outputFile):

    dict = {}

    # Loop through all ZE files;

    infile1 = open(origIDFile, 'r')
    infile2 = open(targetIDFile, 'r')

    outfile1 = open('calphaAtomid.dat', 'w')

    lines1 = [line.strip() for line in infile1]
    lines2 = [line.strip() for line in infile2]

    infile1.close()
    infile2.close()

    length1 = len(lines1)
    length2 = len(lines2)

    for i in my_lt_range(0, length1, 1):

        line1 = lines1[i].split()

        # Check in the second file if it is in the line we want;
        try:
            line1[7]
        except:
            print("It is the (; trash ;) line of .gro file")
        else:
            # We select the entire protein;
            if (1 == 1):
                for j in my_lt_range(0, length2, 1):
                    line2 = lines2[j].split()

                    try:
                        line2[7]
                    except:
                        print("It is the (; trash ;) line of .gro file")
                    else:
                        # Check if the atom matches, need to separate according to the chain IDs;
                        if (line1[2] == 'A') and ((int(line1[0]) + residOffset) == int(line2[0])) and (line1[2] == line2[2]) and (line1[3] == line2[3]):
                            # Record the heavy atom useful atom index in
                            # SBM .gro file;
                            outfile1.write(line1[4] + "\n")
                            # add the key to python dictionary;
                            dict[line1[4]] = line2[4]

    outfile1.close()

    # Based on the record above, change the dihedral.dat file;
    infile3 = open(inputFile, 'r')
    infile4 = open('calphaAtomid.dat', 'r')

    outfile2 = open(outputFile, 'w')

    lines3 = [line.strip() for line in infile3]
    lines4 = [line.strip() for line in infile4]
    infile3.close()
    infile4.close()

    length3 = len(lines3)
    length4 = len(lines4)

    for i in my_lt_range(0, length3, 1):
        line3 = lines3[i].split()
        # check if the index of atoms are recorded in the calphaAtomid.dat file;
        # Because we only selected some domains of the molecule for converting these indices,
        # we don't want to output every one of previous contact pairs;
        # reset the checkflag for every line of dihedral.dat;
        checkflag = 0

        for j in my_lt_range(0, length4, 1):
            line4 = lines4[j].split()
            if (line4[0] == line3[0]):
                checkflag += 1
            elif (line4[0] == line3[1]):
                checkflag += 1
            else:
                continue

        # If the flag number is 2, we got all the flags needed, then we can
        # proceed to the next level, which is to use dictionary and remap the
        # dihedral interaction into new file with new index;
        if checkflag == 2:
            outfile2.write(dict[line3[0]] + "\t" +
                           dict[line3[1]] + "\t" + line3[2] + "\t" + line3[3] + "\n")

    outfile2.close()

    return


############################################################################

if __name__ == "__main__":
    origIDFile = sys.argv[1]
    targetIDFile = sys.argv[2]
    # Offset of residue ID between calphaAtom.gro and processed.gro;
    residOffset = int(sys.argv[3])

    inputFile = sys.argv[4]
    outputFile = sys.argv[5]

    mapIndex_dist(origIDFile, targetIDFile, residOffset, inputFile, outputFile)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
