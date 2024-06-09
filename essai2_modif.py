import matplotlib.pyplot as plt 
from matplotlib import cm
import numpy as np
from structure import *
from tqdm import tqdm
import math

#######################################################################################
# Création du circuit
murs_interieurs = [Mur((10,0),(10,190)), Mur((10,190),(40,190)), Mur((40,190),(40,0))] 
murs_exterieurs = [Mur((0,0),(0,220)), Mur((0,220),(50,220)), Mur((50,220),(50,0))]

#######################################################################################
# Création des points de la courbe squelette
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
    
image_par_fhat = np.vectorize(image_par_fhat)







#######################################################################################

# Grandeurs initiales
v_0 = 30
inclinaison_0 = 0
pos_0 = [xhat[0],yhat[0]]
angle_0 = 0

moto = Moto(0.3, 0.5, 400, 2, pos_0, vitesse=v_0)


# Fonction de minimisation d'un pas de la trajectoire
def next_traj(t, inclinaison, angle_0, pos_0, moto):

    dt = 0.001

    pas_inclinaison = 0.1
    limites_inclinaison = np.pi/2
    inclinaisons = np.arange(inclinaison - limites_inclinaison, inclinaison + limites_inclinaison, pas_inclinaison)

####################################################################################################
    # print('inclinaison envoyé : ', inclinaison)
    # plt.figure()

    # plt.scatter(range(len(inclinaisons)),inclinaisons)
    # plt.title(inclinaison)
    # plt.show()
####################################################################################################



    moto.acceleration = 0

    # Calcul de l'angle de la trajectoire squelette à l'origine de la trajectoire calculée
    angle_courant = np.arctan2(image_par_fhat(pos_0[0] + 0.1) - image_par_fhat(pos_0[0]) , 0.1)

    resultats_trajs = {}  # inclinaison : (x_calcs, y_calcs)

    # Boucle sur les différentes valeurs d'inclinaison
    for inclinaison in inclinaisons:
        current_time = 0

        moto.angle = angle_0
        moto.position = pos_0.copy()
        moto.inclinaison = inclinaison

        x_calcs = [pos_0[0]]
        y_calcs = [pos_0[1]]

        while current_time < t:

            moto.update_inclinaison(dt)
            moto.update_vitesse(dt)
            moto.update_position(dt)
            moto.calcul_rayon_courbure()
            moto.calcul_vitesse_angle()
            moto.update_angle(dt)
            moto.calcul_rotation_matrice()
            pos = moto.position

            x_calcs.append(pos[0])
            y_calcs.append(pos[1])

            current_time += dt
 
        # Calcul de l'angle de la trajectoire calculée
        angle_traj = np.arctan2(y_calcs[-1] - y_calcs[0], x_calcs[-1] - x_calcs[0])

        # Vérifie que la trajectoire ne revienne pas en arrière et ajoute les résultats au tableau
        if abs(angle_traj - angle_courant) < np.pi/2:
            resultats_trajs[inclinaison] = (x_calcs, y_calcs, angle_traj-np.pi/2)

####################################################################################################
    XXX =[]
    YYY = []
    for inclinaison in resultats_trajs.keys():
        for lx in resultats_trajs[inclinaison][0]:
            XXX.append(lx)
        for ly in resultats_trajs[inclinaison][1]:
            YYY.append(ly)
    
    #plt.figure()

    #plt.scatter(x_positions,y_positions)
    #plt.scatter(XXX,YYY)
    #plt.plot(xhat,yhat,c='r')
    #plt.show()
####################################################################################################
        
    # Effectue la minimisation de l'angle de la trajectoire calculée
    resultats_critere = {}    # critère : (inclinaison_opti, x_calcs, y_calcs, angle_suivant)

    for inclinaison in resultats_trajs.keys():

        # Trajectoire calculée
        x_calcs = resultats_trajs[inclinaison][0]
        y_calcs = resultats_trajs[inclinaison][1]


        # Trajectoire modèle
        y_s = image_par_fhat(x_calcs)
        
        # Calcul des angles
        angle_prevu = np.arctan2(y_calcs[-1]-y_calcs[0], x_calcs[-1]-x_calcs[0])
        angle_voulu = np.arctan2(y_s[-1]-y_s[0], x_calcs[-1]-x_calcs[0])
        
        # md = 0          

        # for y,ym in zip(y_calcs,y_s):
        #     md += (y - ym)**2
        # critere = md

        critere = angle_prevu - angle_voulu 

        # ajout des résultats
        resultats_critere[abs(critere)] = inclinaison, y_s, x_calcs

    inclinaison_optimal = resultats_critere[min(list(resultats_critere.keys()))][0]
    x_calcs = resultats_trajs[inclinaison_optimal][0]
    y_calcs = resultats_trajs[inclinaison_optimal][1]
    angle_suivant = resultats_trajs[inclinaison_optimal][2]


##########################################################################################################
    # print('inclinaison calcule : ', inclinaison_optimal)
    # plt.figure()

    # plt.scatter(x_positions,y_positions)
    # plt.scatter(XXX,YYY)
    # plt.scatter(resultats_trajs[inclinaison_optimal][0],resultats_trajs[inclinaison_optimal][1], color='k')
    # #plt.scatter(resultats_trajs[inclinaison_optimal][0],y_s_opti, color='r')
    # plt.plot(xhat,yhat,c='r')
    # plt.xlabel('x (m)')
    # plt.ylabel('y (m)')
    # plt.show()
##########################################################################################################


    return  inclinaison_optimal, x_calcs, y_calcs, angle_suivant





##########################################################################################################
# Simulation sur plusieurs pas de temps

t_simules = np.arange(0.3, .8, 0.1)


resultats = {}

for t_simule in tqdm(t_simules):

    inclinaison_opts = [inclinaison_0]
    x_opts = [pos_0[0]]
    y_opts = [pos_0[1]]
    angles = [angle_0]
    t_total = [0]

    
    # Calcul de la trajectoire complète
    while x_opts[-1] < 40 or y_opts[-1] >= 0:
        inclinaison_opt, x, y, angle = next_traj(t_simule, inclinaison_opts[-1], angles[-1], [x_opts[-1], y_opts[-1]], moto)

        inclinaison_opts.append(inclinaison_opt)
        x_opts = x_opts + x
        y_opts = y_opts + y
        angles.append(angle)
        t_total.append(t_total[-1]+t_simule)

    # Critère des moindres carrés
    y_s = image_par_fhat(x_opts)
    md = 0  

    for i in range(len(y_s)):
        if i > 10 : 
            # Vérifie que la trajectoire calculée ne fasse pas demi-tour
            if x_opts[i] - x_opts[i-10] < 0:
                # si oui, on s'assure de ne pas la prendre
                md+=100000
        md += (y_opts[i] - y_s[i])**2

    critere = md

    resultats[critere] = x_opts, y_opts, inclinaison_opts, t_simule, t_total


######################################################################################################################
    # plt.figure()
    # for mur in murs_interieurs:
    #     plt.plot(mur.x_points,mur.y_points,'g')
    # for mur in murs_exterieurs:
    #     plt.plot(mur.x_points,mur.y_points,'c')

    # plt.scatter(x_positions,y_positions)
    # plt.plot(xhat,yhat,c='r')
    # plt.title('Trajectoire')
    # plt.xlabel('x (m)')
    # plt.ylabel('y (m)')

    # plt.scatter(x_opts,y_opts[:len(x_opts)], c='k')
    # plt.title('p_t = ' + str(t_simule))

    # plt.figure()
    # plt.plot(t_total,inclinaison_opts)
    # plt.show()
######################################################################################################################


x_opts, y_opts, inclinaison_opts, t_simu, t_total = resultats[min(resultats.keys())]













############################################################################################################
# A trier plus tard

temps = np.linspace(0,30, len(x_opts))


fitting_x = np.polyfit(temps, x_opts ,15) 
function_x = np.poly1d(fitting_x)

fitting_y = np.polyfit(temps, y_opts ,15) 
function_y = np.poly1d(fitting_y)




fitting_inclin = np.polyfit(t_total, inclinaison_opts ,6) 
function_inclin = np.poly1d(fitting_inclin)

################################################################################################################

# Pour v0 = 30 et t_simu = 0.3

A = 21
B = 13

from scipy.interpolate import CubicSpline
function_inclin = CubicSpline(t_total,inclinaison_opts)
print(inclinaison_opts)

inclinaisons1 = inclinaison_opts[:A]
t1 = t_total[:len(inclinaisons1)]
inclinaisons2 = inclinaison_opts[A:A+B]
t2 = t_total[len(inclinaisons1):len(inclinaisons1)+len(inclinaisons2)]
inclinaisons3 = inclinaison_opts[A+B:]
t3 = t_total[len(inclinaisons2)+len(inclinaisons1):]

f1 = np.poly1d(np.polyfit(t1, inclinaisons1, 1))
f2 = np.poly1d(np.polyfit(t2, inclinaisons2, 4))
f3 = np.poly1d(np.polyfit(t3, inclinaisons3, 1))

################################################################################################################""
# Pour v0 = 30 et t_simu = 0.1

# from scipy.interpolate import CubicSpline
# function_inclin = CubicSpline(t_total,inclinaison_opts)

# A = 69
# B = 23

# inclinaisons1 = inclinaison_opts[:A]
# t1 = t_total[:len(inclinaisons1)]
# inclinaisons2 = inclinaison_opts[A:A+B]
# t2 = t_total[len(inclinaisons1):len(inclinaisons1)+len(inclinaisons2)]
# inclinaisons3 = inclinaison_opts[A+B:]
# t3 = t_total[len(inclinaisons2)+len(inclinaisons1):]

# f1 = np.poly1d(np.polyfit(t1, inclinaisons1, 1))
# f2 = np.poly1d(np.polyfit(t2, inclinaisons2, 4))
# f3 = np.poly1d(np.polyfit(t3, inclinaisons3, 1))

################################################################################################################""



# current_time = 0
# dt = 0.1
# x_reele = [pos_0[0]]
# y_reele = [pos_0[1]]
# moto = Moto(0.3, 0.5, 400, 2, pos_0, vitesse=v_0)

# while (x_reele[-1] < 40 or y_reele[-1] >= 0) and current_time < 16:

#     moto.update_inclinaison(dt)
#     moto.update_vitesse(dt)
#     moto.update_position(dt)
#     moto.calcul_rayon_courbure()
#     moto.calcul_vitesse_angle()
#     moto.update_angle(dt)
#     moto.calcul_rotation_matrice()
#     pos = moto.position

#     moto.acceleration = 0
    
#     # for i in range(len(t_total) - 1):
#     #     if t_total[i] <= current_time < t_total[i+1]:
#     #         moto.inclinaison = inclinaison_opts[i]


#     if current_time <= t1[-1]:
#         moto.inclinaison = f1(current_time)
#     elif t1[-1] < current_time <= t2[-1]:
#         moto.inclinaison = f2(current_time)
#     else:
#         moto.inclinaison = f3(current_time)


#     # previous_time = current_time
#     # current_time = time.time() - init_time
#     # dt = current_time-previous_time
    
#     x_reele.append(pos[0])
#     y_reele.append(pos[1])

#     current_time += dt

















plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')

plt.scatter(x_positions,y_positions)
plt.plot(xhat,yhat,c='r')

plt.scatter(x_opts,y_opts[:len(x_opts)], c='k')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Trajectoire totale')
# plt.title(t_simu)

plt.figure()
plt.plot(t_total,inclinaison_opts)
plt.plot(t_total,function_inclin(t_total), 'k')
plt.plot(t1,f1(t1))
plt.plot(t2,f2(t2))
plt.plot(t3,f3(t3))
plt.title('Angle beta')
plt.xlabel('t (s)')
plt.ylabel('beta (rad)')

plt.figure()
plt.plot(temps,x_opts)
plt.plot(temps,function_x(temps))
plt.title('x')

plt.figure()
plt.plot(temps,y_opts)
plt.plot(temps,function_y(temps))
plt.title('y')

plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')
plt.plot(function_x(temps),function_y(temps))
plt.title('Traj')


# plt.figure()
# for mur in murs_interieurs:
#     plt.plot(mur.x_points,mur.y_points,'g')
# for mur in murs_exterieurs:
#     plt.plot(mur.x_points,mur.y_points,'c')
# plt.plot(x_reele, y_reele)



plt.show()

liste_PointOpt=[]
for i in range(len(x_opts)):
    if i%40==0:
        liste_PointOpt.append([x_opts[i], y_opts[i]])    
    

def plot_points(points_courbe,style='-'):
    x = []
    y = []
    for p in points_courbe:
        x.append(p[0])
        y.append(p[1])
    plt.plot(x,y,style)
    
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

plt.figure()
A=courbe_bezier_n(liste_PointOpt,100)
plot_points(A,style='r-')
plot_points(liste_PointOpt, style='b')
plt.scatter(A[0],A[1])
plt.grid()

X_bez=[]
Y_bez=[]

for i in A:
    X_bez.append(i[0])
    Y_bez.append(i[1])

plt.figure()
for mur in murs_interieurs:
    plt.plot(mur.x_points,mur.y_points,'g')
for mur in murs_exterieurs:
    plt.plot(mur.x_points,mur.y_points,'c')
plt.plot(X_bez,Y_bez)
plt.title('Traj')
plt.show()