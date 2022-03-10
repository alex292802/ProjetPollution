# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:57:51 2022

@author: Alexandre

Script : Ce programme a pour objectif d’étudier la potentielle séparation de 
2 pics de pollution. En effet, les pics de pollution sont de différentes natures 
(épisode du Sahara, feu de forêt… ). Nous avons analysé les composantes du pic 
et les particules majoritaires afin de savoir ce qu’il s’était passé. Puis nous 
avons réalisé une ACP pour voir si il était possible de séparer un pic de 
pollution d’un autre et ainsi identifier un événement du type sable du Sahara.
Enfin, nous avons réalisé une analyse de Fourier (uniquement du fondamental) 
en considérant l’intervalle [J-1, J+1] avec J le jour où il y a eu le pic de 
pollution.
"""
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#classe pour l'ACP 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from datetime import datetime,timedelta
import matplotlib
from scipy.fft import fft, ifft
def pareto(data) :
    from matplotlib.ticker import PercentFormatter
    y = list(data)
    x = range(len(data))
    ycum = np.cumsum(y)/sum(y)*100
    fig, ax = plt.subplots()
    ax.bar(x,y,color="yellow")
    ax2 = ax.twinx()
    ax2.plot(x,ycum, color="C1", marker="D", ms=7)
    ax2.axhline(y=80,color="r")#Def seuil
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax.tick_params(axis="y", colors="C0")
    ax2.tick_params(axis="y", colors="C1")
    plt.ylim(0,110)
    plt.show()
    
##Travail de pérparation de la donnée
STATION_1=pd.read_pickle('MARSEILLE_LONGCHMAP_HEURE_COMPLET.dataframe')
STATION_2=pd.read_pickle("AIX_ART_HEURES.dataframe")
STATION_3=pd.read_pickle('SAINT_LOUIS_HEURE.dataframe')

Big_data=pd.merge(STATION_1,STATION_2,on=['Heure'])
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
df=df.loc['2019-01-01':'2019-12-31']
df=df.reset_index()

#Filtre Nan
df=df.dropna()

#Filtres Pic
df["Diff carrés"]=(df['Particules PM10 corr']-df['Particules PM2,5 corr'])**2
filtered_df= df[ (df['Diff carrés'] >= 1500)] 
filtered_df.info()

#Histogramme illustrant la répartition de ([PM10]-[PM2.5])^2 sur l'année 2019
fig, ax = plt.subplots()
fig=sns.histplot(df['Diff carrés'])
ax.set_xlim(1,2000)
fig.figure.suptitle("Répartition de ([PM10]-[PM2.5])^2 sur l'année 2019", fontsize = 12)

#On va créer une liste contenant les jours où on a eu un pic pour les
# labels de l'ACP
#On crée aussi une liste contenant le jour d'avant et après  chaque jour où 
#il y a eu un pic pour le filtrage
filtered_df_heures=filtered_df["Heure"]
jours_pic=[] #jours pics
jours_filtrage=[] #1 jour après le pics et 1 jour vant
for i in range (len(filtered_df_heures)):
    jour=filtered_df_heures.iloc[i].day
    mois=filtered_df_heures.iloc[i].month
    annee=filtered_df_heures.iloc[i].year
    dateFormatter = "%Y/%m/%d"
    filtre=str(annee)+'/'+str(mois)+'/'+str(jour)
    jours_pic.append(filtre)
    filtre_deb=datetime.strptime(filtre,dateFormatter) - timedelta(days=1)
    filtre_fin=datetime.strptime(filtre,dateFormatter) + timedelta(days=1)
    jours_filtrage.append([filtre_deb,filtre_fin])

#suppression des doublons
jours_pic_wd=[]   
for i in jours_pic:
    if i not in jours_pic_wd: 
        jours_pic_wd.append(i)

#suppresion des doublons
jours_filtrage_wd=[]   
for i in jours_filtrage:
    if i not in jours_filtrage_wd: 
        jours_filtrage_wd.append(i)

#On récupére l'index des heures où il y a eu un pic de pollution et 
#on les regroupe par jour
index_pics=[] # cette liste regroupe les heures avec un pic de pollution par jour
filtered_df_heures=filtered_df_heures.reset_index()
for i in range (len(jours_filtrage_wd)):
    mask = (filtered_df_heures['Heure'] >= jours_filtrage_wd[i][0]) & (filtered_df_heures['Heure'] <= jours_filtrage_wd[i][1])
    L=filtered_df_heures.loc[mask]
    L=L.drop("index",axis=1)
    L=L.index.to_numpy()
    index_pics.append(L)

#Préparation ACP
##Ecartement des labels
df_NUM=filtered_df.drop(["Heure"],axis=1)

#Normalisation
sc = StandardScaler()

#transformation – centrage-réduction 
Z = sc.fit_transform(df_NUM)

#instanciation 
acp = PCA(svd_solver='full')

#calculs 
coord = acp.fit_transform(Z) 

#Variance expliquée
pareto(acp.explained_variance_ratio_)

# Transformation en DataFrame pandas
Pca_df = pd.DataFrame({"Dim1" : coord[:,0], "Dim2" : coord[:,1]})
fig, ax = plt.subplots()
ax.set_facecolor('gray')

#Création d'une palette de couleurs 
palette=[]
for cname, hex in matplotlib.colors.cnames.items():
    palette.append(cname)
palette=list(reversed(palette))

#Affichage des points
for i in range (len(index_pics)):
    label=jours_pic_wd[i]
    couleur=palette[i]
    for j in range (len(index_pics[i])):
        ax.scatter(Pca_df.loc[index_pics[i][j]][0], Pca_df.loc[index_pics[i][j]][1], color=couleur, label=label)
        label = "_nolegend_"
plt.xlabel("Dimension 1 ") 
plt.ylabel("Dimension 2 ")
plt.title("ACP sur les différents pics de pollution")
ax.legend()
plt.show()

#Analyse de Fourier
fourier=[]
fondamental_f=[]
for i in range (len(jours_filtrage_wd)):
    fondamental=[]
    mask1 = (df['Heure'] >= jours_filtrage_wd[i][0]) & (df['Heure'] <= jours_filtrage_wd[i][1])
    fourier=df.loc[mask1]
    fourier=fourier.drop("Diff carrés",axis=1)
    fondamental.append(fft(fourier['Particules PM1 corr'].to_numpy())[0].real)
    fondamental.append(fft(fourier['Particules PM2,5 corr'].to_numpy())[0].real)
    fondamental.append(fft(fourier['Particules PM10 corr'].to_numpy())[0].real)
    fondamental.append(fft(fourier['Black Carbon (combustion de fossiles)'].to_numpy())[0].real)
    fondamental.append(fft(fourier['Black Carbon (combustion de biomasse)'].to_numpy())[0].real)
    fondamental.append(fft(fourier['Black Carbon (dans les PM2.5)'].to_numpy())[0].real)
    fondamental_f.append(fondamental)

