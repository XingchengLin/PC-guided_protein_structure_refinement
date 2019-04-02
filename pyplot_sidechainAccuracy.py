import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Change axis font size;
plt.rcParams.update({'font.size': 20})
from matplotlib.font_manager import FontProperties
font = FontProperties()
font.set_family('sans-serif')

# Set figure size;
scwrlDir = '.'
#modellerDir = '../../modeller/rotamer'

fig = plt.figure(1, figsize=(20.0, 10.0))

scwrlAccuracyX1 = np.loadtxt(scwrlDir + '/aveAccuracyX1.txt')
scwrlAccuracyX2 = np.loadtxt(scwrlDir + '/aveAccuracyX2.txt')
#modellerAccuracyX1 = np.loadtxt(modellerDir + '/aveAccuracyX1.txt')
#modellerAccuracyX2 = np.loadtxt(modellerDir + '/aveAccuracyX2.txt')

plt.subplot(1, 2, 1)

#plt.plot(scwrlAccuracyX1[:,0], scwrlAccuracyX1[:,1], 'k-', label='X1');
plt.errorbar(scwrlAccuracyX1[:, 0], scwrlAccuracyX1[:,
                                                    1], yerr=scwrlAccuracyX1[:, 2], label='X1')
#plt.plot(scwrlAccuracyX2[:,0], scwrlAccuracyX2[:,1], 'r-', label='X2');
plt.errorbar(scwrlAccuracyX2[:, 0], scwrlAccuracyX2[:,
                                                    1], yerr=scwrlAccuracyX2[:, 2], label='X2')
plt.legend(loc='lower right')
#plt.xlim([0, 21]);
plt.ylim([0.0, 1.0])
plt.xlabel('Time (ns)', fontsize=23)
plt.ylabel('Percentage within 40 degrees of native structure', fontsize=23)
plt.title('SCWRL')
# plt.grid(True);

#plt.subplot(1, 2, 2)
#
##plt.plot(modellerAccuracyX1[:,0], modellerAccuracyX1[:,1], 'k-', label='X1');
# plt.errorbar(modellerAccuracyX1[:, 0], modellerAccuracyX1[:,
#                                                          1], yerr=modellerAccuracyX1[:, 2], label='X1')
##plt.plot(modellerAccuracyX2[:,0], modellerAccuracyX2[:,1], 'r-', label='X2');
# plt.errorbar(modellerAccuracyX2[:, 0], modellerAccuracyX2[:,
#                                                          1], yerr=modellerAccuracyX2[:, 2], label='X2')
#plt.legend(loc='lower right')
##plt.xlim([0, 21]);
#plt.ylim([0.0, 1.0])
#plt.xlabel('Time (ns)', fontsize=23)
#plt.ylabel('Percentage within 40 degrees of native structure', fontsize=23)
# plt.title('Modeller')
# plt.grid(True);


plt.savefig('figure/Side-chain_Accuracy_Time.buried.pdf')
# plt.savefig('figure/Side-chain_Accuracy_Time.exposed.pdf')
plt.show()
