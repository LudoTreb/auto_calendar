import calendar
from pathlib import Path

font_bold_path = (
    Path(__file__).parent / "ress/fonts/Helvetica LT Std/HelveticaLTStd-Bold.otf"
)

year = 2024
month = 2

start_date_x = -1.35
start_date_y = 0.75
scale_date = (0.2, 0.2, 0.2)

cal = calendar.Calendar().itermonthdates(year, month)

# Coordonnées de départ pour la première case de la grille
x, y = start_date_x, start_date_y

final_x = start_date_x + 6 * cell_size

# Boucle sur chaque jour du mois
for dt in cal:
    # Créer un texte pour afficher le jour
    bpy.ops.object.text_add(enter_editmode=False, location=(x, y, 0))
    bpy.context.object.data.body = str(dt.day)
    bpy.context.object.data.align_x = "CENTER"
    bpy.context.object.data.font = bpy.data.fonts.load(str(font_bold_path))

    bpy.context.object.scale = scale_date  # Ajuster la taille du texte

    # Déplacer les coordonnées pour la prochaine case de la grille
    x += cell_size
    # Si nous atteignons la fin de la ligne, réinitialiser x et descendre à la ligne suivante
    if x > final_x:
        x = start_date_x
        y -= cell_size + 0.08
