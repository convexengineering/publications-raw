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

# Enlarging fonts
SMALL_SIZE = 14
MEDIUM_SIZE = 18
BIGGER_SIZE = 18

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title

# Plotting data
plt.plot(P[indices]/1000,W[indices],'r*',label='Data')
Pplot = np.linspace(1,150000,100)
plt.plot(Pplot/1000,maxW*(0.984118 * (Pplot/maxP)**0.117039)**10,'k--',label='K=1')
plt.plot(Pplot/1000, maxW*(0.00441* (Pplot/maxP)**0.759 +
                           1.44* (Pplot/maxP)**2.90)**(1/1.92),'k',label='K=2')
plt.xlabel('Mean sea level maximum power (kW)')
plt.ylabel('Engine weight (lbs)')
plt.grid(True)
plt.legend(loc=2,fontsize=14)
plt.show()
