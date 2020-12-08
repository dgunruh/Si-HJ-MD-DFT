#!/usr/bin/env python
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

nAtoms = 432
preblast_fileName = str(sys.argv[1])
postblast_fileName = str(sys.argv[2])
blastatoms_fileName = str(sys.argv[3])
directory = os.getcwd()

prefile = directory + "/" + preblast_fileName
postfile = directory + "/" + postblast_fileName
atomsfile = directory + "/" + blastatoms_fileName

lines = open(atomsfile).read().splitlines()
blastids = []
for n, line in enumerate(lines):
    if n >=1:
        newline = line.split()
        blastids.append(int(newline[0]))
print(blastids)
c_low = 0.7
c_high = 2.3
a_low = 2.8
a_high = 5.5
unitcellLength = 5.43


#Do the pre-blast processing first
referencePEtotal = 0.0
refAtoms = 0
amorphousPEs = {}
lines = open(prefile).read().splitlines()
for n, line in enumerate(lines):
    newline = line.split()
    if n >=9:
        #print(newline)
        if float(newline[3]) >= c_low*unitcellLength and float(newline[3]) <= c_high*unitcellLength:
            referencePEtotal += float(newline[4])
            refAtoms += 1
        elif float(newline[3]) >= a_low*unitcellLength and float(newline[3]) <= a_high*unitcellLength:
            amorphousPEs[int(newline[0])] = float(newline[4])
    if n >= 440:
        break

referencePEaverage = referencePEtotal/refAtoms
totalValue = 0
preblast = []
preblast_to_shift = []
for key, value in amorphousPEs.items():
    value -= referencePEaverage
    amorphousPEs[key] = value
    totalValue += value

    if key in blastids:
        preblast_to_shift.append([key, value])
        #preblast.append(value)
    else:
        preblast.append(value)
    #print("ID: " + str(key) + " -> Excess Energy (eV): {:.03f}".format(value))
preblast_averageValue = totalValue/len(amorphousPEs)

#Do the post-blast processing
referencePEtotal = 0.0
refAtoms = 0
amorphousPEs = {}
lines = open(postfile).read().splitlines()
for n, line in enumerate(lines):
    newline = line.split()
    if n >=9:
        #print(newline)
        if float(newline[3]) >= c_low*unitcellLength and float(newline[3]) <= c_high*unitcellLength:
            referencePEtotal += float(newline[4])
            refAtoms += 1
        elif float(newline[3]) >= a_low*unitcellLength and float(newline[3]) <= a_high*unitcellLength:
            amorphousPEs[int(newline[0])] = float(newline[4])
    if n >= 440:
        break

referencePEaverage = referencePEtotal/refAtoms
totalValue = 0
postblast = []
postblast_shifted = []
for key, value in amorphousPEs.items():
    value -= referencePEaverage
    amorphousPEs[key] = value
    totalValue += value
    if key in blastids:
        postblast_shifted.append([key, value])
    else:
        postblast.append(value)
    #print("ID: " + str(key) + " -> Excess Energy (eV): {:.03f}".format(value))
postblast_averageValue = totalValue/len(amorphousPEs)

print("Pre-blast excess energy: " + str(preblast_averageValue))
print("Post-blast excess energy: " + str(postblast_averageValue))

preblast_array = np.asarray(preblast)
postblast_array = np.asarray(postblast)

fig, (ax1, ax2) = plt.subplots(2,1, sharex = True, figsize = (6, 8))
fig.subplots_adjust(top = 0.98, bottom = 0.06, right = 0.97, hspace = 0.1)

#Make the pre-blast histogram, using the freedman-diaconis method
count, bins = np.histogram(preblast_array, 'fd')
countmax = np.amax(count)
centers = [(i + bins[n]/2) for n,i in enumerate(bins[1:])]
ax1.hist(preblast_array, bins = len(centers), color = 'steelblue', label = 'Pre-blast', ec = 'black')
ax1.set_ylabel("Count", fontsize = 12)
ax1.legend(loc = 'upper right',fontsize = 12)
textstring = r'$\bar \mu$ = {0:.3f}'.format(preblast_averageValue)
ax1.text(.25, countmax*.95, textstring, fontsize = 10, bbox = {'facecolor':'white','pad':2})
for n, i in enumerate(preblast_to_shift):
    ax1.axvline(x = i[1], linestyle = 'dotted')
    ax1.text(i[1]-.02, countmax/2.0 + n*(countmax/8.0), str(i[0]), fontsize = 8, bbox = {'facecolor':'white', 'pad':2})

#Make the post-blast histrogram, using the freedman-diaconis method
count, bins = np.histogram(postblast_array, 'fd')
countmax = np.amax(count)
centers = [(i + bins[n]/2) for n,i in enumerate(bins[1:])]
ax2.hist(postblast_array, bins = len(centers), color = 'firebrick', label = 'Post-blast', ec = 'black')
ax2.set_ylabel("Count", fontsize = 12)
ax2.legend(loc = 'upper right',fontsize = 12)
ax2.set_xlim(0, 1.3)
ax2.set_xlabel("Excess energy [eV]")
textstring = r'$\bar \mu$ = {0:.3f}'.format(postblast_averageValue)
ax2.text(.25, countmax*.95, textstring, fontsize = 10, bbox = {'facecolor':'white','pad':2})
for n, i in enumerate(postblast_shifted):
    ax2.axvline(x = i[1], linestyle = 'dotted')
    ax2.text(i[1]-.02, countmax/2.0 + n*(countmax/8.0), str(i[0]), fontsize = 8, bbox = {'facecolor':'white','pad':2})
fig.savefig('Pre-PostEnergySpectrum'+ blastatoms_fileName[-8:-4] + '.png', format = 'png', dpi=300)
