####################################################################################
# This script will help fit the experimental data to Gaussian
#
# Input: experimental data file;
#
# Written by Xingcheng Lin, 03/28/2018
####################################################################################

import math
import subprocess
import os
import sys
import time
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


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


def fitCurve(dataFile, yColn, outputFile ):

    data = np.loadtxt(dataFile)

    # Define model function to be used to fit to the data above:
    def parabola(x, *p):
        k, mu = p
        return 0.5 * k * (x - mu)**2

    # The x value is the first column
    xValue = data[:, 0]
    # The y value is the second column
    yValue = data[:, yColn]

    # No need for Scaling caused by Jeff Wham code, b/c the k used will still be in the unit of kj/mol, same as here (if the free energy is)
    # in the unit of kT, then we do need to do the reversed scaling!
    #yValue = yValue / (300.0/120.2717)

    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    p0 = [1., 0.2]

    coeff, var_matrix = curve_fit(parabola, xValue, yValue, p0=p0)

    # Get the fitted curve
    yValue_fit = parabola(xValue, *coeff)

    plt.plot(xValue, yValue, label='experimental data')
    plt.plot(xValue, yValue_fit, label='fitted data')

    # Finally, lets get the fitting parameters, i.e. the mean and standard deviation:
    print('Fitted strength = ', coeff)

    plt.show()

    outfile = open(outputFile, 'w')

    length = np.shape(data)[0]

    for i in my_lt_range(0, length, 1):
        outfile.write(str(xValue[i]) + "\t" + str(yValue[i]) + "\t" + str(yValue_fit[i]) + "\n")
        


    return

############################################################################


if __name__ == "__main__":

    dataFile = sys.argv[1]
    # Column of data for the y value;
    yColn = int(sys.argv[2])
    
    # output file for both the experimental and fitted data;
    outputFile = sys.argv[3]


    fitCurve(dataFile, yColn, outputFile)

    print("Love is an endless mystery,")
    print("for it has nothing else to explain it.")
