# Description de l'application (MVP)
Cette application web présente deux cas d'utilisation principaux :
* Demander des critiques sur un livre ou sur un article en particulier.
* Rechercher des livres ou articles intéressants à lire en se basant sur des critiques publiés par d'autres utilisateurs.

## Lancement de l'application

* Ouvrez un invite de commande
* Placez-vous dans le dossier contenant le répertoire OC9
* Création de l'environnement virtuel : ```python -m venv env```
* Activation de l'environnement virtuel :
    * Pour Windows : ```env\Scripts\activate.bat```
    * Pour Linux   : ```env/bin/activate```
* Installation des dépendances : ```pip install -r requirements.txt```
* Placez-vous dans le dossier contenant manage.py
* Lancement du serveur local : ```python manage.py runserver```
* Ouvrez votre navigateur web a l'url : ```http://127.0.0.1:8000/```

### Details de connexion 

Plusieurs exemples d'utilisateurs existent déjà en base de données.

Utilisateur principal :
* Login / password : Quentin / abcd

Utilisateurs secondaires : 

* Louis Auclair / abcd
* Jean Charles / abcd
* Julien Lejeune / abcd

#### Connectez-vous avec l'utilisateur principal pour voir plus facilement certaine des fonctionnalités importantes.

* Un utilisateur doit voir ses propres tickets et critiques
* Un utilisateur doit voir les tickets et critiques de tous les utilisateurs qu'il suit
* Un utilisateur doit voir les réponses à ses propres tickets même si l'utilisateur qui a répondu ne fait pas partie des personnes qu'il suit
* Bloquer les critiques aux tickets si un utilisateur a déjà posté une critique en réponse.
