
# Auto Calendar

# 🚧 En cours d'écriture 

Bienvenue dans AutoCalendar est un script python qui utilise la bibliothèque blender bpy pour créer un calendrier en fonction des données qu'il récupère comme l'année, les fonts, les couleurs... présentent dans un fichier json.  
Le script génère un fichier pdf avec tous les mois, au format A3+.
On a comme cela un très beau calendrier à jour, en changeant simplement l'année, et cela pour toutes les années qui arrivent ✨😊

## Table of Contents
- [Auto Calendar](#auto-calendar)
- [🚧 En cours d'écriture](#-en-cours-décriture)
  - [Table of Contents](#table-of-contents)
  - [Prérequis](#prérequis)
  - [🛠️ Instalation](#️-instalation)
    - [macOs, linux](#macos-linux)
    - [windows](#windows)
  - [🕹️ Utilisation](#️-utilisation)


## Prérequis
Avant d'utiliser Auto Calendar, assurez-vous d'avoir les éléments suivants installés sur votre système :

- Python (version 3.11.4 ou supérieure) [lien vers install de python](https://www.python.org/downloads/)
- Blender (version 4.0 ou supérieure) [lien vers install de blender](https://www.blender.org/download/)



## 🛠️ Instalation

### macOs, linux
1. Clonez ce dépôt sur votre machine:
   ````
    ````

2. Accédez au répertoire du projet:
   ````
    ```` 
3. Créez et activez un environnement virtuel:
    ````
    ```` 
4. Installez les dépendances nécessaires à l'aide du fichier requirements.txt:
    ````
    ````
5. Chemin vers l'application blender  
Une fois blender installer, il faut définir le chemin vers lequel se trouve l'éxecutable de l'application blender dans le fichier data.json 

### windows

## 🕹️ Utilisation
Ouvrir un terminal

1. Assurez-vous que vous êtes dans le répertoire racine du projet :

```plain
cd /chemin/vers/dossier/Auto_calendar
```
2. Exécutez le script principal main.py pour générer le calendrier :
```python
python main.py
```

3. Récupérer le calendier en pdf dans le dossier '***export_pdf' et voilà ✨

Vous pouvez ensuite changer l'année dans le fichier data.json pour mettre à jour le calendier. Par exemple mettre 2025, sauvegarder le fichier data.json et exécuter de nouveau le script.  



