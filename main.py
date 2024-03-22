import json
import subprocess
from pathlib import Path

from create_pdf import create_pdf_from_img

with open("data.json", "r") as json_file:
    data = json.load(json_file)

name_calendar = data["Settings"]["save"]["name"]


def lancer_script_blender(nom_fichier_blend, nom_script):
    # Chemin absolu du fichier Blender
    chemin_fichier_blend = Path(__file__).parent / nom_fichier_blend

    # Spécifier le chemin complet de l'exécutable Blender
    chemin_blender = "/Applications/Blender.app/Contents/MacOS/Blender"

    # Construire la commande pour lancer Blender avec le script en arrière-plan
    commande_blender = [
        chemin_blender,  # Chemin complet de l'exécutable Blender
        "--background",  # Lancer Blender en arrière-plan sans interface graphique
        "--python",
        nom_script,  # Spécifier le script Python à exécuter
    ]

    # Lancer le processus Blender avec le script en arrière-plan
    subprocess.run(commande_blender, check=True)


# Nom du fichier Blender et nom du script à exécuter
nom_fichier_blend = "calendar-2024.blend"
nom_script = "calendar_automatic.py"

# Appeler la fonction pour lancer le script Blender en arrière-plan
lancer_script_blender(nom_fichier_blend, nom_script)

create_pdf_from_img(name_calendar)
