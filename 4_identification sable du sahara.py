# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:28:47 2022

@author: aberg
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

chemin='/conversion' #Entrer ici le répertoire du fichier OPC à traiter
STATION_1=pd.read_pickle('MARSEILLE_LONGCHMAP_HEURE_COMPLET.dataframe')
STATION_2=pd.read_pickle("AIX_ART_HEURES.dataframe")
STATION_3=pd.read_pickle('SAINT_LOUIS_HEURE.dataframe')

Big_data=pd.merge(STATION_1,STATION_2,on=['Heure'])#on a fait la jointure de deux dataframes qui ont une même colonne commune ici 'heure', attention, si les données heures ne sont pas communes, les données ne sont pas réecopiées
Big_data=pd.merge(Big_data,STATION_3,on=['Heure'])
    
Big_data['Particules PM10 corr']=Big_data[['Particules PM10_x','Particules PM10_y']].min(axis=1)
Big_data['Particules PM2,5 corr']=Big_data[['Particules PM2,5_x','Particules PM2,5_y', 'Particules PM2,5']].min(axis=1)
Big_data['Particules PM1 corr']=Big_data[['Particules PM1_x','Particules PM1_y', 'Particules PM10']].min(axis=1)

X = Big_data.drop(["Dioxyde d'azote (NO2)",
'Dioxyde de carbone', 'Dioxyde de soufre (SO2)', 'Méthane',
"Monoxyde d'azote (NO)", 'Nombre de particules',
"Oxydes d'azote (NOX)", 'Ozone (O3)', 'Particules PM1_x',
'Particules PM10_x', 'Particules PM2,5_x',
 'Particules PM10_y', 'Particules PM2,5_y',
'Particules PM1_y',
'Particules PM10', 'Particules PM2,5'], axis=1)

def index_dates(jour_deb,mois_deb,annee_deb,jour_fin,mois_fin,annee_fin):
    d0 = date(2017, 1, 1)
    deb1 = date(annee_deb, mois_deb, jour_deb)
    fin1 = date(annee_fin, mois_fin, jour_fin)
    index_deb = (deb1 - d0).days*24 # nombre de jour à partir du 1 Janvier 2017
    index_fin = (fin1-d0).days*24  # nombre de jour à partir du 1 Janvier 2017
    return (index_deb,index_fin)

def affichage(X,deb,fin,particule_etudie):
    particule=X[particule_etudie]
    TREND_GLOBAL=48
    abcisse=X['Heure'].iloc[deb:fin]
    ordonnee=particule.iloc[deb:fin]
    ordonnee_lissee=particule.rolling(TREND_GLOBAL).mean().iloc[deb:fin]
    plt.plot(abcisse,ordonnee,'darkorchid')
    plt.plot( abcisse,ordonnee_lissee,'crimson',label='Trend')
    plt.setp(plt.gca().xaxis.get_majorticklabels(),
         'rotation', 90)
    plt.show()
    return ordonnee_lissee
           
(deb,fin)=index_dates(22,4,2019,23,4,2019)

#Biomasse=affichage(X,deb,fin,'Black Carbon (combustion de biomasse)')
#moitié nan
#Fossile=affichage(X,deb,fin,'Black Carbon (combustion de fossiles)')
#moitié nan
#BC_25=affichage(X,deb,fin, 'Black Carbon (dans les PM2.5)')
#quart de nan

#PM1=affichage(X,deb,fin,'Particules PM1 corr')
#200 nan
#PM_25=affichage(X,deb,fin,'Particules PM2,5 corr')
#100 nan
#PM_10=affichage(X,deb,fin,'Particules PM10 corr')
#100 nan

PM_25=X['Particules PM2,5 corr'].iloc[deb:fin]
PM_10=X['Particules PM10 corr'].iloc[deb:fin]



#Calcul du nombre de nan
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

x=X['Heure'].iloc[deb:fin]
rapport=PM_25/PM_10
diff=(PM_10-PM_25)
var=(PM_10-PM_25)/PM_10
diff_quadra=(PM_10-PM_25)**2
plt.plot(x,diff_quadra,color='darkorchid')
plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 90)
plt.title('(PM10-PM2,5)**2')
plt.show()



