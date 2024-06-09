from structure import *
import matplotlib.pyplot as plt
import numpy as np

murs_interieurs = [Mur((10,0),(10,190)), Mur((10,190),(40,190)), Mur((40,190),(40,0))] 
murs_exterieurs = [Mur((0,0),(0,220)), Mur((0,220),(50,220)), Mur((50,220),(50,0))]



positions = [[1, 0], [3, 100], [6, 190], [10, 212], [15, 217],[31,210] , [38, 204], [42, 180], [45, 110], [46, 25]]
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

def image_par_fhat_cord(x):
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
    

image_par_fhat = np.vectorize(image_par_fhat)

def corde(x1,x2,x,y1,y2):
    return ((x2-x)/(x2-x1))*y1 + ((x-x1)/(x2-x1))*y2


corde = np.vectorize(corde)


def perpendiculaire(x0, y0, X, Y):
        """Find the perpendicular distance between a point on a line and a curve"""
        eps = 0.1
        distance_perpendiculaire = []
        for x in X:
            if image_par_fhat(x) - y0 :
                distance_perpendiculaire.append(0)
            if abs((X[-1] - X[0]) * (x - x0) + ((Y[-1] - Y[0]) * (image_par_fhat(x) - y0))) < eps:
                distance_perpendiculaire.append( ((x0-x)**2 + (image_par_fhat(x) - y0)**2)**.5 )

        return max(distance_perpendiculaire)

def find_radius(line_x, line_y):

    C = ((line_x[0]-line_x[-1])**2 + (line_y[0]-line_y[-1])**2)**.5


    d_max = 0
    for x in line_x:
        distance_perpend = perpendiculaire(x, line_y[list(line_x).index(x)], line_x, line_y)
        if distance_perpend > d_max :
            d_max = distance_perpend

    H = d_max
    if H == 0:
        radius = np.inf
    else:
        radius = C**2/(8*H) + H/2

    return radius



x1 = 8
corde_x = np.linspace(x1, x1+20, 100)
corde_y = corde(corde_x[0], corde_x[-1], corde_x, image_par_fhat(corde_x[0]), image_par_fhat(corde_x[-1]))



print('R : ',find_radius(corde_x, corde_y))

print('Inclinaison : ', np.arctan2(45**2, find_radius(corde_x, corde_y) * 9.81))




plt.figure()

plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')

plt.xlabel('x (m)')
plt.ylabel('y (m)')

plt.scatter(x_positions,y_positions)
plt.plot(xhat,yhat,c='r')
#plt.plot(corde_x,corde_y,c='g')
plt.show()