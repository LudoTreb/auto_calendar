import calendar
from pathlib import Path

import bpy

# Paramètres
render_output_path = Path(__file__).parent / "ress/image-test.jpg"
# Chemin vers le fichier de police
font_roman_path = (
    Path(__file__).parent / "ress/fonts/Helvetica LT Std/HelveticaLTStd-Roman.otf"
)
font_bold_path = (
    Path(__file__).parent / "ress/fonts/Helvetica LT Std/HelveticaLTStd-Bold.otf"
)
image_ref = Path(__file__).parent / "ress/ref/Calendar-2024_jan.png"

font_bold = str(font_bold_path)
font_roman = str(font_roman_path)

# info year
year = 2024
year_pos = (1.5, 1.777, 0)
year_scale = (0.175, 0.175, 0.175)


# Size canvas
canvas_dim = (1.78, 2.502)
canvas_pos = (0, 0, -0.001)

# Setting render
cam_pos = (0, 0, 6.967)
scene_resolution = (3508, 4961)
cam_ortho_scale = 5

light_pos = (0, 0, 2)
light_scale = (8, 8, 0)
light_power = 5500


# Paramètres de la grille de dates
start_date_x = -1.35
start_date_y = 0.68
scale_date = (0.2, 0.2, 0.2)

cell_size = 0.46  # Taille de la cellule de la grille

# Paramètres de la grille des jours
day_pos = (-1.35, 1, 0)
day_scale = (0.10, 0.10, 0.10)

start_day_x = -1.35
start_day_y = 1
scale_day = (0.10, 0.10, 0.10)

# Paramètres de la grille des barres
start_line_x = -0.5
start_line_y = -0.5

# Position de l'année


# Position du mois
month_pos = (-1.45, 1.9, 0)
month_pos_2 = (-1.45, 1.9, -0.0006)
month_scale = (0.8, 0.8, 0.8)

month_pos_x = -1.45
month_pos_y = 1.420
scale_month_factor = 0.8
scale_month = (scale_month_factor, scale_month_factor, scale_month_factor)

# Infos ligne de separation
line_pos = (0, 0.9, 0)
line_scale = (1.65, -0.003, 1)
line_offset = 0.55

# Info bloc noir
bloc_pos = (0, 1.9095, -0.0005)
bloc_scale = (1.78, 0.631, 1)
# TODO créer un fonction pour la création de material.
# On aurait en parametre si mat=true alors pas specular ni roughness et juste le tuple rgb en diffuse
# Les couleurs / material
black_material = bpy.data.materials.new(name="Black")
black_material.diffuse_color = (0, 0, 0, 1)
black_material.specular_intensity = 0
black_material.roughness = 0

gray_material = bpy.data.materials.new(name="Gray")
gray_material.diffuse_color = (0.05, 0.05, 0.05, 1)
gray_material.specular_intensity = 0
gray_material.roughness = 0

white_material = bpy.data.materials.new(name="White")
white_material.diffuse_color = (1, 1, 1, 1)
white_material.specular_intensity = 0
white_material.roughness = 0


def create_text(
    text: str,
    text_location: tuple,
    material,
    font_path: str,
    scale: tuple,
    align=("LEFT", "TOP"),
):
    """Create a text objet.

    Args:
        text (str): the text that will display
        location (tuple): the coordonate x, y, z could be a tuple of 3 integer or float
        material (_type_): a material who as already load
        font_path (str): the path of the font
        scale (tuple): the scale x, y, z could be a tuple of 3 integer or float
        align (tuple, optional): Defaults to ('LEFT', 'TOP'). Align value available for the x axis are :
        LEFT, RIGHT, CENTER, JUSTIFY, FLUSH.
        Align value available for the y axis are:
        TOP, TOP BASELINE, MIDDLE, BOTTOM BASELINE, BOTTOM.
    """
    bpy.ops.object.text_add(enter_editmode=False, location=text_location)
    bpy.context.object.data.body = str(text)

    bpy.context.object.data.align_x = align[0]
    bpy.context.object.data.align_y = align[1]
    bpy.context.object.active_material = material
    bpy.context.object.data.font = bpy.data.fonts.load(font_path)
    bpy.context.object.scale = scale


def create_plane(mesh_pos: tuple, mesh_dim, color):
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        enter_editmode=False,
        align="WORLD",
        location=(mesh_pos[0], mesh_pos[1], mesh_pos[2]),
        scale=(1, 1, 1),
    )
    backgroung = bpy.context.object
    backgroung.active_material = color

    backgroung.scale.x = mesh_dim[0]
    backgroung.scale.y = mesh_dim[1]


def create_calendar_month(
    year, month, start_date_x, start_date_y, cell_size, item_one_pos
):
    # Générer le calendrier pour le mois spécifié
    cal = calendar.Calendar().itermonthdates(year, month)

    # Coordonnées de départ pour la première case de la grille
    x, y = start_date_x, start_date_y

    final_x = start_date_x + 6 * cell_size
    # Boucle sur chaque jour du mois
    line_pos = item_one_pos
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
            create_plane(line_pos, line_scale, gray_material)
            x = start_date_x
            y -= cell_size + 0.08

            temp_list = list(line_pos)
            temp_list[1] -= line_offset
            line_pos = tuple(temp_list)


def render_setting(
    cam_pos, resolution, ortho_scale, light_pos, light_scale, light_power, output_path
):
    bpy.context.scene.render.image_settings.file_format = "JPEG"
    bpy.context.scene.render.image_settings.quality = 100

    bpy.ops.object.light_add(
        type="AREA", align="WORLD", location=light_pos, scale=(1, 1, 1)
    )
    light = bpy.context.object
    light.data.use_shadow = False
    light.scale = light_scale
    light.data.energy = light_power

    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]

    bpy.ops.object.camera_add(
        enter_editmode=False,
        align="WORLD",
        location=cam_pos,
        rotation=(0, 0, 0),
        scale=(1, 1, 1),
    )
    camera = bpy.context.object
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = ortho_scale

    # Activer la vue de la caméra
    bpy.context.scene.camera = camera

    # Déclencher le rendu
    bpy.ops.render.render(write_still=True)

    # Sauvegarder l'image rendue
    bpy.data.images["Render Result"].save_render(str(output_path))


# TODO créer un pdf à partir de ces 12 jpeg et supprimer ces jpeg

# TODO Penser à comment bien organiser le code
"""definir les dossiers 1 pour le script principale qui fera appel
aux  fonction dans le dossier constructor.
et fichier data (json) qui renseignera tous les info sur tous les élements
présent dans la scène, couleur, position, scale des objets, les setting de rendu et autres
"""


render_output_folder = Path(__file__).parent / "ress/images"
months = calendar.month_name
days = calendar.day_name

for month_num in range(1, 13):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False, confirm=False)
    # définir le chemin pour l'enregistrement
    render_output_path = (
        render_output_folder / f"calendar_graphictypo_{year}_{month_num}.jpg"
    )

    # create the white backgound
    create_plane(canvas_pos, canvas_dim, white_material)

    # create the black block
    create_plane(bloc_pos, bloc_scale, black_material)

    # create the text year
    create_text(
        year, year_pos, white_material, font_roman, year_scale, align=("RIGHT", "TOP")
    )

    # create the month
    month_name_formatted = months[month_num][:3]
    create_text(month_name_formatted, month_pos, white_material, font_bold, month_scale)

    # create day's name line
    offset = cell_size
    day_pos_init = day_pos
    for day in range(7):
        day = days[day][:3]
        create_text(
            day,
            day_pos_init,
            black_material,
            font_roman,
            day_scale,
            align=("CENTER", "TOP"),
        )
        day_pos_temp = list(day_pos_init)
        day_pos_temp[0] += offset
        day_pos_init = tuple(day_pos_temp)

    # create all date of the month
    create_calendar_month(
        year, month_num, start_date_x, start_date_y, cell_size, line_pos
    )

    # render & save image
    render_setting(
        cam_pos,
        scene_resolution,
        cam_ortho_scale,
        light_pos,
        light_scale,
        light_power,
        render_output_path,
    )
