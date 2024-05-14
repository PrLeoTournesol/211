import matplotlib.pyplot as plt
from structure import*

class Circuit:
    def __init__(self, mursInterieurs, mursExterieurs, ligneDepart, ligneArrivee)->None:
        self.mursInte = mursInterieurs
        self.mursExte = mursExterieurs
        self.Depart=ligneDepart
        self.Arrivee=ligneArrivee
    
    def affichage(self):
        plt.figure()
        for traceMur in self.mursInte:
            plt.plot(traceMur.debut,traceMur.fin,'b-')
        for traceMur in self.mursExte:
            plt.plot(traceMur.debut, traceMur.fin, 'r-')
        plt.plot(self.Depart[0], self.Depart[1], 'b--')
        plt.plot(self.Arrivee[0], self.Arrivee[1], 'g--')
        plt.show()

circuit_test= Circuit([Mur((0,0),(0,1)), Mur((0,1),(1,1)), Mur((1,1),(1,0))], [Mur((-1,0),(-1,2)), Mur((-1,2),(2,2)), Mur((2,2),(2,0))],[(-1,0),(0,0)], [(1,0),(2,0)])

circuit_test.affichage()

