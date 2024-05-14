import matplotlib.pyplot as plt
from structure import*


circuit_test= Circuit([Mur((0,0),(0,1)), Mur((0,1),(1,1)), Mur((1,1),(1,0))], [Mur((-1,0),(-1,2)), Mur((-1,2),(2,2)), Mur((2,2),(2,0))],[[-1,0],[0,0]], [[1,0],[2,0]])

circuit_test.affichage()

