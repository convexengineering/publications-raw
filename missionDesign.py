from SimPleAC_mission2 import Mission
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
# # W = np.linspace(2000,20000,N)
W_p = np.linspace(1000,10000,M)
m.substitutions.update({'Range':('sweep',Range),
                         'W_p'  :('sweep',W_p)})

# Solving
sol = m.localsolve(verbosity=2,skipsweepfailures=True)

# Plotting
Vffuse = sol('V_{f_{fuse}}').reshape((N,M))
Vfwing = sol('V_{f_{wing}}').reshape((N,M))
Vftotal = sol('V_f').reshape((N,M))
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
plt.show()

# Total weight contours
plt.contour(W_p,Range,W)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Total weight contours (N)')
plt.grid()
plt.colorbar()
plt.show()

# Fuselage fuel fraction contours
plt.contour(W_p,Range,Vffuse/Vftotal)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Fuselage fuel fraction contours')
plt.grid()
plt.colorbar()
plt.show()

# Wing weight sensitivity contours
Wwcoeff1sens = sol['sensitivities']['constants']['W_{w_{coeff1}}_Mission/SimPleAC.1/Wing'].reshape((N,M))
Wwcoeff2sens = sol['sensitivities']['constants']['W_{w_{coeff2}}_Mission/SimPleAC.1/Wing'].reshape((N,M))

plt.contour(W_p,Range,Wwcoeff1sens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$W_{w_{coeff1}}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.show()

plt.contour(W_p,Range,Wwcoeff2sens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$W_{w_{coeff2}}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.show()

# Engine weight sensitivity contours
W_e_refsens = sol['sensitivities']['constants']['W_{e,ref}'].reshape((N,M))
plt.contour(W_p,Range,W_e_refsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Engine weight sensitivity contours')
plt.grid()
plt.colorbar()
plt.show()

# Max lift coefficient sensitivity contours
CLmaxsens = sol['sensitivities']['constants']['C_{L,max}'].reshape((N,M))
plt.contour(W_p,Range,CLmaxsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('C_{L,max} sensitivity contours')
plt.grid()
plt.colorbar()
plt.show()

# Max lift coefficient sensitivity contours
CLmaxsens = sol['sensitivities']['constants']['C_{L,max}'].reshape((N,M))
plt.contour(W_p,Range,CLmaxsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('C_{L,max} sensitivity contours')
plt.grid()
plt.colorbar()
plt.show()

# Cruise altitude sensitivity contours
h_cruisesens = sol['sensitivities']['constants']['h_{cruise}'].reshape((N,M))
plt.contour(W_p,Range,h_cruisesens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Cruise altitude sensitivity contours')
plt.grid()
plt.colorbar()
plt.show()


