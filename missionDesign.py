from SimPleAC_mission4 import Mission,SimPleAC
from gpkit import Model, units, Vectorize, Variable
from gpkit import GPCOLORS, GPBLU
from gpkit.constraints.bounded import Bounded
from matplotlib import pyplot as plt
import numpy as np
from gpkit.small_scripts import *

N = 8
M = 8
Range = np.linspace(1000,5000,N)
W_p = np.linspace(1000,10000,M)
#Vmin = np.linspace(25,100,N)

m = Mission(SimPleAC(),4)
m.substitutions.update({
        'h_{cruise_m}'   :5000*units('m'),
        'Range_m'        :3000*units('km'),
        'W_{p_m}'        :6250*units('N'),
        'C_m'            :120*units('1/hr'),
        'V_{min_m}'      :25*units('m/s'),
        'T/O factor_m'   :2,
})
m.substitutions.update({'Range_m':('sweep',Range),
                         'W_{p_m}'  :('sweep',W_p)})
m.cost = m['W_{f_m}']*units('1/N') + m['C_m']*m['t_m']

# Solving
sol = m.localsolve(verbosity=2,skipsweepfailures=True)
#sol = m.autosweep({m['Range']:(1000,5000),
#                   m['W_p']:(1000,10000)})

# Plotting
Obj = sol['cost'].reshape((N,M))
timecost = (sol('C_m').magnitude*sol('t_m').magnitude).reshape((N,M))
Vffuse = sol('V_{f_{fuse}}').reshape((N,M))
Vfwing = sol('V_{f_{wing}}').reshape((N,M))
Vftotal = sol('V_{f_{avail}}').reshape((N,M))
W_e = sol('W_e').reshape((N,M))
Vf = sol('V_f').reshape((N,M))
W_p = sol('W_{p_m}').reshape((N,M))
W_f = sol('W_{f_m}').reshape((N,M))
Range = sol('Range_m').reshape((N,M))
W = sol('W').reshape((N,M))
AR = sol('A').reshape((N,M))
h_cruisesens = sol['sensitivities']['constants']['h_{cruise_m}'].reshape((N,M))
Csens = sol['sensitivities']['constants']['C_m'].reshape((N,M))
Vminsens = sol['sensitivities']['constants']['V_{min_m}'].reshape((N,M))
W_e_refsens = sol['sensitivities']['constants']['W_{e,ref}'].reshape((N,M))
Wwcoeff1sens = sol['sensitivities']['constants']['W_{w_{coeff1}}'].reshape((N,M))
Wwcoeff2sens = sol['sensitivities']['constants']['W_{w_{coeff2}}'].reshape((N,M))
rhofsens = sol['sensitivities']['constants']['\\rho_f'].reshape((N,M))
CLmaxsens = sol['sensitivities']['constants']['C_{L,max}'].reshape((N,M))

# Objective contours
plt.contour(W_p,Range,Obj)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Objective contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Objcontours.png')
plt.close()

# Time cost contours
plt.contour(W_p,Range,timecost)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Time cost contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/timecostcontours.png')
plt.close()

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

# Engine weight contours
plt.contour(W_p,Range,W_e)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Engine weight (N) contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/W_econtours.png')
plt.close()

# Engine weight sensitivity contours
plt.contour(W_p,Range,W_e_refsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Engine weight sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Wesenscontours.png')
plt.close()

# Max lift coefficient sensitivity contours
plt.contour(W_p,Range,CLmaxsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$C_{L,max}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/CLmaxsenscontours.png')
plt.close()

# Cruise altitude sensitivity contours
plt.contour(W_p,Range,h_cruisesens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Cruise altitude sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/hcruisesenscontours.png')
plt.close()

# Min velocity sensitivity contours
plt.contour(W_p,Range,Vminsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('$V_{min}$ sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Vminsenscontours.png')
plt.close()

# Cost index sensitivity contours
plt.contour(W_p,Range,Csens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Cost index sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/Csenscontours.png')
plt.close()

# Fuel weight sensitivity contours
plt.contour(W_p,Range,rhofsens)
plt.xlabel('Payload weight (N)')
plt.ylabel('Range (km)')
plt.title('Fuel weight sensitivity contours')
plt.grid()
plt.colorbar()
plt.savefig('figbank/rhofsenscontours.png')
plt.close()
