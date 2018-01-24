import pandas as pd
import numpy as np
from numpy import logspace, log, log10
import matplotlib.pyplot as plt
from gpfit.fit import fit
from scipy.interpolate import spline



# Maps BSFC to throttle level

df = pd.read_csv('DF35_maxPvh.csv')

RPM = np.array(df['RPM'][0:6]) #RPM
P = np.array(df['P'][0:6]) #kW
BSFC = np.array(df['BSFC'][0:6]) #lb/(hp*hr)

Pmax = np.amax(P)
BSFCmin = np.amin(BSFC)

L = 1- P/Pmax
K=2
Type = 'SMA'
#cstrt, rms_error = fit(log(L[0:-1]),log(BSFC[0:-1]/BSFCmin),K,Type)
cstrt, rms_error = fit(log(P[0:-1]/Pmax),log(BSFC[0:-1]/BSFCmin),K,Type)

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

# Plotting
Lnew = np.linspace(0.1,1,100)
#newPoints = (6.57*(Lnew)**6.60 + 1.14 * (Lnew) ** 0.106)**(1/2.29)
#newPoints = (0.992*(Lnew)**-0.0303)**10
#newPoints = (2670*(Lnew)**32.7 + 0.925*(Lnew)**-0.140)**(1/0.373)
newPoints = (.984*Lnew**-0.0346)**10
newPoints2 = (.984*Lnew**-0.0346)**10
for i in range(0,100):
    if newPoints2[i] <= 1.:
        newPoints2[i] = 1.
#plt.plot(L,BSFC/BSFCmin,label='data')
plt.plot(P/Pmax,BSFC/BSFCmin,'k',label='data',marker='o')
plt.plot(Lnew,newPoints,'k--',label='fit')
plt.plot(Lnew,newPoints2,'k',label='fit+bound')
plt.xlabel('$P_{shaft}/P_{shaft,alt}$')
plt.ylabel('$BSFC/BSFC_{min}$')
plt.legend(loc=1)
plt.grid()
plt.show()

