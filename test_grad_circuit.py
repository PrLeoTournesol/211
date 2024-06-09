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
    if x > b:
        i = i+1
        b = x_positions[i]
        a = x_positions[i-1]
    
    return fhat(a,b,x,y_positions[i-1],y_positions[i])
    

image_par_fhat = np.vectorize(image_par_fhat)







v_0 = 30
inclinaison_0 = -1.4

pos_0 = [-8, 35]
pos_0 = [xhat[40],yhat[40]]

moto = Moto(0.3, 0.5, 400, 2, pos_0, vitesse=v_0)


def next_traj(t, inclinaison, pos_0, moto):

    dt = 0.001

    d_inclinaison = 0.01
    nb_inclinaison = 100
    inclinaisons = np.linspace(inclinaison - nb_inclinaison * d_inclinaison, inclinaison + nb_inclinaison * d_inclinaison, nb_inclinaison)


    moto.acceleration = 0

    resultats_trajs = {}  # inclinaison : x_prevus, y_prevus
    angle_courant = np.arctan2((image_par_fhat(pos_0[0]+0.1) - image_par_fhat(pos_0[0])),0.1) -  np.pi/2

    for inclinaison in inclinaisons:
        valide = True
        current_time = 0

        moto.position = pos_0.copy()
        moto.inclinaison = inclinaison
        # print()
        # print('angle mot : ', moto.angle)
        # print('angle courant : ', angle_courant)
        # print('angle courant : ', angle_courant - np.pi/2)
        # print()

        x_prevus = [pos_0[0]]
        y_prevus = [pos_0[1]]

        while current_time < t:

            moto.update_inclinaison(dt)
            moto.update_vitesse(dt)
            moto.update_position(dt)
            moto.calcul_rayon_courbure()
            moto.calcul_vitesse_angle()
            moto.update_angle(dt)
            moto.calcul_rotation_matrice()
            pos = moto.position

            x_prevus.append(pos[0])
            y_prevus.append(pos[1])

            # if moto.angle > angle_courant + np.pi/2 or moto.angle + np.pi/2 < angle_courant - np.pi/2 :
            #     valide = False
            #     break

            if circuit_test.verif_valide(pos):
                break

            current_time += dt

        if valide : 
            resultats_trajs[inclinaison] = (x_prevus, y_prevus)

    # plt.figure()
    # plt.scatter(resultats_trajs[min(resultats_trajs.keys())][0],resultats_trajs[min(resultats_trajs.keys())][1], c='k')
    # plt.plot(xhat,yhat,c='r')
    # plt.scatter(resultats_trajs[max(resultats_trajs.keys())][0],resultats_trajs[max(resultats_trajs.keys())][1])
    # plt.show()

    # Passage aux moindres carres : 

    resultats_moindre_carre = {}    # moindre_carre : inclinaison

    for inclinaison in resultats_trajs.keys():
        x_prevus = resultats_trajs[inclinaison][0]
        y_prevus = resultats_trajs[inclinaison][1]

        y_ms = image_par_fhat(x_prevus)
        md = 0
        
        Delta_x_voulu = 0.1
        Delta_x_prevu = x_prevus[-1]-x_prevus[0]
        Delta_y_voulu = image_par_fhat(pos_0[0]+0.1)-image_par_fhat(pos_0[0])
        Delta_y_prevu = y_prevus[-1]-y_prevus[0]


        # print('Delta_x_prevu', Delta_x_prevu)
        # print('delta_y_voulu', Delta_y_voulu)
        # print('delta_y_prevu', Delta_y_prevu)
        # print('voulu : ', np.arctan2(Delta_y_voulu,Delta_x_voulu))
        # print('prevu : ', np.arctan2(Delta_y_prevu,Delta_x_prevu))
        # print()

        angle_voulu = np.arctan2(Delta_y_voulu,Delta_x_voulu)
        angle_prevu = np.arctan2(Delta_y_prevu,Delta_x_prevu)

        if angle_voulu - np.pi/2 < angle_prevu < angle_voulu + np.pi/2:
            for y,ym in zip(y_prevus,y_ms):
                md += (y - ym)**2

        else:
            continue
        # plt.figure()
        # plt.scatter(x_prevus,y_prevus, c='k')
        # plt.plot(xhat,yhat,c='r')
        # plt.scatter(x_prevus,y_ms)
        # plt.show()

        resultats_moindre_carre[md] = inclinaison, y_ms, x_prevus
    


    inclinaison_optimal = resultats_moindre_carre[min(list(resultats_moindre_carre.keys()))][0]
    x_suivant = resultats_trajs[inclinaison_optimal][0][-1]
    y_suivant = resultats_trajs[inclinaison_optimal][1][-1]

    # plt.figure()
    # plt.scatter(x_prevus,y_prevus, c='k')
    # plt.plot(xhat,yhat,c='r')
    # plt.scatter(x_prevus,y_ms)
    # plt.show()

    return  inclinaison_optimal, x_suivant, y_suivant, resultats_trajs[inclinaison_optimal][0], resultats_trajs[inclinaison_optimal][1]



inclinaison_opts = [inclinaison_0]
x_opt = [pos_0[0]]
y_opt = [pos_0[1]]


for i in range(4):
    inclinaison_opt, x_suivant, y_suivant, x, y = next_traj(0.1, inclinaison_opts[-1], [x_opt[-1], y_opt[-1]], moto)

    #print(inclinaison_opt)
    print(i)

    inclinaison_opts.append(inclinaison_opt)
    x_opt = x_opt + x
    y_opt = y_opt + y



plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')

plt.scatter(x_positions,y_positions)
plt.plot(xhat,yhat,c='r')
plt.scatter(x_opt,y_opt, c='k')


plt.figure()
plt.plot(range(len(inclinaison_opts)),inclinaison_opts, c='k')

plt.show()