import pandas as pd
import numpy as np
from numpy import logspace, log, log10
import matplotlib.pyplot as plt
from gpfit.fit import fit


# Maps BSFC to throttle level

df = pd.read_csv('DF35_maxPvh.csv')

RPM = np.array(df['RPM'][0:6]) #RPM
P = np.array(df['P'][0:6]) #kW
BSFC = np.array(df['BSFC'][0:6]) #lb/(hp*hr)

Pmax = np.amax(P)
BSFCmin = np.amin(BSFC)

K=1
Type = 'SMA'
cstrt, rms_error = fit(log(P/Pmax),log(BSFC/BSFCmin),K,Type)

#newPoints = (0.992*(P/Pmax)**-0.0303)**10
