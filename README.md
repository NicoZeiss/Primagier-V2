# Application Primagier
Ce projet est le treizième et dernier projet réalisé dans le cadre du parcours **OpenClassrooms** ***[Développeur Python](https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python)***.  
Le site Primagier est accessible à l'adresse suivante : **[Mon appli](https://primagier.herokuapp.com/)**  
Il est destiné à l'usage du personnel de l'**école maternelle Lauchacker**.

Primagier est une application réalisée en langage Python (3.6.8), avec le framework Django.<br/>
Il permet aux instituteurs(trices) de l'école de créer des imagiers facilement et rapidement, et de les télécharger au format PDF.
Un imagier est une planche d'images déstinée à apprendre aux élèves de maternelle des mots simples, afin d'étendre leur vocabulaire.

## Instalation en local
- Forker ce projet GitHub
- Créer un environnement virtuel à la racine du projet
- Installer les dépendances : *pip install -r requirements.txt*
- Créer une base de données PostgreSQL et la configurer dans le fichier *settings.py*
- Effectuer les migrations Django : *./manage.py makemigrations*<br/>
*./manage.py migrate*
- Remplir la base de données avec les données de démonstration : *./manage.py populate categories*<br/>
*./manage.py populate items*
- Créer un superutilisateur : *./manage.py createsueruser*

## Lancement en local
- Lancer la commande : *./manage.py runserver*
- Se rendre, avec votre navigateur web, à l'adresse suivante : *http://127.0.0.1:8000/*

## Principaux packages utilisés
- **[Django](https://www.djangoproject.com/)** : le framework populaire de Python
- **[Requests](https://requests-fr.readthedocs.io/en/latest/)** : librairie HTTP
- **[Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/)** : pour la réalisation des tests unitaires
- **[Gunicorn](https://gunicorn.org/)** : Configuration du serveur HTTP
- **[Pylint](https://www.pylint.org/)** : Mise en conformité avec la PEP8
- **[xhtml2pdf](https://xhtml2pdf.readthedocs.io/en/latest/index.html)** : Convertion de pages HTML en format PDF

## Lancement des test
A la racine du projet, lancer la commande : *./manage.py test_report*<br/>
Cela lancera les tests, et produira un rapport de test qui présente le taux de couverture de l'application.

## Langages web utilisés
- HTML5
- CSS3
- Javascript
- Framework Bootstrap
- Template utilisé : **[Start Boostrap Creative](https://blackrockdigital.github.io/startbootstrap-creative/)**

## Hébergement
- **[Heroku](https://www.heroku.com/)**

## Principales fonctionnalités de l'application
**Création d'un imagier**
- L'utilisateur sélectionne la catégorie souhaitée
- Il choisi ensuite la sous-catégorie
- Il sélectionne les images à ajouter à son imagier
- L'imagier crée est pour l'instant temporaire
- Les items ajoutés sont consultables au bas de la page
  
**Enregistrement d'un imagier en favoris**
- Créer un imagier temporaire
- Cliquer sur *Enregistrer en favoris*
- Renseigner un nom d'imagier, puis valider

**Exporter un imagier en PDF**
*Premier cas :*
- Créer un imagier temporaire
- Cliquer sur *Exporter en PDF*

*Deuxième cas:*
- Accéder aux imagiers favoris
- Sélectionner l'imagier à exporter
- Cliquer sur *Exporter en PDF*

*Puis :*
- Renseigner un titre d'imagier, un nom de fichier, et cocher les polices d'écriture à utiliser
- Valider, puis cliquer sur l'icone de téléchargement

**Créer un compte utilisateur**
- Cliquer sur l'icone de connexion en haut à droite
- Cliquer sur *Créer un compte utilisateur*
- Renseigner un nom d'utilisateur, une adresse email et un mot de passe
- Valider

**Ajouter des items à la base de données**
*L'utilisateur doit appartenir au groupe d'utilisateurs "école"*
- Cliquer le bouton "+" en haut à droite
- Renseigner un nom pour l'item à ajouter
- Renseigner l'URL de l'image
- Sélectionner la catégorie de l'item dans la liste déroulante
- Valider

**Fonctionnalités accessibles à l'administrateur de l'application**
- Ajout/suppression/modification d'items dans la base de données
- Ajout/suppression/modification de catégories/sous-catégories dans la base de données
- Gestion des utilisateurs (création/suppression de compte, ajout au groupe "école")

