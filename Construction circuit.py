from structure import*
import matplotlib.pyplot as plt

class Circuit:
    def __init__(self, mursInterieurs, murExterieurs, ligneDepart, ligneArrivee)->None:
        self.mursInte = mursInterieurs
        self.mursExte = mursExterieurs
        self.Depart=ligneDepart
        self.Arrivee=ligneArrivee
    def __affichage__(self, self.mursInte, self.mursExte):
        plt.figure()
        for traceMur in self.mursInte:
            plt.plot(traceMur.debut,traceMur.fin,'b-')
        for traceMur in self.mursExte:
            plt.plot(traceMur.debut, traceMur.fin, 'r-')
        plt.plot(Depart[0], Depart[1], 'b--')
        plt.plot(Arrivee[0], Arrivee[1], 'g--')
        plt.show()
    

