

class Mur:
    """Créé un mur"""

    def __init__(self, debut, fin) -> None:
        """Initialise le mur avec des coordonées début et fin"""
        self.debut = debut                     # Vecteur de position début du mur
        self.fin = fin                         # Vecteur de position fin du mur



class Vehicule:
    """Créé un vhécule"""
    
    def __init__(self, nb_roue, pos_roue, centre_gravite, masse, largeur, longueur) -> None:
        """Initialise une voiture avec son repère local
                    y
                    ^
                    |
                    |
             long --⟥---------⟤ (<- position roues - aux coins par ex)
                    |          |
                    |          |
                    |     +    |
                    |    Cg    |
                    |          |
                    ⟥---------⟤----------> x
                 (0,0)        larg
        """
        self.nb_roue = nb_roue                 # Nombre de contact
        self.pos_roue = pos_roue               # Position des roues dans le repère local
        self.centre_gravite = centre_gravite   # Position du centre de gravtité dans le repère local
        self.masse = masse                     # Masse du véhicule
        self.largeur = largeur                 # Largeur du véhicule
        self.longueur = longueur               # Longueur du véhicule
