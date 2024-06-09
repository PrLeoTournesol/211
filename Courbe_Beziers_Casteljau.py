# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 11:29:17 2024

@author: lemai
"""
import math
from matplotlib.pyplot import *

def plot_points(points_courbe,style='-'):
    x = []
    y = []
    for p in points_courbe:
        x.append(p[0])
        y.append(p[1])
    plot(x,y,style)
    
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

figure()
plot_points(courbe_bezier_n([P0,P1,P2,P3,P4,P5],200),style='r-')
plot_points(courbe_bezier_n([P5,P6,P7,P8,P9],200),style='r-')
plot_points([P0,P1,P2,P3,P4,P5,P6,P7,P8,P9],style='o')
plot_points([P0,P1,P2,P3,P4,P5,P6,P7,P8,P9],style='b-')

grid()
