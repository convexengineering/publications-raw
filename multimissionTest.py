from gpkit import Model, Variable, SignomialsEnabled, SignomialEquality, VarKey, units,Vectorize
from gpkit.constraints.bounded import Bounded
from relaxed_constants import relaxed_constants, post_process

import numpy as np
import matplotlib.pyplot as plt

from SimPleAC_mission4 import Mission, SimPleAC
from atmosphere import Atmosphere

from SimPleAC_multimission import Multimission

Nmissions = 2
Nsegments = 5

m = Mission(SimPleAC(),5)
m.substitutions.update({
        'h_{cruise_m}'   :5000*units('m'),
        'Range_m'        :3000*units('km'),
        'W_{p_m}'        :6250*units('N'),
        'C_m'            :120*units('1/hr'),
        'V_{min_m}'      :25*units('m/s'),
        'T/O factor_m'   :2,
    })
m.cost = m['W_{f_m}']*units('1/N')
sol1 = m.localsolve(verbosity=2)

m.substitutions.update({
        'Range_m'        :2000*units('km'),
        'W_{p_m}'        :8000*units('N'),
        'C_m'            :360*units('1/hr'),
    })
m.cost = m['C_m']*m['t_m']
sol2 = m.localsolve(verbosity=2)


m = Multimission(Nmissions,Nsegments)
m.substitutions.update({
        'h_{cruise_{mm}}':[5000*units('m'), 5000*units('m')],
        'Range_{mm}'     :[3000*units('km'), 2000*units('km')],
        'W_{p_{mm}}'     :[6250*units('N'),   8000*units('N')],
        'C_{mm}'         :[120*units('1/hr'), 360*units('1/hr')],
    })

m.cost = (m.missions[0]['W_{f_m}']*units('1/N') + m.missions[1]['C_m']*m.missions[1]['t_m'])
sol3 = m.localsolve(verbosity = 2)
