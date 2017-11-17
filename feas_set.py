from SimPleAC_eng import SimPleAC

# Have to execute this in a Robust environment, for plot_feasibilities

m = SimPleAC()
m.cost = m['W_f']
sol = m.localsolve()

substitutions = {'V_{f_{wing}}':0.1211*units('m^3'),
                 'V_{f_{avail}}':0.6331*units('m^3'),
                 'V_{f_{fuse}}': 0.512*units('m^3')}

mGP = m.as_gpconstr(None,substitutions)
plot_feasibilities(mGP.variables_byname('W_{w_{coeff1}}'),mGP.variables_byname('W_{w_{coeff2}}'),mGP)


# Template code from Robust
# m = Model(D, constraints)
# m.solve()
# plot_feasibilities(W_W_coeff1, W_W_coeff2, m)
# W_W_coeff1.key.descr["pr"] = 66
# W_W_coeff2.key.descr["pr"] = 66
# RM = RobustModel(m, 'elliptical', two_term=False)
# RMsol = RM.robustsolve(verbosity=1)
# rm = RM.get_robust_model()
# plot_feasibilities(W_W_coeff1, W_W_coeff2, m, rm, "elliptical")
