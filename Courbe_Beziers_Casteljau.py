# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 11:29:17 2024

@author: lemai
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import bezier

def plot_points(points_courbe,style='-'):
    x = []
    y = []
    for p in points_courbe:
        x.append(p[0])
        y.append(p[1])
    plt.plot(x,y,style)





positions = [[1, 0], [3, 100], [6, 190], [10, 212], [15, 217],[31,210] , [38, 204], [42, 180], [45, 110], [46, 25]]
x_positions = [i[0] for i in positions]
y_positions = [i[1] for i in positions]


# Dénition des fonctions linéaires sur les intervals x1 x2 
def fhat(x1,x2,x,y1,y2):
    return ((x2-x)/(x2-x1))*y1 + ((x-x1)/(x2-x1))*y2


yhat = []
xhat = np.linspace(x_positions[0],x_positions[-1],500)

def image_par_fhat(x):
    i = 1
    
    a = x_bezier[i-1]
    b = x_bezier[i]  
    while x > b:
        if i >= len(x_bezier)-1:
            break
        i += 1
        b = x_bezier[i]
        a = x_bezier[i-1]
            
    b = x_bezier[i]
    a = x_bezier[i-1]
    
    return fhat(a,b,x,y_bezier[i-1],y_bezier[i])
    
image_par_fhat = np.vectorize(image_par_fhat)







def combinaison_lineaire(A,B,u,v):
    return [A[0]*u+B[0]*v,A[1]*u+B[1]*v]

def interpolation_lineaire(A,B,t):
    return combinaison_lineaire(A,B,t,1-t)

def reduction(points_control,t):
    points_sortie=[]
    N = len(points_control)
    for i in range(N-1):
        points_sortie.append(interpolation_lineaire(points_control[i],points_control[i+1],1-t))

    return points_sortie

def point_bezier_n(points_control,t):
    n = len(points_control)
    while n > 1:
        points_control = reduction(points_control,t)
        n = len(points_control)
    return points_control[0]

def courbe_bezier_n(points_control,N):
    n = len(points_control)
    dt = 1.0/N
    t = dt
    points_courbe = [points_control[0]]
    while t < 1.0:
        points_courbe.append(point_bezier_n(points_control,t))
        t += dt
    points_courbe.append(points_control[n-1])
    return points_courbe



P0 = [0,0]
P1 = [4,100]
P2 = [7,190]
P3 = [10,205]
P4 = [12,210]
P5 = [30,205]
P6 = [37,203]
P7 = [42,175]
P8 = [45,110]
P9 = [47,20]


x_bezier = [i[0] for i in courbe_bezier_n(positions[:6],200)] + [i[0] for i in courbe_bezier_n(positions[5:],200)]
y_bezier = [i[1] for i in courbe_bezier_n(positions[:6],200)] + [i[1] for i in courbe_bezier_n(positions[5:],200)]

print(x_bezier)


plt.figure()


plt.plot(x_bezier, y_bezier)
plt.scatter(7, image_par_fhat(7))
#plot_points(courbe_bezier_n(positions[:6],200),style='r-')
#plot_points(courbe_bezier_n(positions[5:],200),style='r-')
plot_points(positions,style='o')
plot_points(positions,style='b-')

plt.grid()

plt.show()
