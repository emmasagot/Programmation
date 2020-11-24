import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import csv

data = pd.read_csv (r'/Users/mac/Desktop/EIVP/Algo et programmation/EIVP_KM.csv', sep = ';')
# print(data)


## Affichage graphique température en fonction du temps

sent_at=[] #liste contenant tous les echantillons de temps
temp=[] #liste contenat tous les echantillons de température

#code permettant de "remplir" les listes précedemment crées :
with open('/Users/mac/Desktop/EIVP/Algo et programmation/EIVP_KM.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=';')
    for i in plots:
        sent_at.append(i[6])
        temp.append(i[2])

#fonction permettant de réduire l'intervalle d'étude en définissant la date de début (a) et la date de fin (b)
def intervalle(a,b):
    abs=[]
    ord=[]
    for i in range(sent_at.index(a),sent_at.index(b)):
        abs.append(sent_at[i])
        ord.append(temp[i])
    return abs,ord

#affichage graphique pour valeurs choisies
a='2019-08-21 11:46:04 +0200' #date de début choisie
b='2019-08-25 11:45:54 +0200' #date de fin choisie
x,y=intervalle(a,b)

plt.plot(x,y, marker='o')

plt.title('Data from the CSV File: temp and time')

plt.xlabel('time')
plt.ylabel('temp')

plt.show()


