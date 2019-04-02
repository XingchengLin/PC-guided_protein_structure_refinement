import numpy as np
import matplotlib.pyplot as plt
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


def pyplot_QWvRW(pearCoeff, scoreName):

    # Change axis font size;
    plt.rcParams.update({'font.size': 20})
    from matplotlib.font_manager import FontProperties
    font = FontProperties()
    font.set_family('sans-serif')

    # Set figure size;
    fig = plt.figure(figsize=(20.0, 10.0))

    qrData = np.loadtxt('Qw_Rw.txt')
    xdata = qrData[:, 0]
    ydata = qrData[:, 1]
    plt.scatter(xdata, ydata, c='k')
    plt.xlabel('Qw', fontsize=23)
    plt.ylabel('Score Potential', fontsize=23)
    plt.title('Qw and Score Correlation', fontsize=23)
    plt.text((np.amax(xdata) - 0.1), np.amax(ydata),
             'Pearson Coeff=' + str(pearCoeff), fontsize=23)

    qrData = np.loadtxt(scoreName + '.selStructure/Qw_Rw.txt')
    xdata = qrData[:, 0]
    ydata = qrData[:, 1]
    plt.scatter(xdata, ydata, c='r')

    qrData = np.loadtxt(scoreName + '.selStructure/Qw_Rw.start.txt')
    xdata = qrData[0]
    ydata = qrData[1]
    plt.scatter(xdata, ydata, s=150, c='b', marker='s')

    plt.savefig('figure/Qw_Score.png')
    plt.show()
    #
    return

############################################################################


if __name__ == "__main__":

    inputFile = sys.argv[1]
    from calPearson import calPearson
    res = calPearson(inputFile)

    pearCoeff = "{:.3f}".format(float(res[0]))

    scoreName = sys.argv[2]

    pyplot_QWvRW(pearCoeff, scoreName)
    print("When the voice of the Silent touches my words,")
    print("I know him and therefore know myself.")
