import pandas as pd 
import numpy as np 
from numpy import logspace, log, log10
import matplotlib.pyplot as plt
from gpfit.fit import fit

# This maps (1-Power Lapse %) to altitude

df = pd.read_csv('DF35_maxPvh.csv')

h = np.array(df['ft']/15000)
#h = np.delete(h,[0])
P = np.array(df['kW'])
#P = np.delete(P,[0])

P_MSL = np.amax(df['kW'])

Pnorm = P/P_MSL

L = 1-Pnorm

# the variables you input into fit() can't have negatives here or Inf or -Inf
logL = log(L)
logh = log(h)

plt.plot(logL,logh)
plt.xlabel('log(h)')
plt.ylabel('log(1-Pnorm)')
#plt.show()

K = 1
Type = 'SMA'

cstrt, rms_error = fit(logh[1:-1],logL[1:-1],K,Type)

# Doing the power curve fit

# RPM = df['RPM'] #RPM
# P = df['P'] #kW
# BSFC = df['BSFC'] #kg/kWhr
#
# RPM = RPM[0:6]
# P = P[0:6]
# BSFC = BSFC[0:6]
#
# BSFCmin = min(BSFC)
# RPMmax = max(RPM)
# Pmax = max(P)
#
# BSFC = BSFC/BSFCmin
# RPM = RPM/RPMmax
# P = P/Pmax


# cstrt, rms_error = fit(log(RPM),log(P),K,Type)


