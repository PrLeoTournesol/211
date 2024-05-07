import numpy as np

class Mur:
    """Créé un mur"""

    def __init__(self, debut, fin) -> None:
        """Initialise le mur avec des coordonées début et fin"""
        self.debut = debut                     # Vecteur de position début du mur
        self.fin = fin                         # Vecteur de position fin du mur



class Moto:
    """Créé une moto"""
    
    def __init__(self, rayon_roue, centre_gravite, masse, largeur, empattement, vitesse, braquage) -> None:
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
                 (0,0)   larg
        """
        
        self.rayon_roue = rayon_roue                # Rayon des roues
        self.braquage_avant = braquage              # Braquage
        self.centre_gravite = centre_gravite        # Position du centre de gravtité dans le repère local
        self.masse = masse                          # Masse du véhicule
        self.largeur = largeur                      # Largeur du véhicule
        self.empattement = empattement              # Longueur du véhicule
        self.vitesse_G = [vitesse,np.tan(braquage) * centre_gravite[1] / empattement]  # Vitesse du centre de gravité [v,theta]

    def verification_glissement(self) -> bool:
        """Vérifie qu'il n'y ai pas de glissement de la roue avant pour f (frottement roue sol)"""
        f = 1
        force_centrifuge = self.masse * self.vitesse_G[0]**2 / np.sin(self.braquage_avant) * self.empattement
        poids = self.masse * 9.81
        force_normale_sol = (self.empattement - self.centre_gravite[1])/self.empattement * poids          # Force normale sur la roue avant

        force_frottement = f * force_normale_sol

        return force_centrifuge > force_frottement

        
        

