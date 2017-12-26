from SimPleAC_mission4 import Mission
from gpkit import Model, units, Vectorize, Variable
from gpkit import GPCOLORS, GPBLU
from gpkit.constraints.bounded import Bounded
from matplotlib import pyplot as plt
import numpy as np

m = Mission(5)
N = 8
M = 8
m.cost = m['W_f'] * units('1/N') + m['Cost Index'] * m['t_m']


# Setting sweep substitutions
Range = np.linspace(1000,5000,N)
W_p = np.linspace(1000,10000,M)
m.substitutions.update({'Range':('sweep',Range),
                         'W_p'  :('sweep',W_p)})

# Solving
sol = m.localsolve(verbosity=2,skipsweepfailures=True)
#sol = m.autosweep({m['Range']:(1000,5000),
#                   m['W_p']:(1000,10000)})

# Plotting
Vffuse = sol('V_{f_{fuse}}').reshape((N,M))
Vfwing = sol('V_{f_{wing}}').reshape((N,M))
Vftotal = sol('V_{f_{avail}}').reshape((N,M))
Vf = sol('V_f').reshape((N,M))
W_p = sol('W_p').reshape((N,M))
W_f = sol('W_f').reshape((N,M))
Range = sol('Range').reshape((N,M))
W = sol('W').reshape((N,M))
AR = sol('A').reshape((N,M))

# Fuel weight contours
plt.contour(W_p,Range,W_f)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Fuel weight contours (N)')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Wfcontours.png')
plt.close()

# Total weight contours
plt.contour(W_p,Range,W)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Total weight contours (N)')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Wcontours.png')
plt.close()

# Fuselage fuel fraction contours
plt.contour(W_p,Range,Vffuse/Vftotal)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Fuselage fuel fraction contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/vffusefraccontours.png')
plt.close()

# Excess wing volume contours
plt.contour(W_p,Range,Vfwing/Vftotal)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Wing fuel fraction contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/vfwingfraccontours.png')
plt.close()

# Wing weight sensitivity contours
Wwcoeff1sens = sol['sensitivities']['constants']['W_{w_{coeff1}}'].reshape((N,M))
Wwcoeff2sens = sol['sensitivities']['constants']['W_{w_{coeff2}}'].reshape((N,M))

plt.contour(W_p,Range,Wwcoeff1sens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$W_{w_{\mathrm{coeff1}}}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Wwcoeff1senscontours.png')
plt.close()

plt.contour(W_p,Range,Wwcoeff2sens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$W_{w_{\mathrm{coeff2}}}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Wwcoeff2senscontours.png')
plt.close()

# Engine weight sensitivity contours
W_e_refsens = sol['sensitivities']['constants']['W_{e,ref}'].reshape((N,M))
plt.contour(W_p,Range,W_e_refsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Engine weight sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Wesenscontours.png')
plt.close()

# Max lift coefficient sensitivity contours
CLmaxsens = sol['sensitivities']['constants']['C_{L,max}'].reshape((N,M))
plt.contour(W_p,Range,CLmaxsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$C_{L,max}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/CLmaxsenscontours.png')
plt.close()

# Cruise altitude sensitivity contours
h_cruisesens = sol['sensitivities']['constants']['h_{cruise}'].reshape((N,M))
plt.contour(W_p,Range,h_cruisesens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Cruise altitude sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/hcruisesenscontours.png')
plt.close()

# Min velocity sensitivity contours
Vminsens = sol['sensitivities']['constants']['V_{min}'].reshape((N,M))
plt.contour(W_p,Range,Vminsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$V_{min}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Vminsenscontours.png')
plt.close()
