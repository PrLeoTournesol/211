import numpy as np

class Mur:
    """Créé un mur"""

    def __init__(self, debut, fin, rayon_courbure = None) -> None:
        """Initialise le mur avec des coordonées début et fin"""
        self.debut = debut                     # Vecteur de position début du mur
        self.fin = fin                         # Vecteur de position fin du mur

        self.x_points_mur = np.linspace(debut[0], fin[0], 1000)
        self.y_points_mur = np.linspace(debut[1], fin[1], 1000)




class Moto:
    """Créé une moto"""
    
    def __init__(self, rayon_roue, y_g, masse, empattement, vitesse = 0, braquage = 0) -> None:
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
        self.braquage_avant = braquage              # angle de braquage de la roue avant   [rad]
        self.angle_rotation = np.tan(braquage) * y_g / empattement # Rotation dans le repère de la moto, lié au braquage  [rad]
        
        self.position_moto = [0,0,0]                # [xG,yG,alpha_mot] avec alpha_mot angle entre la roue arrière et le repère global

    def verification_glissement(self) -> bool:
        """Vérifie qu'il n'y ai pas de glissement de la roue avant pour f (frottement roue sol)"""
        f = 1
        rayon_courbure = self.empattement / np.sin(self.braquage_avant)
        force_centrifuge = self.masse * self.vitesse**2 / rayon_courbure
        poids = self.masse * 9.81
        force_normale_sol = (self.empattement - self.pos_centre_gravite)/self.empattement * poids     # Force normale sur la roue avant

        force_frottement = f * force_normale_sol
        print(force_centrifuge)
        print(force_frottement)

        return force_centrifuge > force_frottement
    

    @property
    def vitesse(self):
        return self._vitesse

    @vitesse.setter
    def vitesse(self, value):
        self._vitesse = value

    @property
    def braquage(self):
        return self._braquage

    @braquage.setter
    def braquage(self, value):
        self._braquage = value



moto = Moto(0.3, 0.5, 400, 1, 2, np.pi/3)

print(moto.verification_glissement())
    
    

        
        

