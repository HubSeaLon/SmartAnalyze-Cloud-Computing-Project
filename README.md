### Projet Cloud 

[SmartAnalyze](https://smartanalyze-fmdcgrf9dwdzfver.francecentral-01.azurewebsites.net/) est une application web utilisant Flask et des services Azure (Text Analytics et Computer Vision) pour analyser des textes et des images. Elle permet :
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

1. Cloner le dépôt et créer un dossier uploads :

```bash
git clone https://github.com/HubSeaLon/SmartAnalyze-Cloud-Computing-Project.git
cd projet_cloud
mkdir uploads
```


2. Créer un environnement virtuel et l'activer :

```bash
python3 -m venv venv
source venv/bin/activate
```
3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
- Créer un fichier .env dans le répertoire principal

```bash
touch .env
```

Avec les informations suivantes :
``` .env
TEXT_ANALYTICS_KEY=<votre_clé>
TEXT_ANALYTICS_ENDPOINT=<votre_endpoint>
VISION_KEY=<votre_clé>
VISION_ENDPOINT=<votre_endpoint>
```

5. Construire et lancer l'image Docker :

```bash
docker build -t smartanalyze .
docker run -p 5000:80 smartanalyze
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

7. Quelque images de l'application
![Capture d'écran 2024-12-07 175109](https://github.com/user-attachments/assets/3d8e1a61-8766-4400-b8b9-39e50911d142)
![Capture d'écran 2024-12-07 175350](https://github.com/user-attachments/assets/6e940d19-86c4-44d1-b279-08444e188c7e)
![Capture d'écran 2024-12-07 175350](https://github.com/user-attachments/assets/60f90fd9-7972-4e27-879a-7934f6789f30)
![Capture d'écran 2024-12-07 180216](https://github.com/user-attachments/assets/2f502107-df11-4f0f-9c3c-983c32b5a529)
![Capture d'écran 2024-12-07 180448](https://github.com/user-attachments/assets/73d70589-3f6f-44c5-b311-93cd74bd49fa)
![Capture d'écran 2024-12-07 180848](https://github.com/user-attachments/assets/927a9337-79bd-4f60-9be3-7f31c1473d72)
![Capture d'écran 2024-12-07 180904](https://github.com/user-attachments/assets/3abca1a3-bbe6-47e0-b566-a8bd76ad69ae)


