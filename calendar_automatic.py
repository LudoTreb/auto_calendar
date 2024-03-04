import calendar
from pathlib import Path

import bpy

# Path for the font
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


# Parameter of the date's grid
date_pos = (-1.35, 0.68, 0)
date_scale = (0.2, 0.2, 0.2)

# Size of a grid's cellule
cell_size = 0.46

# Parameters of the day's line
day_pos = (-1.35, 1, 0)
day_scale = (0.10, 0.10, 0.10)

# Parameters of month
month_pos = (-1.45, 1.9, 0)
month_pos_2 = (-1.45, 1.9, -0.0006)
month_scale = (0.8, 0.8, 0.8)

# Parameters of separate's line
line_pos = (0, 0.9, 0)
line_scale = (1.65, -0.003, 1)
line_offset = 0.55

# Parameter of the black plane
bloc_pos = (0, 1.9095, -0.0005)
bloc_scale = (1.78, 0.631, 1)


def create_material(
    name: str, diffuse_color: tuple, specular_intensity: int, roughness: int
):
    material = bpy.data.materials.new(name=name)
    material.diffuse_color = diffuse_color
    material.specular_intensity = specular_intensity
    material.roughness = roughness
    return material


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


def create_calendar_month(year, month, date_pos, date_scale, cell_size, item_one_pos):
    # Générer le calendrier pour le mois spécifié
    cal = calendar.Calendar().itermonthdates(year, month)

    # Coordonnées de départ pour la première case de la grille
    x, y = date_pos[0], date_pos[1]

    final_x = x + 6 * cell_size
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

        day_text.scale = date_scale  # Ajuster la taille du texte

        # Déplacer les coordonnées pour la prochaine case de la grille
        x += cell_size
        # Si nous atteignons la fin de la ligne, réinitialiser x et descendre à la ligne suivante

        if x > final_x:
            create_plane(line_pos, line_scale, gray_material)
            x = date_pos[0]
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


def delete_temp_folder(path_folder_to_delete):
    """Before delete the folder, it's checking if the folder name content temp

    Args:
        path_folder_to_delete (_type_): _description_
    """
    if (
        path_folder_to_delete.exists()
        and path_folder_to_delete.is_dir()
        and ("temp" in str(path_folder_to_delete))
    ):
        for item in path_folder_to_delete.iterdir():
            if item.is_file():
                item.unlink()

        path_folder_to_delete.rmdir()

    else:
        print("Le dossier n'existe pas")


def create_pdf_from_img(name_pdf: str, path_imgs_folder: str = "ress/temp_img"):
    """create one pdf from all images present in a list.

    Args:
        paht_imgs_folder (_type_): Path object of the images folder
        path_pdf_output (_type_): Path objet of the pdf file
    """
    # récupère sous une string tous les chemins des images jpeg dans une liste
    image_folder = Path(__file__).parent / path_imgs_folder
    image_paths = image_folder.glob("*.jpg")

    # convertis tous ces jpeg en pdf
    for image in image_paths:
        img = Image.open(image, "r")
        img_convert = img.convert("RGB")
        img_convert.save(f"{str(image)[:-3]}pdf")

    # Récupère sous une string tous les chemins des images pdf dans une liste
    pdf_paths = image_folder.glob("*.pdf")
    # Tri les pdf en ordre croissant par rapport à leur nom qui fini par un nombre
    pdf_paths_sorted = sorted(
        pdf_paths, key=lambda path: int(str(path).split("_")[-1].split(".")[0])
    )
    # créer une instance de Pdfwritter pour qui va permmettre de fusionner les pdf en un seul
    merger = PdfWriter()
    pdf_out_folder = Path(__file__).parent / "export"
    pdf_out_folder.mkdir()
    pdf_out_file = pdf_out_folder / name_pdf
    # fusionne les pdf en un seul
    for pdf in pdf_paths_sorted:
        merger.append(pdf)
    merger.write(pdf_out_file)
    merger.close

    # supprime le dossier temp
    delete_temp_folder(image_folder)


# TODO Penser à comment bien organiser le code
"""
Definir les dossiers 1 pour le script principale qui fera appel
aux  fonction dans le dossier constructor.
et fichier data (json) qui renseignera tous les info sur tous les élements
présent dans la scène, couleur, position, scale des objets, les setting de rendu et autres
"""


name_calendar = "calendar_graphictypo_2024.pdf"
render_output_folder = Path(__file__).parent / "ress"
months = calendar.month_name
days = calendar.day_name

black_material = create_material(
    "Black", diffuse_color=(0, 0, 0, 1), specular_intensity=0, roughness=0
)
gray_material = create_material(
    "Gray", diffuse_color=(0.05, 0.05, 0.05, 1), specular_intensity=0, roughness=0
)
white_material = create_material(
    "White", diffuse_color=(1, 1, 1, 1), specular_intensity=0, roughness=0
)


for month_num in range(1, 3):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False, confirm=False)

    # create the path of the folder temporary save the image jpeg
    temp_img_path = render_output_folder / "temp_img"
    if not temp_img_path.is_dir():
        temp_img_path.mkdir()

    render_output_path = temp_img_path / f"calendar_graphictypo_{year}_{month_num}.jpg"

    # create the white backgound
    create_plane(canvas_pos, canvas_dim, white_material)

    # create the black block
    create_plane(bloc_pos, bloc_scale, black_material)

    # create the text year
    create_text(
        year,
        year_pos,
        white_material,
        font_roman,
        year_scale,
        align=("RIGHT", "TOP"),
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
    create_calendar_month(year, month_num, date_pos, date_scale, cell_size, line_pos)

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


# TODO Trouver une solution pour lancer le script en une fois sans avoir à installer Pillow dans l'environnement de blender.
"""Une solution serait dans le script d'avoir une ligne qui lance la partie blender, l'execute et puis l'arrete. 
Puis on continue le script sur la création du pdf.
"""

# from PIL import Image
# from PyPDF2 import PdfWriter

# create_pdf_from_img(name_calendar)
