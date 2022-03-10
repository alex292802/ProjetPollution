# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 12:18:45 2022

@author: aberg

Script : Ce programme permet de calculer le coefficient de pearson entre 2 
stations en faisant la moyenne des coefficients de Pearson pour chaque features
"""
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

#On récupére les données des 3 stations
chemin='/conversion' #Entrer ici le répertoire du fichier OPC à traiter
STATION_1=pd.read_pickle('Marseille_long_Champ_JOURNALIER.dataframe')
STATION_2=pd.read_pickle("Aix Ecole d'Art_JOURNALIER.dataframe")
STATION_3=pd.read_pickle('Avignon_Mairie_JOURNALIER.dataframe')
STATION_1_NOM='Marseille long Champ'
STATION_2_NOM="Aix Ecole d'Art"
STATION_3_NOM='Avignon Mairie'

#On crée un dataframe global avec les données des 3 stations
Big_data=pd.merge(STATION_1,STATION_2,on=['Heure'])#on a fait la jointure de deux dataframes qui ont une même colonne commune ici 'heure', attention, si les données heures ne sont pas communes, les données ne sont pas réecopiées
Big_data=pd.merge(Big_data,STATION_3,on=['Heure'])

#On récupère les features qui nous intéressent
PM25_1=Big_data["Particules PM2,5_x"]
PM25_2=Big_data["Particules PM2,5_y"]
PM25_3=Big_data["Particules PM2,5"]
PM10_1=Big_data["Particules PM10_x"]
PM10_2=Big_data["Particules PM10_y"]
PM10_3=Big_data["Particules PM10"]
PM1_1=Big_data["Particules PM1_x"]
PM1_3=Big_data["Particules PM1_y"]

#Pour chaque couple de station, on crée une liste contenant les features 
#qui nous intéressent
#Station 1 et 2
L1=[PM25_1.copy(),PM25_2.copy(),PM10_1.copy(),PM10_2.copy()]
#Station 2 et 3
L2=[PM25_2.copy(),PM25_3.copy(),PM10_2.copy(),PM10_3.copy()]
#Station 1 et 3
L3=[PM25_1.copy(),PM25_3.copy(),PM10_1.copy(),PM10_3.copy(),PM1_1.copy(),PM1_3.copy()]

#Cette fonction calcule le coefficient de pearson entre 2 listes tout en 
#supprimant les nan si ils existent
def coefficient_pearson(L):
    index_nan=[]
    for i in range(len(L)):
        for j in range(len(L[i])):
            if (np.isnan(L[i][j])):
                index_nan.append(j)
    index_nan=set(index_nan)          
    for i in range(len(L)):        
        L[i].drop(index_nan,inplace=True)
    pearson=0
    for i in range (0,len(L),2):
        pearson+=pearsonr(L[i],L[i+1])[0]
    pearson=pearson/(len(L)/2)
    return pearson
    
    
print("Le coefficient de Pearson entre les stations "+STATION_1_NOM+" et "+STATION_2_NOM+" est "+str(coefficient_pearson(L1)))
print("Le coefficient de Pearson entre les stations "+STATION_2_NOM+" et "+STATION_3_NOM+" est "+str(coefficient_pearson(L2)))
print("Le coefficient de Pearson entre les stations "+STATION_1_NOM+" et "+STATION_3_NOM+" est "+str(coefficient_pearson(L3)))
print("Calculs effectués pour les données journalières")