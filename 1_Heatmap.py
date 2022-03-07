# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Auteur: Benjamin Schmitt

Script: HeatMap d'une visualisation calendaire' Utilisation de données journalières.

Ceci est un script temporaire.
"""

import calplot#Librairie à installler avec pip
import pandas as pd

#Chargement des données
df=pd.read_csv(r'C:/Users/Benjamin/Desktop/Fichiers csv/Marseille_long_Champ_JOURNALIER_nor.csv')

#Transformation des dates en datetimes
df['Heure'] = pd.to_datetime(df['Heure'])

#Indexation du dataframe en fonction de la date
df = df.set_index('Heure')


#Filtre
df=df.loc['2017-6-1':'2021-6-10'] #Filtre les dates
df.dropna(inplace=True) #Supprime les dates pours lesquelles ily a un nan 



# Récupérations des Series de features pour la heatmpap

BlackCarbon_biomasse=pd.Series(df['Black Carbon (combustion de biomasse)'])
BlackCarbon_fossiles=pd.Series(df['Black Carbon (combustion de fossiles)'])
BlackCarbon_PM2_5=pd.Series(df['Black Carbon (dans les PM2.5)'])
PM10 = pd.Series(df['Particules PM10'])
PM1=pd.Series(df["Particules PM1"])  
PM2_5=pd.Series(df["Particules PM2,5"])  
NO2 = pd.Series(df["Dioxyde d'azote (NO2)"])
CO2= pd.Series(df["Dioxyde de carbone"])

CH4= pd.Series(df["Méthane"])
SO2=pd.Series(df["Dioxyde de soufre (SO2)"])
NO= pd.Series(df["Monoxyde d'azote (NO)"])
Nbr_particules=pd.Series(df['Nombre de particules'])          
NOX=pd.Series(df["Oxydes d'azote (NOX)"])      
O3= pd.Series(df["Ozone (O3)"])  



# Création des calendars heatmap

calplot.calplot(data=BlackCarbon_biomasse, cmap='coolwarm', suptitle='BlackCarbon_biomasse')
calplot.calplot(data=BlackCarbon_fossiles, cmap='coolwarm', suptitle='BlackCarbon_fossiles')
calplot.calplot(data=BlackCarbon_PM2_5, cmap='coolwarm', suptitle='BlackCarbon_PM2_5')
calplot.calplot(data=PM10, cmap='coolwarm', suptitle='Heatmap PM10')
calplot.calplot(data=PM1, cmap='coolwarm', suptitle='PM1')
calplot.calplot(data=PM2_5, cmap='coolwarm', suptitle='PM2_5')
calplot.calplot(data=NO2, cmap='coolwarm', suptitle="Dioxyde d'azote (NO2)")
calplot.calplot(data=CO2, cmap='coolwarm', suptitle="Dioxyde de carbone")
calplot.calplot(data=CH4, cmap='coolwarm', suptitle='Méthane')
calplot.calplot(data=SO2, cmap='coolwarm', suptitle="Dioxyde de soufre (SO2)")
calplot.calplot(data=NO, cmap='coolwarm', suptitle="Monoxyde d'azote (NO)")
calplot.calplot(data=Nbr_particules, cmap='coolwarm', suptitle='Heatmap Nbr_particules')
calplot.calplot(data=NOX, cmap='coolwarm', suptitle="Oxydes d'azote (NOX)")
calplot.calplot(data=O3, cmap='coolwarm', suptitle="Ozone (O3)")

df
