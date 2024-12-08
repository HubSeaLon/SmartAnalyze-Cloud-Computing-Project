Projet Cloud 

SmartAnalyze est une application web utilisant Flask et des services Azure (Text Analytics et Computer Vision) pour analyser des textes et des images. Elle permet :
- D'obtenir des informations détaillées sur des textes (langue, sentiment, mots-clés, entités, résumé).
- D'extraire du texte, de détecter des objets et de générer une description à partir d'images.

Liste des outils et technologies employés : 
- Flask (Python)
- Docker
- Azure Web App
- Azure Container Registry
- Azure Cognitive Services (Text Analytics et Computer Vision)

Prérequis :
- Python 3.9 ou supérieur
- Docker
- Compte Azure avec :
  - Un registre de conteneurs (Container Registry)
  - Les services Text Analytics et Computer Vision activés

### Étapes pour lancer l'application :

1. Cloner le dépôt :

```bash
git clone https://github.com/HubSeaLon/projet_cloud.git
cd projet_cloud
```
Créer un dossier uploads 

2. Créer un environnement virtuel et l'activer :

```bash
python3 -m venv venv
source venv/bin/activate
```
3. Installer les dépendances :
```bash
pip isntall -r requirements.txt
```

4. Configurer les variables d'environnement :
- Créer un fichier .env dans le répertoire principal avec les informations suivantes :
TEXT_ANALYTICS_KEY=<votre_clé>
TEXT_ANALYTICS_ENDPOINT=<votre_endpoint>
VISION_KEY=<votre_clé>
VISION_ENDPOINT=<votre_endpoint>

5. Construire et lancer l'image Docker :

```bash
docker build -t smartanalyze .
docker run -p 5000:5000 smartanalyze
```
Ouvrez votre navigateur et accédez à : http://localhost:5000

6. Déploiement sur Azure :

- Pousser l'image Docker vers Azure Container Registry :

```bash
az login
az acr login --name <NomDuRegistre>
docker tag smartanalyze <NomDuRegistre>.azurecr.io/smartanalyze:latest
docker push <NomDuRegistre>.azurecr.io/smartanalyze:latest
```
Configurer Azure Web App :

Dans le portail Azure, créez une Web App et configurez-la pour utiliser l'image Docker poussée dans votre Container Registry. Et autoriser les droits de l'App Web pour le container (AcrPull) 



