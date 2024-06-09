from structure import *
import time
import numpy as np
import matplotlib.pyplot as plt


x_0 = -10
y_0 = 1

x = [x_0]
y = [y_0]
x2 = []
y2 = []

test = []

murs_interieurs = [Mur((0,0),(0,30)), Mur((0,30),(20,30)), Mur((20,30),(20,0))] 
murs_exterieurs = [Mur((-15,0),(-15,40)), Mur((-15,40),(40,40)), Mur((40,40),(40,0))]

circuit_test= Circuit(
    murs_interieurs,
    murs_exterieurs,
    [[-8,0],[0,0]], 
    [[10,0],[17,0]]
    )

rayon_circuit = 15

init_time = time.time()
current_time = 0
dt = 0.01

resultats = {}


for _ in range(1000):

    current_time = 0

    p1 = np.random.rand() / 10
    p2 = (np.random.rand() - 1) 
    p3 = 20
    p4 = -np.random.rand()

    x = [x_0]
    y = [y_0]
    v = [p3]

    acc = []

    valide = True
    moto = Moto(0.3, 0.5, 400, 2, [x_0,y_0],vitesse=p3)


    while current_time < 30:

        if x[-1] < 20 :
             moto.acceleration = p2
        else:
            moto.acceleration = -p2

        if np.sqrt((x[-1] - 0)**2 + (y[-1] - 30)**2) < 10:
            moto.inclinaison = -np.arctan2(moto.vitesse**2,9.81*rayon_circuit)
        else:
            moto.inclinaison =  p4



        # previous_time = current_time
        # current_time = time.time() - init_time
        # dt = current_time-previous_time
        

        moto.update_inclinaison(dt)
        moto.update_vitesse(dt)
        moto.update_position(dt)
        moto.calcul_rayon_courbure()
        moto.calcul_vitesse_angle()
        moto.update_angle(dt)
        moto.calcul_rotation_matrice()
        pos = moto.position_moto
        moto.distance_parcourue(pos, [x[-1],y[-1]])

        x.append(pos[0])
        y.append(pos[1])
        v.append(moto.vitesse)

        if circuit_test.verif_valide(pos):
            x2.append(pos[0])
            y2.append(pos[1])
            valide = True
            break

        # if abs(((x[-1] - (0))/(-15 - x[0])) * ((40 - y[-1])/(y[-1] - 30)) - 1) < 0.5:
        #     x2.append(pos[0])
        #     y2.append(pos[1])
        #     valide = True
        #     break

        current_time += dt
    
    if valide:
        resultats[(x[-1] - 40)**2 + (y[-1] - 0)**2] = (p1, p2, p3, p4,x,y,v, acc)


print('vitesse max : ', resultats[min(resultats.keys())][:4])
#print(resultats)
#print(len(resultats))

#print('distance parcourue : ', moto.distance_totale)


#circuit_test.affichage()


x_max = resultats[min(resultats.keys())][4]
y_max = resultats[min(resultats.keys())][5]
v_max = resultats[min(resultats.keys())][6]
acc_max = resultats[min(resultats.keys())][7]

plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')
plt.scatter(x_max, y_max)
plt.scatter(x2, y2, color='r')

# plt.figure()
# plt.plot(np.linspace(0,30,len(acc_max)+1), v_max)
# plt.xlabel('vmax')

# plt.figure()
# plt.plot(np.linspace(0,30,len(acc_max)), acc_max)
# plt.xlabel('accmax')


plt.show()