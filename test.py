import matplotlib.pyplot as plt

class Circuit:
    def _init_(self, mursInterieurs, mursExterieurs, ligneDepart, ligneArrivee)->None:
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

#test2
