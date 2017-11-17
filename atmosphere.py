from gpkit import Model, Variable, SignomialsEnabled, VarKey, units
from gpkit.constraints.bounded import Bounded
from gpkit import Vectorize
import numpy as np
import matplotlib.pyplot as plt


class Atmosphere(Model):
    "Atmosphere models borrowed from Tony Tao, 2017."
    def setup(self):
        # Env. constants
        alt_top = Variable('h_{top}',10000,'m','highest altitude valid')
        a_MSL   = Variable('a_{MSL}',340.20,'m/s','Speed of sound at MSL')
        mu_MSL  = Variable('\\mu_{MSL}', 1.778e-5, "kg/m/s", 'dynamic viscosity at MSL', pr=4.)
        nu_MSL  = Variable('\\nu_{MSL}', 1.4524e-5, 'm^2/s', 'kinematic viscosity at MSL')
        T_MSL   = Variable('T_{MSL}', 288.19, 'K', 'temperature at MSL')
        rho_MSL = Variable("\\rho_{MSL}", 1.2256, "kg/m^3", "density of air at MSL", pr=5.)
        p_MSL   = Variable('P_{MSL}', 101308, 'Pa', 'pressure at MSL')

        alt = Variable('h','m','altitude')
        a   = Variable('a','m/s','Speed of sound')
        mu  = Variable('\\mu', "kg/m/s", 'dynamic viscosity', pr=4.)
        nu  = Variable('\\nu', 'm^2/s', 'kinematic viscosity')
        p = Variable('P', 'Pa', 'pressure')
        T   = Variable('T', 'K', 'temperature ')
        rho = Variable("\\rho", "kg/m^3", "density of air", pr=5.)


        # Defining ratios needed for constraints
        alt_rat = alt/alt_top
        a_rat = a/a_MSL
        mu_rat = mu/mu_MSL
        nu_rat = nu/nu_MSL
        p_rat = p/p_MSL
        rho_rat = rho/rho_MSL
        T_rat = T/T_MSL

        constraints = []
        constraints += [
        alt <= alt_top,
        a_rat ** -0.0140    >= 0.00173 * (alt_rat) ** 1.13 + 1.00 * (alt_rat) ** 1.20e-05,
        mu_rat ** -0.00795  >= 0.00156 * (alt_rat) ** 1.17 + 1.00 * (alt_rat) ** 1.33e-05,
        nu_rat ** 0.00490   >= 0.00424 * (alt_rat) ** 1.10 + 1.00 * (alt_rat) ** 1.67e-05,
        p_rat ** -0.00318   >= 0.00416 * (alt_rat) ** 1.12 + 1.00 * (alt_rat) ** 2.18e-05,
        rho_rat ** -0.00336 >= 0.00357 * (alt_rat) ** 1.11 + 1.00 * (alt_rat) ** 1.72e-05,
        T_rat ** -0.00706   >= 0.00173 * (alt_rat) ** 1.13 + 1.00 * (alt_rat) ** 1.21e-05,
        ]

        return constraints

if __name__ == "__main__":
    m = Atmosphere()
    m.substitutions.update({'h':5000*units('m')})
    m.cost = 1/m['a']/m['\\mu']*m['\\nu']/m['P']/m['\\rho']/m['T']
    sol = m.solve()
    print sol.table()
