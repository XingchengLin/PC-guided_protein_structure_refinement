import os
import sys
import re
data = ''


def is_float(s):
    try:
        int(s)
        return "Truth"
    except:
        return "Flase"


print("*.py inputfile_name  outputfile_name CACA|CACB|CBCB probility(0-1)")
inputfile = sys.argv[1]
medianlist = sys.argv[3] + 'mediandist.dat'
outputfile = sys.argv[2]
prob = float(sys.argv[4])
with open(medianlist, 'r') as fopen:
    medians = fopen.readlines()
with open(inputfile, 'r') as fopen:
    # l1=next(fopen)
    # l2=next(fopen)
    # l3=next(fopen)
    # l4=next(fopen)
    # l5=next(fopen)
    lines = fopen.readlines()
N = 0
# for linex in linesx:
#   N+=1
# print linex
#   if N > 5:
#     lines+= linex
seq = ''
LINES = ''
# print lines
for line in lines:
  # print line
    N = N + 1
    if N > 5:
        # if is_float(line.split()[0]) == 'False':
        if line.count(' ') < 1:
            seq += line.split()[0]
#    print is_float(line.split()[0])
#    print seq
        elif line.count(' ') > 3:
            #     print seq
            #     print len(line)
            #     LINES += line
            # for LINE in LINES:
            LINE = line
#     print LINE
            if float(LINE.split()[4]) >= prob:
                index1 = LINE.split()[0]
                index2 = LINE.split()[1]
                symbol1 = seq[int(index1) - 1]
                symbol2 = seq[int(index2) - 1]
                probaility = LINE.split()[4]
                for median in medians:
                    if (median.split()[0] == symbol1 and median.split()[1] == symbol2) or (median.split()[0] == symbol2 and median.split()[1] == symbol1):
                        #              print("%s-%s %s-%s"%(median.split()[0],median.split()[1],symbol1,symbol2))
                        dist = median.split()[2]
                        break
                data_line = index1 + ' ' + index2 + ' ' + dist + ' ' + probaility + '\n'
                data += data_line
            else:
                break
with open(outputfile, 'w') as fwrite:
    fwrite.writelines(data)
print(seq)
