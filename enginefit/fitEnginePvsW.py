import pandas as pd 
import numpy as np 
from numpy import logspace, log, log10, amin, amax
import matplotlib.pyplot as plt
from gpfit.fit import fit

# SOURCE OF DATA: http://media.aero.und.edu/uasresearch.org/documents/195-197_Reference-Section_Engines.pdf

df = pd.read_csv('powervsweight.csv')

P = df[u'37000'];
minP = amin(P)
maxP = amax(P)
logP = log(P/maxP)
#indP0 = np.array(np.argpartition(logP, -2)[-2:])
indP0 = []

W = df[u'33.2'];
minW = amin(W)
maxW = amax(W)
logW = log(W/maxW)
#indW0 = np.array([logW.argmax()])
indW0 = []


indices = np.delete(np.linspace(0,len(logP)-1,len(logP)),
	np.concatenate([indP0,indW0]))
logPin = np.array(logP[indices])
logWin = np.array(logW[indices])

Type = 'SMA'
K = 2

cstrt, rms_error = fit(logPin,logWin,K,Type)

#Result for K=1: w**0.1 = 0.984118 * (u_1)**0.117039
# rms_error 0.412

#Result for K=2: w**1.92 = 0.00441 * (u_1)**0.759
#           + 1.44 * (u_1)**2.90
# rms_error 0.346


# Plotting data
plt.plot(P[indices]/1000,W[indices],'r*',label='Data')
Pplot = np.linspace(1,150000,100)
plt.plot(Pplot/1000,maxW*(0.984118 * (Pplot/maxP)**0.117039)**10,label='K=1')
plt.plot(Pplot/1000, maxW*(0.00441* (Pplot/maxP)**0.759 +
                           1.44* (Pplot/maxP)**2.90)**(1/1.92),label='K=2')
plt.xlabel('Mean sea level maximum power (kW)')
plt.ylabel('Engine weight (lbs)')
plt.grid(True)
plt.legend(loc=2)
plt.show()
