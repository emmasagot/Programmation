import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import csv

data = pd.read_csv (r'/Users/mac/Desktop/EIVP/Algo et programmation/EIVP_KM.csv', sep = ';')
#print(data)

tableau_data=data.values #conversion du fichier csv en tableau numpy

## Affichage d'un graphique temp=f(sent_at)

x=[]
y=[]

#récupération des colonnes qui nous intéressent

temp=[]
sent_at=[]

for i in range (len(tableau_data)):
    temp.append(tableau_data[i][2])
    sent_at.append(tableau_data[i][6])

#fonction permettant de réduire l'intervalle d'étude en définissant la date de début (a) et la date de fin (b)

def intervalle(a,b):
    abs=[]
    ord=[]
    for i in range (sent_at.index(a),sent_at.index(b)):
        abs.append(sent_at[i])
        ord.append(temp[i])
    return abs, ord

#affichage graphique pour valeurs choisies

a='2019-08-20 11:46:11 +0200' #date de début choisie
b='2019-08-25 11:45:54 +0200' #date de fin choisie
x,y=intervalle(a,b)

plt.plot(x,y, marker='o')
plt.xlabel('temps')
plt.ylabel('température')
plt.title('température en fonction du temps')
plt.show()


