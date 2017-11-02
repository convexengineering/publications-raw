from SimPleAC_eng import *
from gpkit import units

objectives = ['W_f','W','D','T_{flight}']#,'W_f/T_{flight}','W_f+c*T_{flight}']
solDict = {}
splitList = ['/','+','*']
baseObj = 'W_f'

m = SimPleAC()

for i in objectives:
    if '/' in i:
        m.cost = m[i.split('/')[0]]/ m[i.split('/')[1]]
    elif 'W_f+c*T_{flight}' in i:
        c = 200
        m.cost = m['W_f'] + c*units('N/hr')*m['T_{flight}']
    else:
        m.cost = m[i]
    solDict[i] = m.localsolve(verbosity=0)
    if i == baseObj:
        baseSol = solDict[i]

def genNormalizedRow(sol,baseSol,baseObj,objectives):
    return [sol(i)/baseSol(i) for i in objectives]


for i in objectives:
    print genNormalizedRow(solDict[i],baseSol,baseObj,objectives)


