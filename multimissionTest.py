from gpkit import Model, Variable, SignomialsEnabled, SignomialEquality, VarKey, units,Vectorize
from gpkit.constraints.bounded import Bounded
from relaxed_constants import relaxed_constants, post_process
from gpkit.small_scripts import *

import numpy as np
import matplotlib.pyplot as plt

from SimPleAC_mission4 import Mission, SimPleAC
from atmosphere import Atmosphere

from SimPleAC_multimission import Multimission

Nmissions = 2
Nsegments = 4

m = Multimission(SimPleAC(),1,Nsegments)
m.substitutions.update({
        'h_{cruise_{mm}}':5000*units('m'),
        'Range_{mm}'     :3000*units('km'),
        'W_{p_{mm}}'     :6250*units('N'),
        'C_{mm}'         :120*units('1/hr'),
    })
m.cost = m['W_{f_m}']*units('1/N')
sol1 = m.localsolve(verbosity=2)

m = Multimission(SimPleAC(),1,Nsegments)
m.substitutions.update({
        'h_{cruise_{mm}}':5000*units('m'),
        'Range_{mm}'     :2000*units('km'),
        'W_{p_{mm}}'     :8000*units('N'),
        'C_{mm}'         :360*units('1/hr'),
    })
m.cost = m['C_m']*m['t_m']
sol2 = m.localsolve(verbosity=2)


m = Multimission(SimPleAC(),2,Nsegments)
m.substitutions.update({
        'h_{cruise_{mm}}':[5000*units('m'), 5000*units('m')],
        'Range_{mm}'     :[3000*units('km'), 2000*units('km')],
        'W_{p_{mm}}'     :[6250*units('N'),   8000*units('N')],
        'C_{mm}'         :[120*units('1/hr'), 360*units('1/hr')],
    })

m.cost = (m.missions[0]['W_{f_m}']*units('1/N') + m.missions[1]['C_m']*m.missions[1]['t_m'])
sol3 = m.localsolve(verbosity = 2)

# Creating a mission array
# Variable + Value M1 + Value M2 + Value MM + Units + Desc
varlist = ['W','S','W_e','W_w','W_{w_{strc}}','W_{w_{surf}}','W_f','t_m','BSFC']
nvars = len(varlist)
nptable = np.array((7,nvars))
sols = [sol1, sol2, sol3]

tablename = "mmtable.tex"
with open(tablename, 'w') as f:
    f.write("\\begin{longtable}{llllll}\n \\toprule\n")
    f.write("\\toprule\n")
    f.write("Variables & Value & Units & Description \\\\ \n")
    f.write("\\midrule\n")
    for varname in varlist:
        try:
            val1 = "%0.3f" % sol1(varname).magnitude
        except:
            val1 = '-'
        try:
            val2 = "%0.3f" % sol2(varname).magnitude
        except:
            val2 = '-'
        try:
            val3 = "%0.3f" % sol3(m.variables_byname(varname)[0]).magnitude
        except:
            val3 = '-'
        try:
            val4 = "%0.3f" % sol3(m.variables_byname(varname)[1]).magnitude
        except:
            val4 = '-'
        #units = unitstr(model[varname].units)
        #label = sol1[varname].descr["label"]
        f.write("$%s$ & %s & %s & %s & %s \\\\\n" %
                    (varname, val1, val2, val3, val4))
    f.write("\\bottomrule\n")
    f.write("\\end{longtable}\n")

