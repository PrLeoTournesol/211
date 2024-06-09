import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from structure import *
from tqdm import tqdm


murs_interieurs = [Mur((10,0),(10,190)), Mur((10,190),(40,190)), Mur((40,190),(40,0))] 
murs_exterieurs = [Mur((0,0),(0,220)), Mur((0,220),(50,220)), Mur((50,220),(50,0))]

circuit_test= Circuit(
    murs_interieurs,
    murs_exterieurs,
    [[-8,0],[0,0]], 
    [[10,0],[17,0]]
    )



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
    
def corde(x1,x2,x,y1,y2):
    return ((x2-x)/(x2-x1))*y1 + ((x-x1)/(x2-x1))*y2


image_par_fhat = np.vectorize(image_par_fhat)
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

def find_inclinaison(line_x, line_y):
    return np.arctan2(45**2, find_radius(corde_x, corde_y) * 9.81)













v_0 = 30
inclinaison_0 = 0

pos_0 = [xhat[0],yhat[0]]
angle_0 = 0

moto = Moto(0.3, 0.5, 400, 2, pos_0, vitesse=v_0)


def next_traj(t, inclinaison, angle_0, pos_0, moto):

    dt = 0.001



    d_inclinaison = 0.1
    nb_inclinaison = np.pi/2
    inclinaisons = [inclinaison - np.pi/3,inclinaison - np.pi/6, inclinaison,inclinaison + np.pi/6, inclinaison + np.pi/3]
    inclinaisons = np.arange(inclinaison - nb_inclinaison, inclinaison + nb_inclinaison, d_inclinaison)

##########################################################################################################
    # print('inclinaison envoyé : ', inclinaison)
    # plt.figure()

    # plt.scatter(range(len(inclinaisons)),inclinaisons)
    # plt.title(inclinaison)
    # plt.show()
##########################################################################################################



    moto.acceleration = 0
    angle_courant = np.arctan2(image_par_fhat(pos_0[0] + 0.1) - image_par_fhat(pos_0[0]) , 0.1)

    resultats_trajs = {}  # inclinaison : x_prevus, y_prevus, angle_moto

    for inclinaison in inclinaisons:
        valide = True
        current_time = 0

        moto.angle = angle_0
        moto.position = pos_0.copy()
        moto.inclinaison = inclinaison

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
            moto_angle = moto.angle

            # if circuit_test.verif_valide(pos):
            #     break

            current_time += dt
 
        angle_traj = np.arctan2(y_prevus[-1] - y_prevus[0], x_prevus[-1] - x_prevus[0])
        if abs(angle_traj - angle_courant) < np.pi/2:
            # print('Trajectoire : ', angle_traj)
            # print('Voulu : ', angle_courant)
            resultats_trajs[inclinaison] = (x_prevus, y_prevus, angle_traj-np.pi/2)

##########################################################################################################
    XXX =[]
    YYY = []
    for inclinaison in resultats_trajs.keys():
        for lx in resultats_trajs[inclinaison][0]:
            XXX.append(lx)
        for ly in resultats_trajs[inclinaison][1]:
            YYY.append(ly)
    
    # plt.figure()

    # plt.scatter(x_positions,y_positions)
    # plt.scatter(XXX,YYY)
    # plt.plot(xhat,yhat,c='r')
    # plt.show()
##########################################################################################################
        
    resultats_moindre_carre = {}    # moindre_carre : inclinaison

    for inclinaison in resultats_trajs.keys():


        x_prevus = resultats_trajs[inclinaison][0]
        y_prevus = resultats_trajs[inclinaison][1]



        y_ms = image_par_fhat(x_prevus)
        md = 0  

        
        angle_prevu = np.arctan2(y_prevus[-1]-y_prevus[0], x_prevus[-1]-x_prevus[0])
        angle_voulu = np.arctan2(y_ms[-1]-y_ms[0], x_prevus[-1]-x_prevus[0])

        for y,ym in zip(y_prevus,y_ms):
            md += (y - ym)**2

        critere = md
        critere = (angle_prevu - angle_voulu + 2*np.pi) % (2*np.pi)
        critere = angle_prevu - angle_voulu 

        resultats_moindre_carre[abs(critere)] = inclinaison, y_ms, x_prevus
    
    # plt.figure()
    # plt.plot([resultats_moindre_carre[i][0] for i in resultats_moindre_carre.keys()],resultats_moindre_carre.keys())
    # plt.show()

    inclinaison_optimal = resultats_moindre_carre[min(list(resultats_moindre_carre.keys()))][0]
    y_ms_opti = resultats_moindre_carre[min(list(resultats_moindre_carre.keys()))][1]
    x_suivant = resultats_trajs[inclinaison_optimal][0][-1]
    y_suivant = resultats_trajs[inclinaison_optimal][1][-1]
    angle_suivant = resultats_trajs[inclinaison_optimal][2]


##########################################################################################################
    # print('inclinaison calcule : ', inclinaison_optimal)
    # plt.figure()

    # plt.scatter(x_positions,y_positions)
    # plt.scatter(XXX,YYY)
    # plt.scatter(resultats_trajs[inclinaison_optimal][0],resultats_trajs[inclinaison_optimal][1], color='k')
    # #plt.scatter(resultats_trajs[inclinaison_optimal][0],y_ms_opti, color='r')
    # plt.plot(xhat,yhat,c='r')
    # plt.xlabel('x (m)')
    # plt.ylabel('y (m)')
    # plt.show()
##########################################################################################################


    return  inclinaison_optimal, x_suivant, y_suivant, resultats_trajs[inclinaison_optimal][0], resultats_trajs[inclinaison_optimal][1], angle_suivant





###############################################################################################################
corde_x = np.linspace(pos_0[0], pos_0[0]+5, 100)
corde_y = corde(corde_x[0], corde_x[-1], corde_x, image_par_fhat(corde_x[0]), image_par_fhat(corde_x[-1]))

inclinaison_0 = find_inclinaison(corde_x, corde_y)
inclinaison_theorique = [inclinaison_0]
inclinaison_theorique.append(find_inclinaison(corde_x, corde_y))
###############################################################################################################



t_simu = 0.7
t_simus = [0.3]
t_simus = np.arange(0.3, .5, 0.1)

resultats = {}


for t_simu in tqdm(t_simus):

    inclinaison_opts = [inclinaison_0]
    x_opt = [pos_0[0]]
    y_opt = [pos_0[1]]
    angles = [angle_0]
    t_total = [0]

    x_suivants = [pos_0[0]]
    

    while x_opt[-1] < 40 or y_opt[-1] >= 0:
        inclinaison_opt, x_suivant, y_suivant, x, y, angle = next_traj(t_simu, inclinaison_opts[-1],angles[-1], [x_opt[-1], y_opt[-1]], moto)

        corde_x = np.linspace(x_suivant, x_suivant+2, 100)
        corde_y = corde(corde_x[0], corde_x[-1], corde_x, image_par_fhat(corde_x[0]), image_par_fhat(corde_x[-1]))


        #print('inclinaison', inclinaison_opt)
        # print('angle de la moto : ',moto.angle)
        inclinaison_opts.append(inclinaison_opt)
        x_suivants.append(x_suivant)
        x_opt = x_opt + x
        y_opt = y_opt + y
        angles.append(angle)
        t_total.append(t_total[-1]+t_simu)

    y_ms = image_par_fhat(x_opt)
    md = 0  

    for i in range(len(y_ms)):
        if i > 10 : 
            if x_opt[i] - x_opt[i-10] < 0:
                md+=100000
        md += (y_opt[i] - y_ms[i])**2

    critere = md

    resultats[critere] = x_opt, y_opt, inclinaison_opts, t_simu, t_total
    # plt.figure()
    # for mur in murs_interieurs:
    #     plt.plot(mur.x_points,mur.y_points,'g')
    # for mur in murs_exterieurs:
    #     plt.plot(mur.x_points,mur.y_points,'c')

    # plt.scatter(x_positions,y_positions)
    # plt.plot(xhat,yhat,c='r')

    # plt.scatter(x_opt,y_opt[:len(x_opt)], c='k')
    # plt.title(t_simu)

    # plt.figure()
    # plt.plot(t_total,inclinaison_opts)
    # plt.show()


x_opt, y_opt, inclinaison_opts, t_simu, t_total = resultats[min(resultats.keys())]















temps = np.linspace(0,30, len(x_opt))


fitting_x = np.polyfit(temps, x_opt ,15) 
function_x = np.poly1d(fitting_x)

fitting_y = np.polyfit(temps, y_opt ,15) 
function_y = np.poly1d(fitting_y)




fitting_inclin = np.polyfit(t_total, inclinaison_opts ,6) 
function_inclin = np.poly1d(fitting_inclin)

################################################################################################################""

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

plt.scatter(x_opt,y_opt[:len(x_opt)], c='k')
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
plt.plot(temps,x_opt)
plt.plot(temps,function_x(temps))
plt.title('x')

plt.figure()
plt.plot(temps,y_opt)
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
