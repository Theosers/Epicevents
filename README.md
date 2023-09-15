# Epicevents

Ce projet utilise la version de python 3.11

# Description :

Logiciel de gestion de la relation client (CRM) de l'entreprise, qui effectue le suivi de tous les clients et événements.
Il s'agit d'une application Django avec une base de données PostgreSQL.
La base de donnée est configuré dans le fichier settings.py et configuré localement avec comme nom 'postgres' sur le port '5432'.

Activités :
- Elaboration d’un diagramme entité-relation (ERD) en adoptant une approche de type «domain-driven design»
- Mise en place de l'application Django REST et d’un ensemble d’endpoints sécurisés
- Configuration de la base de donnée PostgreSQL
- Ajout des opérations CRUD appliquées aux divers objets CRM
- Création d’une interface front-end simple à l'aide du site d'administration Django(laquelle permettra aux utilisateurs autorisés de gérer l'application, d'accéder à l'ensemble des modèles et de vérifier la configuration de la base de données)
- Test des endpoints d'API de l'application avec Postman

# Setup :

- Téléchargez le projet
- Installez le fichier requirements.txt :
```python 
python3 -m pip install -r requirements.txt
```
- Lancez le serveur django avec la commande:
```python 
python3 manage.py runserver
```
