
# R = np.array([[1,-15,(-15)**2,(-15)**3,(-15)**4],
#                 [1,-13,(-13)**2,(-13)**3,(-13)**4],
#                 [1,-8,(-8)**2,(-8)**3,(-8)**4],
#                 [1,3,(3)**2,(3)**3,(3)**4],
#                 [1,21,(21)**2,(21)**3,(21)**4],
#                 [1,30,(30)**2,(30)**3,(30)**4]])


# y_tilde = np.array([2,20,35,38,30,5])


# RT = np.transpose(R)

# a = RT @ R
# b = np.linalg.inv(a)
# c = RT @ y_tilde

# pMC =  b @ c


# p = np.polyfit(x_points,y_points, 3)

# p_extra = np.poly1d(p)

# y_extrap = [pMC[0] + pMC[1]*x + pMC[2] * x**2 + pMC[3] * x**3 + pMC[4] * x**4 for x in np.linspace(-15,30,100)]
# y_extrap_scatter = [pMC[0] + pMC[1]*x + pMC[2] * x**2 + pMC[3] * x**3 + pMC[4] * x**4 for x in x_points]

