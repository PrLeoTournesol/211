# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 10:43:26 2024

@author: lemai
"""

import math
from matplotlib.pyplot import *

def combinaison_lineaire(A,B,u,v):
    return [A[0]*u+B[0]*v,A[1]*u+B[1]*v]

def interpolation_lineaire(A,B,t):
    return combinaison_lineaire(A,B,t,1-t)

def point_bezier_3(points_control,t):
    x=(1-t)**2
    y=t*t
    A = combinaison_lineaire(points_control[0],points_control[1],(1-t)*x,3*t*x)
    B = combinaison_lineaire(points_control[2],points_control[3],3*y*(1-t),y*t)
    return [A[0]+B[0],A[1]+B[1]]

def courbe_bezier_3(points_control,N):
    if len(points_control) != 4:
        raise SystemExit("4 points de controle")
    dt = 1.0/N
    t = dt
    points_courbe = [points_control[0]]
    while t < 1.0:
        points_courbe.append(point_bezier_3(points_control,t))
        t += dt
    points_courbe.append(points_control[3])
    return points_courbe

def plot_points(points_courbe,style='-'):
    x = []
    y = []
    for p in points_courbe:
        x.append(p[0])
        y.append(p[1])
    plot(x,y,style)
    
figure(figsize=(8,8))
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
points = courbe_bezier_3([P1,P2,P3,P4],50)
plot_points(points,style='b.')
plot_points(points,style='r-')


points = courbe_bezier_3([P4,P5,P6,P7],50)
plot_points(points,style='b.')
plot_points(points,style='r-')

points = courbe_bezier_3([P6,P7,P8,P9],50)
plot_points(points,style='b.')
plot_points(points,style='r-')
plot_points([P0,P1,P2,P3,P4,P5,P6,P7,P8,P9],style='g')
grid()
                 