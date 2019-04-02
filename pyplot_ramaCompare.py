import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Change axis font size;
plt.rcParams.update({'font.size': 20})
from matplotlib.font_manager import FontProperties
font = FontProperties()
font.set_family('sans-serif')

# Set figure size;
fig1 = plt.figure(1, figsize=(20.0, 10.0))

scwrlDir = '.'
modellerDir = '../../modeller/rotamer'


scwrlDiheFreqX1 = np.loadtxt(scwrlDir + '/diheFreqX1.txt')
modellerDiheFreqX1 = np.loadtxt(modellerDir + '/diheFreqX1.txt')
scwrlDiheFreqX2 = np.loadtxt(scwrlDir + '/diheFreqX2.txt')
modellerDiheFreqX2 = np.loadtxt(modellerDir + '/diheFreqX2.txt')

resid = scwrlDiheFreqX1[:, 0]
scwrlAccuracyX1 = scwrlDiheFreqX1[:, 1]
modellerAccuracyX1 = modellerDiheFreqX1[:, 1]
scwrlAccuracyX2 = scwrlDiheFreqX2[:, 1]
modellerAccuracyX2 = modellerDiheFreqX2[:, 1]
# Data from X1 & X2 share the same normalized sasa
scwrl_norm_sasa = scwrlDiheFreqX1[:, 2]
# Data from X1 & X2 share the same normalized sasa
modeller_norm_sasa = modellerDiheFreqX1[:, 2]

#print (np.average(scwrlAccuracyX1), np.average(scwrlAccuracyX2), np.average(modellerAccuracyX1), np.average(modellerAccuracyX2));

plt.subplot(1, 2, 1)
plt.plot(resid, scwrlAccuracyX1 - modellerAccuracyX1,
         'ko', ms=5, label='Scwrl-Modeller')
plt.plot([0, resid[-1]], [np.average(scwrlAccuracyX1 - modellerAccuracyX1),
                          np.average(scwrlAccuracyX1 - modellerAccuracyX1)], 'k--')
plt.plot(resid, modellerAccuracyX1, 'ro', ms=5, label='Modeller', mfc=None)
plt.plot([0, resid[-1]], [np.average(modellerAccuracyX1),
                          np.average(modellerAccuracyX1)], 'r--')
plt.plot(resid, scwrlAccuracyX1, 'go', ms=5, label='Scwrl')
plt.plot([0, resid[-1]], [np.average(scwrlAccuracyX1),
                          np.average(scwrlAccuracyX1)], 'g--')
plt.legend(loc='lower right')
#plt.xlim([0, 21]);
#plt.ylim([0.3, 0.8]);
plt.xlabel('Residue Index', fontsize=23)
plt.ylabel('X1 Percentage within 40 degrees of native structure', fontsize=23)
# plt.grid(True);
plt.title('X1')

plt.subplot(1, 2, 2)
plt.plot(resid, scwrlAccuracyX2 - modellerAccuracyX2,
         'ko', ms=5, label='Scwrl-Modeller')
plt.plot([0, resid[-1]], [np.average(scwrlAccuracyX2 - modellerAccuracyX2),
                          np.average(scwrlAccuracyX2 - modellerAccuracyX2)], 'k--')
plt.plot(resid, modellerAccuracyX2, 'ro', ms=5, label='Modeller', mfc=None)
plt.plot([0, resid[-1]], [np.average(modellerAccuracyX2),
                          np.average(modellerAccuracyX2)], 'r--')
plt.plot(resid, scwrlAccuracyX2, 'go', ms=5, label='Scwrl')
plt.plot([0, resid[-1]], [np.average(scwrlAccuracyX2),
                          np.average(scwrlAccuracyX2)], 'g--')

plt.legend(loc='lower right')
#plt.xlim([0, 21]);
#plt.ylim([0.3, 0.8]);
plt.xlabel('Residue Index', fontsize=23)
plt.ylabel('X2 Percentage within 40 degrees of native structure', fontsize=23)
plt.title('X2')


#manager = plt.get_current_fig_manager()
# manager.window.showMaximized()


plt.savefig('figure/predictionCompare.pdf')
plt.show()

#plt.plot([1,2,3,4], [1,4,9,16], 'ro')
#plt.axis([0, 6, 0, 20])


# Plot the correlation between SASA and predictionFreq;
# Set figure size;
fig2 = plt.figure(2, figsize=(20.0, 10.0))

plt.subplot(1, 2, 1)

plt.plot(scwrl_norm_sasa, scwrlAccuracyX1, 'ko', ms=5)
# Calculate pearson correlation;
res = stats.pearsonr(scwrlAccuracyX1, scwrl_norm_sasa)
coeff = np.around(res[0], decimals=3)
fig2.text(0.35, 0.95, 'Pearson Coeff=' + str(coeff), fontsize=15)
# Calculate the product of sidechain accuracy weighted by sasa;
metric = np.around(
    np.sum(np.divide(scwrlAccuracyX1, scwrl_norm_sasa)), decimals=3)
fig2.text(0.35, 0.90, 'Metric =' + str(metric), fontsize=15)

plt.legend(loc='lower right')
#plt.xlim([0, 21]);
#plt.ylim([0.3, 0.8]);
plt.xlabel('Normalized SASA', fontsize=23)
plt.ylabel('X1 Percentage within 40 degrees of native structure', fontsize=23)
plt.title('SCWRL X1')
# plt.grid(True);

plt.subplot(1, 2, 2)

plt.plot(modeller_norm_sasa, modellerAccuracyX1, 'ko', ms=5)
# Calculate pearson correlation;
res = stats.pearsonr(modellerAccuracyX1, modeller_norm_sasa)
coeff = np.around(res[0], decimals=3)
fig2.text(0.80, 0.95, 'Pearson Coeff=' + str(coeff), fontsize=15)
# Calculate the product of sidechain accuracy weighted by sasa;
metric = np.around(
    np.sum(np.divide(modellerAccuracyX1, modeller_norm_sasa)), decimals=3)
fig2.text(0.80, 0.90, 'Metric =' + str(metric), fontsize=15)


plt.legend(loc='lower right')
#plt.xlim([0, 21]);
# plt.ylim([0.3, 0.8]);:24

plt.xlabel('Normalized SASA', fontsize=23)
plt.ylabel('X1 Percentage within 40 degrees of native structure', fontsize=23)
plt.title('Modeller X1')
# plt.grid(True);

plt.savefig('figure/X1sasa_vs_sidechain.pdf')
plt.show()

# Plot the correlation between SASA and predictionFreq;
# Set figure size;
fig3 = plt.figure(3, figsize=(20.0, 10.0))

plt.subplot(1, 2, 1)

plt.plot(scwrl_norm_sasa, scwrlAccuracyX2, 'ko', ms=5)
# Calculate pearson correlation;
res = stats.pearsonr(scwrlAccuracyX2, scwrl_norm_sasa)
coeff = np.around(res[0], decimals=3)
fig3.text(0.35, 0.95, 'Pearson Coeff=' + str(coeff), fontsize=15)
# Calculate the product of sidechain accuracy weighted by sasa;
metric = np.around(
    np.sum(np.divide(scwrlAccuracyX2, scwrl_norm_sasa)), decimals=3)
fig3.text(0.35, 0.90, 'Metric =' + str(metric), fontsize=15)

plt.legend(loc='lower right')
#plt.xlim([0, 21]);
#plt.ylim([0.3, 0.8]);
plt.xlabel('Normalized SASA', fontsize=23)
plt.ylabel('X2 Percentage within 40 degrees of native structure', fontsize=23)
plt.title('SCWRL X2')
# plt.grid(True);

plt.subplot(1, 2, 2)

plt.plot(modeller_norm_sasa, modellerAccuracyX2, 'ko', ms=5)
# Calculate pearson correlation;
res = stats.pearsonr(modellerAccuracyX2, modeller_norm_sasa)
coeff = np.around(res[0], decimals=3)
fig3.text(0.80, 0.95, 'Pearson Coeff=' + str(coeff), fontsize=15)
# Calculate the product of sidechain accuracy weighted by sasa;
metric = np.around(
    np.sum(np.divide(modellerAccuracyX2, modeller_norm_sasa)), decimals=3)
fig3.text(0.80, 0.90, 'Metric =' + str(metric), fontsize=15)


plt.legend(loc='lower right')
#plt.xlim([0, 21]);
# plt.ylim([0.3, 0.8]);:24

plt.xlabel('Normalized SASA', fontsize=23)
plt.ylabel('X2 Percentage within 40 degrees of native structure', fontsize=23)
plt.title('Modeller X2')
# plt.grid(True);

plt.savefig('figure/X2sasa_vs_sidechain.pdf')
plt.show()
