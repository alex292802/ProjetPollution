# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 10:57:02 2022

Script: Ce programme permet la réalisation ainsi que  la visualisation de l'ACP.
        Il permet également de faire de la classification à partir des nouvelles 
        coordonnées engendrées par l'ACP'

@author: Benjamin
"""
################################ Librairies ###################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#classe pour l'ACP 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#Autres fonctions

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

################################## ACP ########################################

#Chargement des données

df=pd.read_pickle('Marseille_long_Champ_JOURNALIER.dataframe')

#Transformation des dates en datetimes
df['Heure'] = pd.to_datetime(df['Heure'])

#Indexation du dataframe en fonction de la date
df = df.set_index('Heure')


#Filtre dates
df1=df.loc['2020-11-01':'2021-03-01']
df2=df.loc['2021-05-01':'2021-09-01']
#Rajout Label
df1=df1.assign(Label="Hiver 2020-2021")
df2=df2.assign(Label="Eté 2021")
df=pd.concat([df1,df2], axis=0)




#Désindexation du dataframe 
df = df.reset_index()
df.info()

#Filtre colonnes
df=df.drop(["Heure",
        'Méthane',"Dioxyde de soufre (SO2)", "Black Carbon (dans les PM2.5)", "Dioxyde de carbone","Oxydes d'azote (NOX)", "Monoxyde d'azote (NO)",
       'Nombre de particules',
       "Dioxyde d'azote (NO2)"], axis=1)

#df.info()
#Filtre des Nan
df.dropna(inplace=True) #Supprime les dates pours lesquelles ily a un nan 
df.info()


#Préparation ACP
##Ecartement des labels
df_NUM=df.drop(["Label"],axis=1)

#Opération de base sur les features
#X_Ratio=df[['PM1/PM10','PM1/PM2,5','PM2,5/PM10']]
df_NUM=df_NUM.assign(PM10=df['Particules PM10']-df["Particules PM2,5"])
df_NUM=df_NUM.assign(PM2_5=df['Particules PM2,5']-df["Particules PM1"])
#df_NUM.info()
df_NUM=df_NUM.drop(["Particules PM10"],axis=1)
df_NUM=df_NUM.drop(["Particules PM2,5"],axis=1)
print("Colonnes analysées par l'ACP",df.columns)
df_NUM.info()

#Normalisation
sc = StandardScaler()

#transformation – centrage-réduction 
Z = sc.fit_transform(df_NUM)


#instanciation 
acp = PCA(svd_solver='full')

#affichage des paramètres 
print(acp)

#calculs 
coord = acp.fit_transform(Z) 


#Variance expliquée
pareto(acp.explained_variance_ratio_)

# Transformation en DataFrame pandas
Pca_df = pd.DataFrame({
    "Dim1" : coord[:,0], 
    "Dim2" : coord[:,1],
    "Labels" : df["Label"],
})

# Résultat (premières lignes)
Pca_df.head()

# permet de créer une palette de couleurs, basée sur Color Brewer
palette = plt.get_cmap("Dark2")
# associe une couleur à chaque continent (cf ci-dessous)
couleurs = dict(zip(Pca_df["Labels"].drop_duplicates(), palette(range(2))))
position = dict(zip(couleurs.keys(), range(2)))



# Affichage des points avec une liste de couleurs

Pca_df.plot.scatter(x = "Dim1", y = "Dim2", c = [couleurs[p] for p in Pca_df["Labels"]])
# boucle pour afficher la légende
for cont, coul in couleurs.items():
    plt.scatter(3, position[cont] / 3 + 2.15, c = [coul], s = 20)
    plt.text(3.2, position[cont] / 3 + 2, cont)
plt.xlabel("Dimension 1 (60%)") 
plt.ylabel("Dimension 2 (25 %)")
plt.suptitle("Premier plan factoriel (83%)")
plt.show()


##############################################################################
##############################################################################
################################# Classification ############################# 

#Librairies supplémentaires

from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

#Transformation en valeurs numériques des labels
prepoces=LabelEncoder()
prepoces.fit(Pca_df['Labels'])
Pca_df['Labels']=prepoces.transform(Pca_df['Labels'])
#séparation des features et du label
X = Pca_df.drop(columns = 'Labels', axis = 1)
Y = Pca_df['Labels']

#Préparation des jeux d'entraînement et de test.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, stratify = None, random_state = 2)

#Paramètrage du modèle

#model = KNeighborsClassifier(n_neighbors=2)
#model = KNMeans(n_clusters=2)
model = MLPClassifier(solver='lbfgs', alpha=1e-5, activation= 'logistic', learning_rate_init=0.001,
                   hidden_layer_sizes=(10, 4), random_state=1)

#Apprentissage
model.fit(X_train, Y_train)

#prédiction du modèle 
X_train_pred = model.predict(X_train)
#calcul de la métrique d'évaluation entre la prédiction et les données connues (RMSE)
training_data_rmse = sqrt(mean_squared_error(X_train_pred, Y_train))
print('RMSE on training data', training_data_rmse)
#idem
X_test_pred = model.predict(X_test)
test_data_rmse = sqrt(mean_squared_error(X_test_pred, Y_test))
print('RMSE on test data set', test_data_rmse)


#print('R2 on training data', r2_score(Y_train, X_train_pred))
#print('R2 on training data', r2_score(Y_test, X_test_pred))


#Matrice de confusion (Echec implémentation)
#confusion_matrix(y_true, y_pred)


############################# 

inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters = k, init = "random", n_init = 20).fit(df_NUM)
    inertia = inertia + [kmeans.inertia_]
inertia = pd.DataFrame({"k": range(1, 11), "inertia": inertia})
inertia.plot.line(x = "k", y = "inertia")
plt.scatter(2, inertia.query('k == 2')["inertia"], c = "red")
#plt.show()



