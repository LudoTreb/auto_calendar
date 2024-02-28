import calendar
from pathlib import Path

import bpy

# Paramètres

# Chemin vers le fichier de police
font_roman_path = (
    Path(__file__).parent / "ress/fonts/Helvetica LT Std/HelveticaLTStd-Roman.otf"
)
font_bold_path = (
    Path(__file__).parent / "ress/fonts/Helvetica LT Std/HelveticaLTStd-Bold.otf"
)
image_ref = Path(__file__).parent / "ress/ref/Calendar-2024_jan.png"

year = 2024

month = 1  # pour les essais Février 2024

# Paramètres de la grille de dates
start_date_x = -1.35
start_date_y = 0.68
scale_date = (0.2, 0.2, 0.2)

cell_size = 0.46  # Taille de la cellule de la grille

# Paramètres de la grille des jours
start_day_x = -1.35
start_day_y = 1
scale_day = (0.10, 0.10, 0.10)

# Paramètres de la grille des barres
start_line_x = -0.5
start_line_y = -0.5

# Position de l'année
year_pos_x = 1.5
year_pos_y = 1.777
scale_year_factor = 0.175
scale_year = (scale_year_factor, scale_year_factor, scale_year_factor)

# Position du mois
month_pos_x = -1.45
month_pos_y = 1.420
scale_month_factor = 0.8
scale_month = (scale_month_factor, scale_month_factor, scale_month_factor)


# Les couleurs / material
black_material = bpy.data.materials.new(name="Black")
black_material.diffuse_color = (0, 0, 0, 1)

gray_material = bpy.data.materials.new(name="Gray")
gray_material.diffuse_color = (0.5, 0.5, 0.5, 1)

white_material = bpy.data.materials.new(name="White")
white_material.diffuse_color = (1, 1, 1, 1)

# Size canvas
canvas_dim_x = 1.78
canvas_dim_y = 2.502
canvas_pos_x = 0
canvas_pos_y = 0
canvas_pos_z = -0.1

# les fonctions


#
def create_day_line(start_day_x, start_day_y):
    """create the line of the day"""
    days = calendar.day_name
    x, y = start_day_x, start_day_y

    for day in days:
        bpy.ops.object.text_add(enter_editmode=False, location=(x, y, 0))
        bpy.context.object.data.body = str(day[:3])
        bpy.context.object.data.align_x = "CENTER"

        bpy.context.object.active_material = black_material
        bpy.context.object.data.font = bpy.data.fonts.load(str(font_roman_path))

        bpy.context.object.scale = scale_day

        x += cell_size


def create_calendar_month(year, month, start_date_x, start_date_y, cell_size):
    # Générer le calendrier pour le mois spécifié
    cal = calendar.Calendar().itermonthdates(year, month)

    # Coordonnées de départ pour la première case de la grille
    x, y = start_date_x, start_date_y

    final_x = start_date_x + 6 * cell_size

    # Boucle sur chaque jour du mois
    for dt in cal:

        bpy.ops.object.text_add(enter_editmode=False, location=(x, y, 0))

        day_text = bpy.context.object
        day_text.data.body = str(dt.day)
        day_text.data.align_x = "CENTER"
        day_text.data.font = bpy.data.fonts.load(str(font_bold_path))

        if dt.month == month:
            day_text.active_material = black_material
        else:
            day_text.active_material = gray_material

        day_text.scale = scale_date  # Ajuster la taille du texte

        # Déplacer les coordonnées pour la prochaine case de la grille
        x += cell_size
        # Si nous atteignons la fin de la ligne, réinitialiser x et descendre à la ligne suivante
        if x > final_x:
            x = start_date_x
            y -= cell_size + 0.08


def create_month(month, month_pos_x, month_pos_y):
    months = calendar.month_name
    bpy.ops.object.text_add(
        enter_editmode=False, location=(month_pos_x, month_pos_y, 0)
    )
    bpy.context.object.data.body = str(months[month][:3])

    bpy.context.object.data.align_x = "LEFT"
    bpy.context.object.active_material = black_material
    bpy.context.object.data.font = bpy.data.fonts.load(str(font_bold_path))
    bpy.context.object.scale = scale_month


def create_year(year, year_pos_x, year_pos_y):
    bpy.ops.object.text_add(enter_editmode=False, location=(year_pos_x, year_pos_y, 0))
    bpy.context.object.data.body = str(year)

    bpy.context.object.data.align_x = "RIGHT"
    bpy.context.object.active_material = black_material
    bpy.context.object.data.font = bpy.data.fonts.load(str(font_roman_path))
    bpy.context.object.scale = scale_year


def create_plane(pos_x, pos_y, pos_z, scale_x, scale_y, color):
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        enter_editmode=False,
        align="WORLD",
        location=(pos_x, pos_y, pos_z),
        scale=(1, 1, 1),
    )
    backgroung = bpy.context.object
    backgroung.active_material = white_material

    backgroung.scale.x = canvas_dim_x
    backgroung.scale.y = canvas_dim_y


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False, confirm=False)

create_objet()
create_year(year, year_pos_x, year_pos_y)
create_month(1, month_pos_x, month_pos_y)
create_day_line(start_day_x, start_day_y)
create_calendar_month(year, month, start_date_x, start_date_y, cell_size)
