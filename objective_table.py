from SimPleAC_eng import *
from gpkit import units
import numpy as np

objectives = ['W_f','W','D','T_{flight}','W_f/T_{flight}','W_f+c*T_{flight}']
solDict = {}
splitList = ['/','+','*']
baseObj = 'W_f'

m = SimPleAC()

# Parses objective string and returns objective function
def parseObj(i,m):
    # i is objective, m is model
    if '/' in i:
        return m[i.split('/')[0]]/ m[i.split('/')[1]]
    elif 'W_f+c*T_{flight}' in i:
        c = 200
        return  m['W_f'] + c*units('N/hr')*m['T_{flight}']
    else:
        return m[i]

# Parses objective string and returns that objective for solution
def parseSol(i,sol):
    # i is objective, sol is the solution
    if '/' in i:
        return sol(i.split('/')[0]).magnitude/ sol(i.split('/')[1]).magnitude
    elif 'W_f+c*T_{flight}' in i:
        c = 200
        return  sol('W_f').magnitude + c*sol('T_{flight}').magnitude
    else:
        return sol(i).magnitude

# Generates a row of the objectives for a particular solve,
# normalized by the base objective
def genNormalizedRow(sol, baseSol, baseObj, objectives):
        return [np.around(parseSol(i,sol) / parseSol(i,baseSol),2) for i in objectives]

# Prints latex table of np.array
def printTable(table):
    n = table.shape[0]
    print '\\begin{table}'
    print '\\begin{center}'
    print '\\begin{tabular}' + '{' + n*'c' + '}'
    for i in range(0,n):
        row = ''
        for j in range(0,n):
            row = row + str(table[i,j])
            if j < n-1:
                row = row + '&'
            else:
                row = row + '\\\\'
        print row
    print '\\end{tabular}'
    print '\\end{center}'
    print '\\end{table}'

# Loop to find solution for each objective
for i in objectives:
    m.cost = parseObj(i,m)
    solDict[i] = m.localsolve(verbosity=0)
    if i == baseObj:
        baseSol = solDict[i]

# Normalized objective table
normTable = np.zeros([len(objectives),len(objectives)])
count = 0;

for i in objectives:
    normTable[count,:] = genNormalizedRow(solDict[i],baseSol,baseObj,objectives)
    count += 1

printTable(normTable)




