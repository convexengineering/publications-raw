from SimPleAC_mission2 import Mission
from gpkit import Model, units, Vectorize, Variable
from gpkit import GPCOLORS, GPBLU
from gpkit.constraints.bounded import Bounded
from plot_feasibilities import plot_feasibilities
from matplotlib import pyplot as plt
import numpy as np


# Simple model with monomial eq. and posynomial
x = Variable('x')
y = Variable('y')

constraints = []
constraints += [x + y <= 2,
                x*y <= 1./2.,
                #1 >= 10**-10/x,
                #1 >= 10**-10/y
                ]
m = Model(x,constraints)
sol = m.solve()

plt.figure(1)
plot_feasibilities(x,y,m)

# Subplots for x*y=1/2
# fig, axes = plt.subplots(2)
# xlin = np.linspace(0.2929,1.707)
# ylin = 0.5/xlin
# plt.figure(2)
# plt.subplot(212)
# line = plt.plot(xlin,ylin)
# plt.setp(line,color=GPBLU)
# plt.subplot(211)
# logline = plt.plot(np.log(xlin),np.log(ylin))
# plt.setp(logline,color=GPBLU)
# plt.suptitle('x vs y feasibility space')
# plt.show()



# m = Mission(5)
# m.cost = m['W_f'] * units('1/N') + m['Cost Index'] * m['t_m']
# sol = m.localsolve()
#
# substitutions = {'V_{f_{wing}}':sol('V_{f_{wing}}').magnitude*sol('V_{f_{wing}}').units,
#                  'V_{f_{avail}}':sol('V_{f_{avail}}').magnitude*sol('V_{f_{avail}}').units,
#                  'V_{f_{fuse}}':sol('V_{f_{fuse}}').magnitude*sol('V_{f_{fuse}}').units}
#
# mGP = m.as_gpconstr(None,substitutions)
# plot_feasibilities(mGP.variables_byname('W_{w_{coeff1}}'),mGP.variables_byname('W_{w_{coeff2}}'),mGP)


# Template code from Robust
# m = Model(D, constraints)
# m.solve()
# plot_feasibilities(W_w_coeff1, W_w_coeff2, m)
# W_w_coeff1.key.descr["pr"] = 66
# W_w_coeff2.key.descr["pr"] = 66
# RM = RobustModel(m, 'elliptical', two_term=False)
# RMsol = RM.robustsolve(verbosity=1)
# rm = RM.get_robust_model()
# plot_feasibilities(W_w_coeff1, W_w_coeff2, m, rm, "elliptical")
