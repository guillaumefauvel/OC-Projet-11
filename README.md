# GUDLIFT - Site de réservation à des évènements sportif 
### Application destinée à la mise en pratique d'un développement basé sur le débogage et les tests techniques.

# Lancement du projet

1. Tout d'abord, cloner le repository sur votre machine.  
2. Mettez en place un environnement virtuel (Avec notamment `virtual env`)
3. Installer les dépendances avec un `pip install -r requirements.txt`
4. A la fin du fichier server.py ajuster l'argument mode à la fonction create_app à votre besoin : `Debugging` si vous désirer être uniquement en lecture de la base de données ou `Production` si vous désirer sauvegarder vos actions.
5. Une fois votre choix réalisé lancer le serveur Flask avec un `python server.py`

# Lancements des tests

## Les tests unitaires / intégrations

Les tests ont été réalisé avec pytest.
Pour les lancer, entrez : `pytest -v` à la racine du projet.

## Les tests de fonctionnels

Les tests fonctionnels sont développés à l'aide de Selenium et du module Unittest.  
Pour les lancer vous devez en premier lieu lancer le serveur en mode `Debugging` (CF - Lancement du projet 4.).  
Ensuite lancez à la racine du projet la commande `python .\tests\functionnal\funtionnal_testing.py`

## Les tests de performance

Pour fournir des tests de performance nous utilisons Locust. 
Afin d'initialiser ce test entrer à la racine la commande `cd .\tests\performance_tests\ ; locust`  
Accéder à la plateforme de test en suivant ce lien : `http://localhost:8089`  
Vous pourrez ainsi lancer la simulation de traffic.
