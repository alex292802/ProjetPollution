# Corrélation entre pollution aux particules fines et autres types de pollution 

La qualité de l'air que l'on respire dépend de nombreux paramètres, les émissions de polluants bien sûr, du relief naturel ou urbain, de la présence d'îlots de chaleur, mais également des conditions météorologiques. Ainsi le vent est un élément déterminant dans la dispersion des polluants atmosphériques. La pluie permet également de diminuer de manière significative les concentrations de polluants dans l'air ambiant. A l'inverse, les situations anticycloniques, avecdes masses d'air stagnantes, conduisent à des augmentationsdes concentrations de polluants. Par ailleurs, de récentesétudes ont aussi montré que les arbres, en jouant le rôled’intercepteur de particules, ont un impact direct sur la pollution (captation, puis transport par les pluies, captationet remise en suspension par le vent). On comprend donc queles changements de saison ont un impact direct sur la pollution, impact renforcé par les activités humaines qui varient elles aussi au cours des saisons (chauffage au bois, épandage, etc.).

L’objectif est de mettre en évidence la corrélation entre la granulométrie de la pollution en particules fines et la naturede la pollution (analyse fonction des données disponibles au sein d’une même station de mesure / de différentes stations de mesures).

Le projet a pour sous-objectifs :
1. L’extraction des données 
2. L’analyse des données : pollution de fond /événements ponctuels
3. La visualisation temporelle multigraphiques des données (PM1, PM2.5, PM10, ozone, NO2, black carbon et notamment black carbon dans PM2.5, etc…
4. La mise en place d’un algorithme permettant la détection automatique d’évènement ponctuel (par exemple épisode du Sable du Sahara) 
5. La corrélation entre le type de pollution et les informations en termes de particules fines.

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

7 codes :

1_Heatmap

2_Heatmap_Hour

3_ACPClass

4_construction_jeu_de_donnee_propre

5_correlation_entre_stations

6_visualisation_evenements_particuliers

7_identification_evenements_particuliers

Une description de chaque code et de son utlité est présente en début de chaque fichier .py.
