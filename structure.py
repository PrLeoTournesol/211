import numpy as np
import matplotlib.pyplot as plt

class Mur:
    """Créé un mur"""

    def __init__(self, debut, fin) -> None:
        """Initialise le mur avec des coordonées début et fin"""
        self.debut = debut                     # Vecteur de position début du mur
        self.fin = fin                         # Vecteur de position fin du mur

        self.x_points = [self.debut[0],self.fin[0]]
        self.y_points = [self.debut[1],self.fin[1]]

        self.list_x = np.linspace(self.debut[0],self.fin[0], 20)
        self.list_y = np.linspace(self.debut[1],self.fin[1], 20)



class Circuit:
    def __init__(self, mursInterieurs, mursExterieurs, ligneDepart, ligneArrivee)->None:
        self.mursInte = mursInterieurs
        self.mursExte = mursExterieurs
        self.Depart=ligneDepart
        self.Arrivee=ligneArrivee
    
    def affichage(self):
        plt.figure()
        for traceMur in self.mursInte:
            plt.plot(traceMur.x_points,traceMur.y_points,'b-')
        for traceMur in self.mursExte:
            plt.plot(traceMur.x_points,traceMur.y_points, 'r-')
        plt.plot([self.Depart[0][0],self.Depart[1][0]], [self.Depart[0][1],self.Depart[1][1]], 'b--')
        plt.plot([self.Arrivee[0][0],self.Arrivee[1][0]], [self.Arrivee[0][1],self.Arrivee[1][1]], 'g--')
        plt.show()

    def verif_valide(self,coord):
        x,y = coord

        exterieur = ((x < min([min(mur.x_points) for mur in self.mursExte])) or (x > max([max(mur.x_points) for mur in self.mursExte]))) or (y < min([min(mur.y_points) for mur in self.mursExte])) or (y > max([max(mur.y_points) for mur in self.mursExte]))   
        interieur = (x > min([min(mur.x_points) for mur in self.mursInte])) and (x < max([max(mur.x_points) for mur in self.mursInte])) and (y > min([min(mur.y_points) for mur in self.mursInte])) and (y < max([max(mur.y_points) for mur in self.mursInte]))
        
        if exterieur or interieur:
            return True
        return False


class Moto:
    """Créé une moto"""
    
    def __init__(self, rayon_roue, y_g, masse, empattement, pos_initiale = [0,0] ,vitesse = 0, inclinaison = 0) -> None:
        """Initialise une voiture avec son repère local
                    y
                    ^
                    |
                    |
             empat  |     |  <- Roues 
                    |     |     
                    |     |     
                    |     +    
                    |     | Cg    
                    |     |     
                    |-----|-------------> x
                        (0,0)
        """
        
        # Paramètres géométriques : 
        self.rayon_roue = rayon_roue                # Rayon des roues  [m]
        self.masse = masse                          # Masse du véhicule  [kg]
        self.empattement = empattement              # Longueur du véhicule  [m]
        self.pos_centre_gravite = y_g               # Position du centre de gravtité dans le repère local suivant y  [m]

        # Paramètres dynamique
        self.vitesse = vitesse                      # Vitesse du centre de gravité   [m/s]
        self.vitesse_angle = 0                      # Vitesse angulaire de la moto dans le repère global  [rad/s]
        self.angle = 0                              # Angle de rotation de la moto dans le repère global [rad]
        self.rot_matrice = np.zeros((2,2))          # Matrice de rotation
        self.position = pos_initiale               # [xG,yG] dans le repère de la moto 
        self.distance_totale = 0                    # [xG,yG] dans le repère de la moto 

        self.acceleration = 0                       # acceleration de la moto dans le repère de la moto [m/s2]
        self.vitesse_inclinaison = 0                # vitesse de l'inclinaison de la moto [rad/s]
        self.rayon_courbure = np.inf                # Rayon de courbure à un instant t (r = inf en ligne droite) [m]

        self.inclinaison = inclinaison              # Inclinaison de la moto [rad]
        
    
    def calcul_rayon_courbure(self) -> float:
        """
        Calcul le rayon de courbure en connaissant la vitesse et l'angle d'inclinaison : 
        http://albert25.free.fr/motard/physique_explications.html
        """
        if abs(self.inclinaison) > 1e-2:
            self.rayon_courbure = self.vitesse**2 / (9.81 * np.tan(self.inclinaison))
        else:
            self.rayon_courbure = np.inf

        return self.rayon_courbure
    
    def update_vitesse(self, dt) -> None:
        self.vitesse = self.vitesse + dt * self.acceleration

    def update_position(self, dt) -> None:
        self.position[0] = self.position[0] + dt * (-np.sin(self.angle)) * self.vitesse
        self.position[1] = self.position[1] + dt * (np.cos(self.angle)) * self.vitesse
    
    def update_inclinaison(self, dt) -> None:
        self.inclinaison = self.inclinaison + dt * self.vitesse_inclinaison

    def calcul_vitesse_angle(self) -> None:
        if self.rayon_courbure < 1e3:
            self.vitesse_angle = self.vitesse/self.rayon_courbure
        else:
            self.vitesse_angle = 0

    def update_angle(self,dt):
        self.angle = self.angle + dt * self.vitesse_angle

    def calcul_rotation_matrice(self):
        self.rot_matrice[0,0] = np.cos(self.angle)
        self.rot_matrice[0,1] = -np.sin(self.angle)
        self.rot_matrice[1,0] = np.sin(self.angle)
        self.rot_matrice[1,1] = np.cos(self.angle)

    def changement_repere(self, vecteur):
        return self.rot_matrice @ np.transpose(vecteur)

    def distance_parcourue(self, pos, pos_avant):
        self.distance_totale += ( (pos[0]-pos_avant[0])**2 + (pos[1]-pos_avant[1])**2 )**.5


    @property
    def vitesse(self):
        return self._vitesse

    @vitesse.setter
    def vitesse(self, value):
        self._vitesse = value

    @property
    def vitesse_inclinaison(self):
        return self._vitesse_inclinaison

    @vitesse_inclinaison.setter
    def vitesse_inclinaison(self, value):
        self._vitesse_inclinaison = value

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def inclinaison(self):
        return self._inclinaison

    @inclinaison.setter
    def inclinaison(self, value):
        self._inclinaison = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, liste):
        if isinstance(liste, list):
            self._position = liste



