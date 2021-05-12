#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter import filedialog as fd
import os
import math


# In[9]:


#User defined constants for the program
crystalline_layers = 1
amorphous_layers = 3
totalLayers = crystalline_layers + amorphous_layers
rdf_region = "amorphous"
rdf_cutoff = 8.0 #angstroms
x_boundary = "periodic"
y_boundary = "periodic"
z_boundary = "fixed"

#histogram parameters
nbins = 60
binbottom = 1.5
bintop = rdf_cutoff
binwidth = (bintop-binbottom)/nbins

#initialize variables that will be used
iterator = 0
nAtoms = 0
xSize = 0
ySize = 0
zSize = 0
zBoxSize = 0
z_lower_boundary = 0.0
z_upper_boundary = 0.0
atomicInformationDict = {}
atomicLocations = []


# In[10]:


#Load tkinter and read in the user chosen file
root = Tk()
file = fd.askopenfilename(title = "Choose the a-Si/c-Si interface xyz file")
root.withdraw()
f = open(file, 'r')
for line in f:
    #if iterator == 3:
    #    nAtoms = float(line)
    if iterator == 5:
        newline = line.split()
        xSize = float(newline[1]) - float(newline[0])
    if iterator == 6:
        newline = line.split()
        ySize = float(newline[1]) - float(newline[0])
    if iterator == 7:
        newline = line.split()
        zSize = float(newline[1]) - float(newline[0])
        
        #Set z_boundaries to distinguish between layers
        if rdf_region == "amorphous":
            z_lower_bound = (crystalline_layers+0.5)*zSize/totalLayers
            z_upper_bound = (totalLayers-0.5)*zSize/totalLayers
        elif rdf_region == "interface":
            z_lower_bound = (crystalline_layers-0.5)*zSize/totalLayers
            z_upper_bound = (crystalline_layers + 0.5)*zSize/totalLayers
        elif rdf_region == "crystalline":
            z_lower_bound = 0.0
            z_upper_bound = (crystalline_layers - 0.5)*zSize/totalLayers
            
    elif iterator >= 9:
        newline = line.split()
        floatline = [float(i) for i in newline]
        atomicInformationDict[floatline[0]] = [floatline[1], floatline[2:]]
        if z_lower_bound <= floatline[4]*zSize and floatline[4]*zSize<=z_upper_bound:
            unscaledCoordinates = [floatline[2]*xSize, floatline[3]*ySize, floatline[4]*zSize]
            atomicLocations.append(unscaledCoordinates)
            nAtoms += 1
    iterator += 1

#make an array of all the atoms
atomicArray = np.array(atomicLocations)

#set the box size in the z direction
if z_boundary == "periodic":
    zBoxSize = zSize
else:
    zBoxSize = z_upper_bound - z_lower_bound

#prepare the histogram corrections due to ideal gas
numberDensity = nAtoms/(xSize*ySize*zBoxSize)
binBottomEdges = np.arange(binbottom, bintop, binwidth)
idealGasRDF = numberDensity*4*math.pi*np.square(binBottomEdges)*binwidth

#calculate the distance between every atomic pair, if all non-periodic boundary conditions
#for i in range(atomicArray.shape[0] - 1):
#    distances.extend(np.linalg.norm(atomicArray[i+1:,:] - atomicArray[i,:], axis=1))
totalCount = np.zeros(nbins)
for n, i in enumerate(atomicArray[:-1]):
    ndistances = []
    for j in np.concatenate((atomicArray[:n], atomicArray[n+1:]), axis=0):
        #print(i)
        #print(j)
        if x_boundary == "periodic":
            xDistance = min(abs(i[0]-j[0]),abs(min(i[0],j[0]) - max(i[0], j[0]) + xSize))
        else:
            xDistance = abs(i[0] - j[0])
            
        if y_boundary == "periodic":
            yDistance = min(abs(i[1]-j[1]),abs(min(i[1],j[1]) - max(i[1], j[1]) + ySize))
        else:
            yDistance = abs(i[1] - j[1])
            
        if z_boundary == "periodic":
            zDistance = min(abs(i[2]-j[2]),abs(min(i[2],j[2]) - max(i[2], j[2]) + zSize))
        else:
            zDistance = abs(i[2] - j[2])
        
        distance = math.sqrt(xDistance**2 + yDistance**2 + zDistance**2)
        if distance < rdf_cutoff:
            ndistances.append(distance)
      
    ndistancearray = np.asarray(ndistances)
    count, bins = np.histogram(ndistancearray, nbins, (binbottom, bintop))
    
    if z_boundary != "periodic":
        #correction due to the fact that the rdf sphere extends beyond the simulation box
        zElevation = min(i[2] - z_lower_bound, z_upper_bound - i[2])
        sphericalCaps = np.maximum(np.zeros(binBottomEdges.size), binBottomEdges-zElevation)
        idealGasRDF = numberDensity*binwidth*(4*math.pi*np.square(binBottomEdges) - 2*math.pi*binBottomEdges*sphericalCaps)
    else:
        #no correction needed, due to periodic boundary conditions
        idealGasRDF = numberDensity*binwidth*(4*math.pi*np.square(binBottomEdges))
    
    count = np.divide(count, nAtoms*idealGasRDF)
    totalCount += count

#plot the rdf
plt.plot(binBottomEdges, totalCount, 'b-')
plt.ylabel("$g(r)$")
plt.xlabel("r($\AA$)")
plt.show()

