import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import csv

data = pd.read_csv (r'/Users/mac/Desktop/EIVP/Algo et programmation/EIVP_KM.csv', sep = ';')
print(data)


## Affichage graphique température en fonction du temps (à modifier --> trop d'intervals de temps : temps affichage graphique long

x=[]
y=[]

with open('/Users/mac/Desktop/EIVP/Algo et programmation/EIVP_KM.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=';')
    for i in plots:
        x.append(i[6])
        y.append(i[2])


plt.plot(x,y, marker='o')

plt.title('Data from the CSV File: temp and time')

plt.xlabel('time')
plt.ylabel('temp')

# plt.show()