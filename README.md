# GUDLIFT - Site de réservation à des évènements sportif 
### Application utilisant Flask destinée à la mise en pratique d'un développement basé sur le débogage et les tests techniques.

# Lancement du projet

1. Tout d'abord, clonez le repository sur votre machine.  
2. Mettez en place un environnement virtuel (Notamment avec `virtual env`)
3. Installez les dépendances avec un `pip install -r requirements.txt`
4. A la fin du fichier `server.py` ajuster l'argument `mode` à la fonction `create_app` à votre besoin : `Debugging` si vous désirez être uniquement en lecture de la base de données ou `Production` si vous désirez sauvegarder vos actions.
5. Une fois votre choix réalisé lancer le serveur Flask avec un `python server.py`

# Lancements des tests

## Les tests unitaires / intégrations

Les tests ont été réalisé avec **Pytest**.  
Pour les lancer, entrez `pytest -v` à la racine du projet.  
Si vous souhaitez obtenir un rapport de couverture des tests lancer la commande `pytest --cov=. --cov-report html` à la racine du projet.  
Le rapport sera accessible au ficher index.html dans le dossier htmlcov
## Les tests fonctionnels

Les tests fonctionnels sont développés à l'aide de Selenium et du module **Unittest**.  
Pour les lancer vous devez en premier lieu lancer le serveur en mode `'Debugging'` (CF - Lancement du projet 4.).  
Ensuite lancez à la racine du projet la commande `python .\tests\functionnal_tests\functionnal_testing.py`

## Les tests de performance

Pour fournir des tests de performance nous utilisons **Locust**.  
Afin d'initialiser ce test, entrez à la racine la commande `cd .\tests\performance_tests\ ; locust`  
Accédez à la plateforme de test en suivant ce lien `http://localhost:8089`  
Vous pourrez ainsi lancer la simulation de trafic.

