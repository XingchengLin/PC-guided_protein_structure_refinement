####################################################################################
# This script will help fit the experimental data to a spline curve and output
# The derivative
#
# Input: experimental data file;
#
# Written by Xingcheng Lin,07/12/2018
####################################################################################

import math
import subprocess
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


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


def fitSpline(dataFile, yColn, outputFile):

    data=np.loadtxt(dataFile)
    x_origin=data[:,0].round(decimals=3)
    y=data[:,yColn].round(decimals=3)


    spl=UnivariateSpline(x_origin,y,k=5,s=0)
    
    # Extrapolate the x and y until -1 and 2;
    x = x_origin
#    while (x[0] > -0.2):
#        x = np.insert(x, 0, x[0]-(x[1]-x[0]));
#        
#    while (x[-1] < 1.2):
#        x = np.append(x, x[-1]+(x[-1]-x[-2]));
    
    dy = np.diff(spl(x))/ np.diff(x)
    # Because dy is one elment shorter than y;

    x2 = (x[:-1] + x[1:])/2    
    y2 = spl(x2)

    # Insert a boundary condition (free energy 1000 kJ/mol), because we don't want the biased simulation go out of the "wall";
    x2 = np.insert(x2, 0, x2[0]-(x2[1]-x2[0]));
    y2 = np.insert(y2, 0, 1000)
    dy = np.insert(dy, 0, (y2[1]-y2[0])/(x2[1]-x2[0]))
    x2 = np.append(x2, x2[-1]+(x2[-1]-x2[-2]));
    y2 = np.append(y2, 1000)
    dy = np.append(dy, (y2[-1]-y2[-2])/(x2[-1]-x2[-2]))

    x2 = np.round(x2, decimals=3)
    y2 = np.round(y2, decimals=3)
    dy = np.round(dy, decimals=3)

    print(np.shape(dy))
    print (np.shape(x2))
    print (np.shape(y2))
    
    plt.plot(x_origin, y)
    plt.plot(x2,y2)
    plt.plot(x2, dy)
#    plt.show()
    
    length = np.shape(x2)[0];
    
    outfile = open(outputFile, 'w');
    
    for i in my_lt_range(0, length, 1):
        outfile.write(str(x2[i]) + "\t" + str(y2[i]) + "\t" + str(dy[i]) + "\n");
    
    return

############################################################################


if __name__ == "__main__":

    dataFile = sys.argv[1]
    # Column of data for the y value;
    yColn = int(sys.argv[2])
    
    # output file for both the experimental and fitted data;
    outputFile = sys.argv[3]


    fitSpline(dataFile, yColn, outputFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
