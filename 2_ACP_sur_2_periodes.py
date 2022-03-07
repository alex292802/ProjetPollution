# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 14:28:36 2022

@author: aberg
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from datetime import date

# Lecture et préparation des données
chemin = '/conversion'  # Entrer ici le répertoire du fichier OPC à traiter
STATION_1 = pd.read_pickle('Marseille_long_Champ_JOURNALIER.dataframe')


X = STATION_1.drop(["Heure", "Monoxyde d'azote (NO)", 'Ozone (O3)', "Dioxyde d'azote (NO2)",
       'Dioxyde de carbone', 'Dioxyde de soufre (SO2)', 'Méthane',
       'Nombre de particules', "Oxydes d'azote (NOX)"], axis=1)
print("Colonnes analysées par l'ACP", X.columns)

# On récupére l'index de tous les nan puis on les enleve
index_nan = []
for i in range(len(X)):
    for j in range (X.shape[1]):
        if (np.isnan(X.iloc[i, j])):
            index_nan.append(i)
X = X.dropna()

#On va ensuite effectuer une ACP
# instanciation
sc = StandardScaler()

# transformation – centrage-réduction
Z = sc.fit_transform(X)
Z=X
# instanciation
acp = PCA(svd_solver='full')

# calculs des coordonnées
coord = acp.fit_transform(Z)
coord = pd.DataFrame(coord)
coord.index = X.index

#test des bâtons brisés 
n = X.shape[0] 
p = X.shape[1]
eigval = (n-1)/n*acp.explained_variance_
bs = 1/np.arange(p,0,-1) 
bs = np.cumsum(bs) 
bs = bs[::-1]
print("Test des batons brisés")
print(pd.DataFrame({'Val.Propre':eigval,'Seuils':bs}))

#Visualisation des différentes variances expliquées selon la dimension
eig = pd.DataFrame(
    {
        "Dimension" : ["Dim" + str(x + 1) for x in range(6)], 
        "Variance expliquée" : acp.explained_variance_,
        "% variance expliquée" : np.round(acp.explained_variance_ratio_ * 100),
        "% cum. var. expliquée" : np.round(np.cumsum(acp.explained_variance_ratio_) * 100)
    }
)
eig.plot.bar(x = "Dimension", y = "% variance expliquée") # permet un diagramme en barres
plt.show()

#1er intervalle de temps  
d0 = date(2017, 1, 1)
jour_deb1 = 1
mois_deb1 = 11
annee_deb1 = 2019
jour_fin1 = 1
mois_fin1 = 3
annee_fin1 = 2020
deb1 = date(annee_deb1, mois_deb1, jour_deb1)
fin1 = date(annee_fin1, mois_fin1, jour_fin1)
index_deb1 = (deb1 - d0).days # nombre de jour à partir du 1 Janvier 2017
index_fin1 = (fin1-d0).days  # nombre de jour à partir du 1 Janvier 2017

#2eme intervalle de temps
jour_deb2 = 1
mois_deb2 = 5
annee_deb2 = 2020
jour_fin2 = 1
mois_fin2 = 9
annee_fin2 = 2020
deb2 = date(annee_deb2, mois_deb2, jour_deb2)
fin2 = date(annee_fin2, mois_fin2, jour_fin2)
index_deb2 = (deb2 - d0).days # nombre de jour à partir du 1 Janvier 2017
index_fin2 = (fin2-d0).days  # nombre de jour à partir du 1 Janvier 2017

#Liste des index des points que l'on considére 
index1 = [i for i in range(index_deb1, index_fin1)]
index2 = [i for i in range(index_deb2, index_fin2)]

#On retire les nan de ces listes
index_sans_nan1=[]
for i in range(len(index1)):
    if not (index1[i] in index_nan):
        index_sans_nan1.append(index1[i])        
index_sans_nan2=[]
for i in range(len(index2)):
    if not (index2[i] in index_nan):
        index_sans_nan2.append(index2[i])


#Affichage des points et de la légende
fig, ax = plt.subplots()

label1="Hiver entre le "+str(jour_deb1)+"/"+str(mois_deb1)+"/"+str(annee_deb1)+" et "+str(jour_fin1)+"/"+str(mois_fin1)+"/"+str(annee_fin1)
for i in range (len(index_sans_nan1)):       
    ax.scatter(coord.loc[index_sans_nan1[i]][0], coord.loc[index_sans_nan1[i]][1], color='blue',label=label1)
    label1 = "_nolegend_"

label2="Eté entre le "+str(jour_deb2)+"/"+str(mois_deb2)+"/"+str(annee_deb2)+" et "+str(jour_fin2)+"/"+str(mois_fin2)+"/"+str(annee_fin2)
for i in range (len(index_sans_nan2)):       
    ax.scatter(coord.loc[index_sans_nan2[i]][0], coord.loc[index_sans_nan2[i]][1], color='red',label=label2)
    label2 = "_nolegend_"
    
plt.xlabel('Dimension 1 ('+str(eig.loc[0][2])+"%)" )
plt.ylabel('Dimension 2 ('+str(eig.loc[1][2])+"%)")
plt.title('ACP (été/hiver)')
plt.axhline(y = 0, linewidth = .5)
plt.axvline(x = 0, linewidth = .5)
ax.legend()