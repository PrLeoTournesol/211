import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from structure import *


murs_interieurs = [Mur((0,0),(0,30)), Mur((0,30),(20,30)), Mur((20,30),(20,0))] 
murs_exterieurs = [Mur((-15,0),(-15,40)), Mur((-15,40),(35,40)), Mur((35,40),(35,0))]

circuit_test= Circuit(
    murs_interieurs,
    murs_exterieurs,
    [[-8,0],[0,0]], 
    [[10,0],[17,0]]
    )



positions = [[-10, 2], [-8, 35], [3, 39], [15, 36], [21, 30], [23, 5]]
x_positions = [i[0] for i in positions]
y_positions = [i[1] for i in positions]


# Dénition des fonctions linéaires sur les intervals x1 x2 
def fhat(x1,x2,x,y1,y2):
    return ((x2-x)/(x2-x1))*y1 + ((x-x1)/(x2-x1))*y2


yhat = []
xhat = np.linspace(x_positions[0],x_positions[-1],500)

# Interpolation linéaire de la fonction 
i = 1
for x in xhat:
    a = x_positions[i-1]
    b = x_positions[i]   
    if x > b:
        i = i+1
        b = x_positions[i]
        a = x_positions[i-1]
    while x <= b:
        yhat.append(fhat(a,b,x,y_positions[i-1],y_positions[i]))
        break

def image_par_fhat(x):
    i = 1
    
    a = x_positions[i-1]
    b = x_positions[i]  
    while x > b:
        if i >= len(x_positions)-1:
            break
        i += 1
        b = x_positions[i]
        a = x_positions[i-1]
            
    b = x_positions[i]
    a = x_positions[i-1]
    
    return fhat(a,b,x,y_positions[i-1],y_positions[i])
    
xs = np.linspace(-10,25,200)
ys = []
for x in xs:
    ys.append(image_par_fhat(x))

pos_0 = [-10,40]
#print(np.tan((image_par_fhat(pos_0[0]+0.1) - image_par_fhat(pos_0[0]))/0.1))

#print(image_par_fhat(-15))

plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')

plt.scatter(x_positions,y_positions)
plt.plot(xhat,yhat,c='r')
plt.plot(xs,ys,c='k')

plt.show()