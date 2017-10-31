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
indP0 = logP.argmax()

W = df[u'33.2'];
minW = amin(W)
maxW = amax(W)
logW = log(W/maxW)
indW0 = logW.argmax()


indices = np.delete(np.linspace(0,len(logP)-1,len(logP)),[indP0,indW0])
logPin = np.array(logP[indices])
logWin = np.array(logW[indices])

Type = 'SMA'
K = 2

cstrt, rms_error = fit(logPin,logWin,K,Type)