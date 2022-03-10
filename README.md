# Corrélation entre pollution aux particules fines et autres types de pollution 

La qualité de l'air que l'on respire dépend de nombreux paramètres, les émissions de polluants, bien sûr, du relief naturel ou urbain, de la présence d'îlots de chaleur, mais également des conditions météorologiques. Ainsi, le vent est un élément déterminant dans la dispersion des polluants atmosphériques. La pluie permet également de diminuer de manière significative les concentrations de polluants dans l'air ambiant. À l'inverse, les situations anticycloniques, avec des masses d'air stagnantes, conduisent à des augmentations des concentrations de polluants. Par ailleurs, de récentes études ont aussi montré que les arbres, en jouant le rôled’intercepteur de particules, ont un impact direct sur la pollution (captation, puis transport par les pluies, captations remise en suspension par le vent). On comprend donc que les changements de saison ont un impact direct sur la pollution, impact renforcé par les activités humaines qui varient elles aussi au cours des saisons (chauffage au bois, épandage, etc.).

Nous pouvons découper ce projet en 3 taches principales :

Tout d’abord, nous savons que le nombre de particules dans l'air évolue au cours de l’année et est sensiblement différent en été par rapport à l’hiver. Notre premier objectif était de mettre en évidence une bisaisonalité en séparant l’été de l’hiver notamment. Chaque journée est un individu, chaque particule est un des features. L’enjeu était d’obtenir 2 nuages de points avec éventuellement un continuum de point. Nous nous sommes ensuite demandé quelles étaient les features les plus pertinentes pour séparer l’hiver de l’été et si les résultats ne sont pas issus d’une donnée prépondérante. Pour se faire, nous avons d'abord réalisé des Analyses en Composantes Principales sur différents ensembles de features, puis nous y avons appliqué différentes techniques de classification (notamment des techniques de clustering et de régression logistique) en reprenant les nouvelles coordonnées des deux premières composantes. En comparant les différents résultats obtenus, nous avons alors montré que le meilleur ensemble permettant de décrire la bisaisonnalité correspondait aux polluants suivant : PM10,PM2.5,PM1,Blacks Carbon contenus dans les PM2.5.

Notre 2ème objectif était de construire un jeu de données propres à partir des données des 3 stations disponibles. Dans l’optique d’identifier des événements particuliers du type sable du Sahara, nous avons eu besoin d'un jeu de donnée propre. En effet, en se servant uniquement des données de Marseille Long Champs, nous avons rencontré plusieurs problèmes :
• La mesure d’événements locaux se déroulant uniquement dans la zone géographique de Marseille Long Champs
• Les erreurs de mesure liés aux instruments
• La présence de nombreux NaN
• La présence de données qui ne nous intéressent pas (notamment les gaz)
Nous avons commencé par calculer le coefficient de Pearson entre les différentes stations pour voir dans quelle mesure les données des stations étaient corrélés. Nous avons ensuite fusionné les données des 3 stations en prenant le minimum des 3 valeurs disponibles pour chaque features et nous avons enlevé les gaz des features. Nous avons également remarqué qu’il manquait des données sur des intervalles assez importants. Après avoir essayé de compléter ces trous de données de plusieurs manières (régression et différentes méthodes de fitting…), nous avons tracé la droite reliant les 2 points de chaque côté du trou de donnée puis nous avons simplement supprimé les points. Ainsi, on obtient une fonction discontinue, mais ce n’est pas dérangeant pour la suite.

Notre dernier objectif était l’étude de la potentielle séparation de 2 pics de pollution. En effet, les pics de pollution sont de différentes natures (épisode du Sahara, feu de forêt… ) et nous voulions être capables de séparer un épisode de sable du Sahara des autres pics de pollution. Nous sommes passés aux données horaires pour avoir plus de data et nous avons étudié l’année 2019 en particulier.
Les épisodes de sable du Sahara se manifestent principalement par une grande augmentation de la concentration des particules PM10 et PM2.5. Nous avons donc fabriqué une quantité à partir de ces 2 concentrations nous permettant d'observer quand le nombre de particules dont le diamètre était compris entre le diamétre des PM10 et PM2.5 variait brusquement. On s’est résolu à utiliser la différence au carré des particules de taille comprise entre les PM2.5 et PM10. Il était ensuite nécessaire de créer un seuil, pour savoir à partir de quelle valeur de (PM10-PM2.5)² on avait un pic de pollution. Nous avons donc regardé statistiquement la pollution pour en traçant un histogramme de la répartition des classes. Une fois ce seuil déterminé, nous avons pu remonter une liste de potentiels pics de sable du Sahara. Nous avons analysé les composantes du pic et les particules majoritaires afin de savoir ce qu’il s’était passé. Puis nous avons réalisé une ACP pour voir s'il était possible de séparer un pic de pollution d’un autre et ainsi identifier un événement du type sable du Sahara. Enfin, nous avons réalisé une analyse de Fourier (uniquement du fondamental) en considérant l’intervalle [J-1, J+1] avec J le jour où il y a eu le pic de pollution.

Les données sont toutes disponibles en open source et par station de mesures à l’adresse suivante : https://www.atmosud.org/donnees/acces-par-station

Nous avons travaillé en priorité sur les données PM1 PM2.5 et PM10 de la station de mesure Marseille longchamps (https://www.atmosud.org/donnees/acces-parstation/03043)

Nous avons travaillé avec le langage Python aussi bien pour l’extraction et l’analyse des données que pour la visualisation des données.

Ce git comprends :

3 fichiers horaires :

-SAINT_LOUIS_HEURE

-MARSEILLE_LONGCHMAP_HEURE_COMPLET

-AIX_ART_HEURES

3 fichiers journaliers :

-Aix Ecole d'Art_JOURNALIER

-Avignon_Mairie_JOURNALIER

-Marseille_long_Champ_JOURNALIER

6 codes :

1_Heatmap

2_Heatmap_Hour

3_ACPClass

4_correlation_entre_stations

5_construction_jeu_de_donnee_propre

6_identification_evenements_particuliers

Une description de chaque code et de son utlité est présente en début de chaque fichier .py.
