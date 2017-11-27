from gpkit import Model, Variable, SignomialsEnabled, SignomialEquality, VarKey, units,Vectorize
from gpkit.constraints.bounded import Bounded
from relaxed_constants import relaxed_constants, post_process

import numpy as np
import matplotlib.pyplot as plt

from SimPleAC_mission2 import Mission, SimPleAC
from atmosphere import Atmosphere

class Multimission(Model):
    def setup(self,Nmissions,Nsegments):
        self.aircraft = SimPleAC()

        # Multimission objective variables
        W_f_mm = Variable('W_{f_{mm}}','N','Multimission fuel weight')

        with Vectorize(Nmissions):
            W_f_m   = Variable('W_{f_{m}}','N','Total mission fuel')
            t_m     = Variable('t_m','hr','Total mission time')

            with Vectorize(Nsegments):
                Wavg   = Variable('W_{avg}','N','Segment average weight')
                Wstart = Variable('W_{start}', 'N', 'Weight at the beginning of flight segment')
                Wend   = Variable('W_{end}', 'N','Weight at the end of flight segment')
                h      = Variable('h','m','Flight altitude')
                dhdt   = Variable('\\frac{\\Delta h}{dt}','m/hr','Climb rate')
                W_f_s  = Variable('W_{f_s}','N', 'Segment fuel burn')
                t_s    = Variable('t_s','hr','Time spent in flight segment')
                R_s    = Variable('R_s','km','Range flown in segment')
                state  = Atmosphere()
                self.aircraftP = self.aircraft.dynamic(state)

            # Mission variables
            Range      = Variable("Range",3000, "km", "aircraft range")
            W_p        = Variable("W_p", 6250, "N", "payload weight", pr=20.)
            V_min      = Variable("V_{min}", 25, "m/s", "takeoff speed", pr=20.)
            cost_index = Variable("Cost Index",360,'1/hr','hourly cost index')

        constraints = []

        # Setting up the mission
        with SignomialsEnabled():
            constraints += [h == state['h'], # Linking states

                        # Weights at beginning and end of mission
                        Wstart[0] >= W_p + self.aircraft.wing['W_w'] + self.aircraft.engine['W_e'] + W_f_m,
                        Wend[Nsegments-1] >= W_p + self.aircraft.wing['W_w'] + self.aircraft.engine['W_e'],

                        # Lift, and linking segment start and end weights
                        Wavg <= 0.5 * state['\\rho'] * self.aircraft['S'] * self.aircraftP.wingP['C_L'] * self.aircraftP['V'] ** 2,
                        Wstart >= Wend + W_f_s, # Making sure fuel gets burnt!
                        Wstart[1:Nsegments] == Wend[:Nsegments-1],
                        Wavg == Wstart ** 0.5 * Wend ** 0.5,

                        # Altitude changes
                        h[0] == t_s[0]*dhdt[0], # Starting altitude
                        dhdt >= 1.*units('m/hr'),
                        SignomialEquality(h[1:Nsegments],h[:Nsegments-1] + t_s[1:Nsegments]*dhdt[1:Nsegments]),

                        # Thrust and fuel burn
                        W_f_s >= self.aircraftP.engineP['BSFC'] * self.aircraftP.engineP['T'] * t_s,
                        self.aircraftP.engineP['T'] * self.aircraftP['V'] >= self.aircraftP['D'] * self.aircraftP['V'] + Wavg * dhdt,

                        # Flight time
                        t_s == R_s/self.aircraftP['V'],

                        # Aggregating segment variables
                        self.aircraft['W_f'] >= W_f_m,
                        R_s == Range/Nsegments, # Dividing into equal range segments
                        W_f_m >= sum(W_f_s),
                        t_m >= sum(t_s)
                        ]

        # Maximum takeoff weight
        constraints += [self.aircraft['W'] >= W_p + self.aircraft.wing['W_w'] + self.aircraft['W_f'] + self.aircraft.engine['W_e']]

        # Stall constraint
        constraints += [self.aircraft['W'] <= 0.5 * state['\\rho'] *
                            self.aircraft['S'] * self.aircraft['C_{L,max}'] * V_min ** 2]

        # Wing weight model
        constraints += [self.aircraft.wing['W_{w_{strc}}']**2. >=
                        self.aircraft.wing['W_{w_{coeff1}}']**2. / self.aircraft.wing['\\tau']**2. *
                        (self.aircraft.wing['N_{ult}']**2. * self.aircraft.wing['A'] ** 3. *
                        ((W_p+self.aircraft.fuse['V_{f_{fuse}}']*self.aircraft['g']*self.aircraft['\\rho_f']) *
                         self.aircraft['W'] * self.aircraft.wing['S']))]

        # Multimission constraints
        constraints += [W_f_mm >= sum(W_f_m)]

        return constraints, state, self.aircraft, self.aircraftP

if __name__ == "__main__":
    m = Multimission(3,5)
    m.substitutions.update({
        'Range'     :[3000*units('km'), 2300*units('km'), 1500*units('km')],
        'W_p'       :[6250*units('N'),   8000*units('N'),   4000*units('N')],
        'Cost Index':[360*units('1/hr'), 480*units('1/hr'), 240*units('1/hr')]
    })
    m.cost = m['W_{f_{mm}}']*units('1/N') + sum(m['Cost Index']*m['t_m'])
    sol = m.localsolve(verbosity = 4)

