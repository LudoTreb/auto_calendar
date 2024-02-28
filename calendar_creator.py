from random import randint

import bpy

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False, confirm=False)


offset = 0
for i in range(5):

    bpy.ops.object.text_add(
        enter_editmode=False, align="WORLD", location=(0, offset, 0), scale=(1, 1, 1)
    )
    # on rentre en mode edition
    bpy.ops.object.editmode_toggle()
    # on selection tout le text
    bpy.ops.font.select_all()
    # delete la selection
    bpy.ops.font.delete(type="PREVIOUS_OR_SELECTION")

    bpy.ops.font.text_insert(text=str(randint(0, 10)))
    bpy.ops.object.editmode_toggle()

    offset += 1


def new_text(text: str, x_offset: int):
    pass


import calendar


def create_day_line():
    days = calendar.day_name

    for day in days:
        print(day)


# Fonction pour créer une grille de dates dans Blender
def create_calendar_month(year, month, start_x, start_y, cell_size):
    # Générer le calendrier pour le mois spécifié
    cal = calendar.Calendar().itermonthdates(year, month)

    # Coordonnées de départ pour la première case de la grille
    x, y = start_x, start_y

    # Boucle sur chaque jour du mois
    for dt in cal:
        # Créer un texte pour afficher le jour
        bpy.ops.object.text_add(enter_editmode=False, location=(x, y, 0))
        bpy.context.object.data.body = str(dt.day)
        bpy.context.object.scale = (0.5, 0.5, 0.5)  # Ajuster la taille du texte

        # Déplacer les coordonnées pour la prochaine case de la grille
        x += cell_size
        # Si nous atteignons la fin de la ligne, réinitialiser x et descendre à la ligne suivante
        if x - start_x >= 7 * cell_size:
            x = start_x
            y -= cell_size


# Paramètres de la grille de dates
year = 2024
month = 2  # Février 2024
start_x = 0
start_y = 0
cell_size = 1  # Taille de la cellule de la grille

# Créer la grille de dates dans Blender
# create_calendar_month(year, month, start_x, start_y, cell_size)

