# Article-recommendation-system

Ce projet est un système de recommandation d'articles scientifiques basé sur les citations des documents et en exploitant les réseaux de neurones (Deep Learning). Il a la capabilité de fournir des recommandation adaptées aux préférences et aux besoins  des utilisateurs pour les aider a accéder aux ressources désirées dans un temps limité.

Notre approche a surpassé les systemes de recommandation traditionnels, tels que les limites les plus importantes que le système surmonte sont le problème de la masse critique et la scalabilité. Notre système a pu fournir des articles pertinents à la requête de l’utilisateur en peu de temps et avec une grande précision pour
les deux ensembles de données utilisés dans ce projet. Le premier jeu de données contient plus de 2k articles et le deuxième corpus contient plus de 3 millions d’articles, cela montre que le système n’est pas affecté par la taille de la base de données. De plus, il a la capacité de renvoyer des résultats même sans la base de données de l’utilisateur et ses votes, contrairement aux systèmes traditionnels basés sur le filtrage collaboratif qui souffrent du problème de démarrage à froid.


## Aminer dataset

Les données sont téléchargeables à partir [ici](https://www.aminer.org/citation). Ensuite, nous avons appliqué quelques techniques de prétraitement et l'avons téléchargé sur postgresql.

Pour pouvoir charger les données dans postgresql, installez Spark sur votre machine et exécutez le script ```convert.py``` et les requêtes répertoriées dans ```query_sql.txt```.

Après avoir stocké les données dans postgresql, vous devez également charger des données binaires (fichiers *.pkl) depuis [ce lien](https://www.kaggle.com/code/yassou432/recommendation-system-part-2-2/data)

## Deuxième dataset

Les données sont téléchargeables à partir [ici](https://github.com/SJ-palpa/curation_projet). 

Après avoir stocké les données dans postgresql, vous devez également charger des données binaires (fichiers *.pkl) depuis [ce lien](https://www.kaggle.com/code/yassou432/random-data-for-recommendation-system-part-02/data)

## Lancer l'application web

Après avoir configuré la base de données et les fichiers nécessaires. Exécutez les commandes suivantes pour lancer l'application Web :

- Créez un nouvel environnement Python :

  ```cmd
  cd Article-recommendation-system
  python -m venv env
  ```

- Activer l'environnement :

  ```cmd
  .\env\Scripts\activate
  ```

- Installez les packages requis (s'ils ne sont pas déjà installés) :
  
  ```cmd
  pip install -r requirements.txt
  ```

- Exécuter :

  ```cmd
  python execute.py
  ```

## UI de notre application

Page Home :
![home](https://user-images.githubusercontent.com/37484871/197530911-6d416414-694b-4657-a0bf-7fc9d1a64c02.jpg)

Page de description d'article avec la liste des remmandations retournée par notre algorithme :
![description](https://user-images.githubusercontent.com/37484871/197530894-c328e3fe-9307-4b21-a59b-e0f58b0df417.jpg)

Inscription de l’utilisateur :
![register](https://user-images.githubusercontent.com/37484871/197530923-c9a83414-6d2d-45a6-b5c2-1ef75c925ff4.jpg)

Connexion au compte utilisateur
![login](https://user-images.githubusercontent.com/37484871/197530915-1b1c5cc5-9a58-4b7d-b177-394a2c8078ea.jpg)

Compte d'utilisateur :
![profil](https://user-images.githubusercontent.com/37484871/197530917-05e0a10d-763f-4d10-8b01-c26d51405186.jpg)

Historique :
![history](https://user-images.githubusercontent.com/37484871/197530904-41ee014b-31a2-4928-94c1-165e5280166b.jpg)
