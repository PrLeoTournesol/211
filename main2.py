from structure import *
import time
import numpy as np
import matplotlib.pyplot as plt


x_0 = -10
y_0 = 1

x = [-x_0]
y = [y_0]
x2 = []
y2 = []

test = []

murs_interieurs = [Mur((10,0),(10,190)), Mur((10,190),(40,190)), Mur((40,190),(40,0))] 
murs_exterieurs = [Mur((0,0),(0,220)), Mur((0,220),(50,220)), Mur((50,220),(50,0))]


circuit_test= Circuit(
    murs_interieurs,
    murs_exterieurs,
    [[-8,0],[0,0]], 
    [[10,0],[17,0]]
    )
    
init_time = time.time()
current_time = 0
dt = 0.01

resultats = {}


p1 = -0.04126209544304882
p2 = 0.7859248295039817
p3 = 4.865532118450655
p4 = -0.014949277784002775

x = [x_0]
y = [y_0]
v = [p3]

angle = [0]

valide = True
moto = Moto(0.3, 0.5, 400, 2, [x_0,y_0],vitesse=45)


while current_time < 20:

    moto.update_inclinaison(dt)
    moto.update_vitesse(dt)
    moto.update_position(dt)
    moto.calcul_rayon_courbure()
    moto.calcul_vitesse_angle()
    moto.update_angle(dt)
    moto.calcul_rotation_matrice()
    pos = moto.position
    
    moto.distance_parcourue(pos, [x[-1],y[-1]])


    # if x[-1] < 14:
    #     moto.acceleration = p1
    #     moto.inclinaison = p4 * current_time
    #     t5 = current_time

    # else:
    #     moto.acceleration = p1
    #     moto.inclinaison = -0.0

    moto.acceleration = 0
    moto.inclinaison = -1

    # previous_time = current_time
    # current_time = time.time() - init_time
    # dt = current_time-previous_time
    
    x.append(pos[0])
    y.append(pos[1])
    angle.append(moto.angle)
    v.append(moto.vitesse)


    if circuit_test.verif_valide(pos):
        x2.append(pos[0])
        y2.append(pos[1])
        valide = False
        break

    

    current_time += dt




print('distance parcourue : ', moto.distance_totale)


#circuit_test.affichage()



plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')

plt.xlabel('x (m)')
plt.ylabel('y (m)')

plt.scatter(x, y)
# plt.scatter(x2, y2, color='r')



# plt.figure()
# plt.plot(x,angle)

# plt.figure()
# plt.plot(x,v)


plt.show()