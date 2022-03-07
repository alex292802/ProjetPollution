# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 20:09:37 2022

Script: Heatmap des pollutions au niveau horraire. 

@author: Benjamin
"""

import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt


#Chargement des données 


STATION_1=pd.read_csv(r'C:/Users/Benjamin/Desktop/Fichiers csv/Longchamp.csv')
STATION_2=pd.read_csv(r'C:/Users/Benjamin/Desktop/Fichiers csv/Aix.csv')
STATION_3=pd.read_csv(r'C:/Users/Benjamin/Desktop/Fichiers csv/Saint_Louis.csv')


#Nettoyage des données 

Big_data=pd.merge(STATION_1,STATION_2,on=['Heure'])#on a fait la jointure de deux dataframes qui ont une même colonne commune ici 'heure', attention, si les données heures ne sont pas communes, les données ne sont pas réecopiées
Big_data=pd.merge(Big_data,STATION_3,on=['Heure'])
print(Big_data.columns)

Big_data['Particules PM10 corr']=Big_data[['Particules PM10_x','Particules PM10_y']].min(axis=1)
Big_data['Particules PM2,5 corr']=Big_data[['Particules PM2,5_x','Particules PM2,5_y', 'Particules PM2,5']].min(axis=1)
Big_data['Particules PM1 corr']=Big_data[['Particules PM1_x','Particules PM1_y', 'Particules PM10']].min(axis=1)

df = Big_data.drop(["Dioxyde d'azote (NO2)",
'Dioxyde de carbone', 'Dioxyde de soufre (SO2)', 'Méthane',
"Monoxyde d'azote (NO)", 'Nombre de particules',
"Oxydes d'azote (NOX)", 'Ozone (O3)', 'Particules PM1_x',
'Particules PM10_x', 'Particules PM2,5_x',
 'Particules PM10_y', 'Particules PM2,5_y',
'Particules PM1_y',
'Particules PM10', 'Particules PM2,5'], axis=1)



#Transformation des dates en datetimes
df['Heure'] = pd.to_datetime(df['Heure'])

#Indexation du dataframe en fonction de la date
df = df.set_index('Heure')
 
#Filtre Période
df=df.loc['2019-04-20':'2019-04-24']
df=df.reset_index()
#Filtre Nan
df=df.dropna()

#Travail sur le dataframe (A partir du datetime, va récupérer la semaine considérée
#                            et va découper le datetime suivant le jour et la date,
#                               nouvel indexage en fonction de ces caractéristiques )
s = (df.groupby([df.Heure.dt.isocalendar().week,
                 df.Heure.dt.strftime('%Y-%m-%d'), 
                 df.Heure.dt.strftime('%H:00')])
       ['Particules PM10 corr'].mean()
       .rename_axis(index=['week','day','hour'])
    )

#Heatmap de ce dataframe
fig, axes = plt.subplots(2,figsize=(10,10))
for w, ax in zip(s.index.unique('week'), axes.ravel()):
    sns.heatmap(s.loc[w].unstack(level='day'), ax=ax)
    ax.set_title(f'Week {w}')