##############################################################
# This script will help calculate the distance between each atom
# pair of a given structure;
#
# According to the rule of Q_Wolynes, we only write down pairs with i<j-2;

# Written by Xingcheng Lin, 12/06/2016
##############################################################

import math
################################################


def my_lt_range(start, end, step):
    while start < end:
        yield start
        start += step


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
###########################################


infile = open('smog.gro', 'r')
outfile = open('dist.txt', 'w')

lines = [line.strip() for line in infile]
length = len(lines)


for i in my_lt_range(0, length, 1):
    line1 = lines[i].split()

    try:
        line1[5]
    except:
        print("it is a trash line")
    else:
        if (is_number(line1[5])):
            # Calculate and output pair distance, only write down pairs with i<j-2;
            for j in my_lt_range(i + 3, length, 1):
                line2 = lines[j].split()
                try:
                    line2[5]
                except:
                    print("it is also a trash line")
                else:
                    distance = math.sqrt((float(line1[3]) - float(line2[3]))**2 + (
                        float(line1[4]) - float(line2[4]))**2 + (float(line1[5]) - float(line2[5]))**2)

                    outfile.write(
                        str(line1[2]) + "\t" + str(line2[2]) + "\t" + str(distance) + "\n")

outfile.close()
