import pandas as pd 
import numpy as np 
from numpy import logspace, log, log10, amin, amax
import matplotlib.pyplot as plt
# you have to change it to this and run the file form gpfit
from gpfit.fit import fit

# since this is not an installable code source you have to navigate to the
# ~gpfit folder.  

# SOURCE OF DATA: http://media.aero.und.edu/uasresearch.org/documents/195-197_Reference-Section_Engines.pdf

df = pd.read_csv('powervsweight.csv')

P = df[u'37000'];
minP = amin(P)
maxP = amax(P)
logP = log(P/maxP)
indP0 = np.array(np.argpartition(logP, -2)[-2:])

W = df[u'33.2'];
minW = amin(W)
maxW = amax(W)
logW = log(W/maxW)
indW0 = np.array([logW.argmax()])


indices = np.delete(np.linspace(0,len(logP)-1,len(logP)),
	np.concatenate([indP0,indW0]))
logPin = np.array(logP[indices])
logWin = np.array(logW[indices])

Type = 'SMA'
K = 2

cstrt, rms_error = fit(logPin,logWin,K,Type)
#Result: w**0.789 = 0.0336 * (u_1)**0.157
#           + 1.57 * (u_1)**1.34
# rms_error 0.346


# Plotting data
plt.plot(P[indices]/1000,W[indices],'r*') 
Pplot = np.linspace(1,150000,100)
plt.plot(Pplot/1000,(0.0336 * (Pplot/maxP)**0.157
    + 1.57 * (Pplot/maxP)**1.34)**(1/0.789)*maxW,'b-')
plt.xlabel('Mean sea level maximum power (kW)')
plt.ylabel('Engine weight (lbs)')
plt.grid(True)
plt.show()
