# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 13:15:52 2022

@author: aberg

Script: Ce programme permet de récupérer l'ensemble des données, les fusionner
en un dataset complet, d'abandonner les caractéristiques qui ne nous intéressent 
pas et d'enlever les nan. Il est ensuite possible de compléter les données 
en traçant la droite reliant les 2 points de chaque coté du trou de données puis 
d'afficher certaines caractéristiques de ce nouveau dataset obtenu (concentration
en PM1, PM10, PM25...)
        
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

#Travail de pérparation de la donnée
STATION_1=pd.read_pickle('Marseille_long_Champ_JOURNALIER.dataframe')
STATION_2=pd.read_pickle("Aix Ecole d'Art_JOURNALIER.dataframe")
STATION_3=pd.read_pickle('Avignon_Mairie_JOURNALIER.dataframe')

Big_data=pd.merge(STATION_1,STATION_2,on=['Heure'])
Big_data=pd.merge(Big_data,STATION_3,on=['Heure'])
    
Big_data['PM10 (méthode du min)']=Big_data[['Particules PM10_x','Particules PM10_y']].min(axis=1)
Big_data['PM2.5 (méthode du min)']=Big_data[['Particules PM2,5_x','Particules PM2,5_y', 'Particules PM2,5']].min(axis=1)
Big_data['PM1 (méthode du min)']=Big_data[['Particules PM1_x','Particules PM1_y', 'Particules PM10']].min(axis=1)

X = Big_data.drop(['Black Carbon (combustion de biomasse)',
       'Black Carbon (combustion de fossiles)',
       'Black Carbon (dans les PM2.5)', "Dioxyde d'azote (NO2)_x",
'Dioxyde de carbone', 'Dioxyde de soufre (SO2)', 'Méthane',
"Monoxyde d'azote (NO)_x", 'Nombre de particules',
"Oxydes d'azote (NOX)_x", 'Ozone (O3)_x', 'Particules PM1_x',
'Particules PM10_x', 'Particules PM2,5_x',
"Dioxyde d'azote (NO2)_y", "Monoxyde d'azote (NO)_y",
"Oxydes d'azote (NOX)_y", 'Particules PM10_y', 'Particules PM2,5_y',
"Dioxyde d'azote (NO2)", "Monoxyde d'azote (NO)",
"Oxydes d'azote (NOX)", "Ozone (O3)_y", 'Particules PM1_y',
'Particules PM10', 'Particules PM2,5'], axis=1)

#Fonction permettant de calculer l'index d'une date passée en paramètre par 
#rapport au 1er janvier 2017 (date du début des mesures)
def index_dates(jour_deb,mois_deb,annee_deb,jour_fin,mois_fin,annee_fin):
    d0 = date(2017, 1, 1)
    deb1 = date(annee_deb, mois_deb, jour_deb)
    fin1 = date(annee_fin, mois_fin, jour_fin)
    index_deb = (deb1 - d0).days # nombre de jour à partir du 1 Janvier 2017
    index_fin = (fin1-d0).days  # nombre de jour à partir du 1 Janvier 2017
    return (index_deb,index_fin)

#Fonction permettant de compléter les données en traçant la droite reliant 
#les 2 points de chaque coté du trou de données
def donnees_completes(X):
    for labels in X.columns:
        if labels!="Heure":
            particule=X[labels]
            intervalle_nan=[]
            index=0
            ind=0
            while(ind<len(particule)-2):
               ind+=1
               if (np.isnan(particule[ind])==True):
                   index=ind
                   liste_nan=[]
                   while (np.isnan(particule[index])==True):
                       liste_nan.append(index)
                       index+=1
                   intervalle_nan.append(liste_nan)
                   ind=index
            for i in range (len(intervalle_nan)):
                deb=intervalle_nan[i][0]-1
                fin=intervalle_nan[i][-1]+1
                l_intervalle=fin-deb-1
                pente=(particule.iloc[fin]-particule.iloc[deb])/l_intervalle
                pas=0
                for j in range (deb+1,fin):
                    pas+=1
                    particule.iloc[j]=particule.iloc[deb]+pas*pente

#Fonction permettant d'afficher la courbe associée à la particule de notre choix 
def affichage(X,deb,fin,particule_etudie):
    particule=X[particule_etudie]
    abcisse=X['Heure'].iloc[deb:fin]
    ordonnee=particule.iloc[deb:fin]
    plt.plot(abcisse,ordonnee,'darkorchid')
    plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 90)
    plt.ylabel('µg/m³')
    plt.title('Evolution de la quantité de '+particule_etudie)
    plt.show()

#Comptage du nombre de Nan
(deb,fin)=index_dates(1,4,2017,1,6,2017)
compteurs=[]
for labels in X.columns:
    if labels!="Heure":
        particule=X[labels]
        compteur=0
        for i in range (len(particule)):
           if (np.isnan(particule[i])==True):
               compteur+=1
        compteurs.append(compteur)
print (compteurs)

donnees_completes(X)
affichage(X,deb,fin,'PM1 (méthode du min)')




