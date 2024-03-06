import calendar
import json
from pathlib import Path

import bpy

months = calendar.month_name
days = calendar.day_name

with open("data.json", "r") as json_file:
    data = json.load(json_file)

name_calendar = data["Settings"]["save"]["name"]
render_output_folder = (
    Path(__file__).parent / data["Settings"]["save"]["temp_render_path"]
)

font_roman = str(Path(__file__).parent / data["Fonts"]["roman_path"])
font_bold = str(Path(__file__).parent / data["Fonts"]["bold_path"])


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


def create_calendar_month(
    year,
    month,
    date_pos,
    date_scale,
    cell_size,
    item_one_pos,
    item_one_scale,
    item_one_offset,
):
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
        day_text.data.font = bpy.data.fonts.load(font_bold)

        if dt.month == month:
            day_text.active_material = black_material
        else:
            day_text.active_material = gray_material

        day_text.scale = date_scale  # Ajuster la taille du texte

        # Déplacer les coordonnées pour la prochaine case de la grille
        x += cell_size
        # Si nous atteignons la fin de la ligne, réinitialiser x et descendre à la ligne suivante

        if x > final_x:
            create_plane(line_pos, item_one_scale, gray_material)
            x = date_pos[0]
            y -= cell_size + 0.08

            temp_list = list(line_pos)
            temp_list[1] -= item_one_offset
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


black_material = create_material(
    data["Colors"]["black"]["name"],
    data["Colors"]["black"]["diffuse_color"],
    data["Colors"]["black"]["specular_intensity"],
    data["Colors"]["black"]["roughness"],
)
gray_material = create_material(
    data["Colors"]["gray"]["name"],
    data["Colors"]["gray"]["diffuse_color"],
    data["Colors"]["gray"]["specular_intensity"],
    data["Colors"]["gray"]["roughness"],
)
white_material = create_material(
    data["Colors"]["whihte"]["name"],
    data["Colors"]["whihte"]["diffuse_color"],
    data["Colors"]["whihte"]["specular_intensity"],
    data["Colors"]["whihte"]["roughness"],
)


for month_num in range(1, 3):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False, confirm=False)

    # create the path of the folder temporary save the image jpeg
    temp_img_path = render_output_folder / "temp_img"
    if not temp_img_path.is_dir():
        temp_img_path.mkdir()

    render_output_path = (
        temp_img_path
        / f'calendar_graphictypo_{data["Dates"]["year"]["year"]}_{month_num}.jpg'
    )

    # create the white backgound
    create_plane(
        data["Meshs"]["canvas"]["canvas_pos"],
        data["Meshs"]["canvas"]["canvas_dim"],
        white_material,
    )

    # create the black block
    create_plane(
        data["Meshs"]["top_block"]["bloc_pos"],
        data["Meshs"]["top_block"]["bloc_scale"],
        black_material,
    )

    # create the text year
    create_text(
        data["Dates"]["year"]["year"],
        data["Dates"]["year"]["year_pos"],
        white_material,
        font_roman,
        data["Dates"]["year"]["year_scale"],
        align=("RIGHT", "TOP"),
    )

    # create the month
    month_name_formatted = months[month_num][:3]
    create_text(
        month_name_formatted,
        data["Dates"]["month"]["month_pos"],
        white_material,
        font_bold,
        data["Dates"]["month"]["month_scale"],
    )

    # create day's name line
    offset = data["Dates"]["cell"]["cell_size"]
    day_pos_init = data["Dates"]["day"]["day_pos"]
    for day in range(7):
        day = days[day][:3]
        create_text(
            day,
            day_pos_init,
            black_material,
            font_roman,
            data["Dates"]["day"]["day_scale"],
            align=("CENTER", "TOP"),
        )
        day_pos_temp = list(day_pos_init)
        day_pos_temp[0] += offset
        day_pos_init = tuple(day_pos_temp)

    # create all date of the month
    create_calendar_month(
        data["Dates"]["year"]["year"],
        month_num,
        data["Dates"]["date"]["date_pos"],
        data["Dates"]["date"]["date_scale"],
        data["Dates"]["cell"]["cell_size"],
        data["Meshs"]["separate_line"]["line_pos"],
        data["Meshs"]["separate_line"]["line_scale"],
        data["Meshs"]["separate_line"]["line_offset"],
    )

    # render & save image
    render_setting(
        data["Settings"]["render"]["cam_pos"],
        data["Settings"]["render"]["scene_resolution"],
        data["Settings"]["render"]["cam_ortho_scale"],
        data["Settings"]["lighting"]["light_pos"],
        data["Settings"]["lighting"]["light_scale"],
        data["Settings"]["lighting"]["light_power"],
        render_output_path,
    )


# TODO Trouver une solution pour lancer le script en une fois sans avoir à installer Pillow dans l'environnement de blender.
"""Une solution serait dans le script d'avoir une ligne qui lance la partie blender, l'execute et puis l'arrete. 
Puis on continue le script sur la création du pdf.
"""

# from PIL import Image
# from PyPDF2 import PdfWriter

# create_pdf_from_img(name_calendar)


# TODO Define a function to create a grid with a specific order of vertice's index
"""From this grid we will position the day and date by recovering the position of the vertice grid.
"""

# the code for the creation of the grid in specific inex's order
# Dimensions de la grille
rows = 7
cols = 8

# Création d'une liste pour stocker les coordonnées des sommets
vertices = []

# Création d'une boucle pour générer les coordonnées des sommets
for x in range(rows):
    for y in range(cols):
        vertices.append((x, y, 0))  # Ajoute les coordonnées du sommet à la liste

# Création d'une liste pour stocker les indices des faces
faces = []

# Création d'une boucle pour générer les indices des faces
for y in range(rows - 1):
    for x in range(cols - 1):
        # Calcul des indices des sommets pour cette face
        v1 = x + y * cols
        v2 = v1 + 1
        v3 = v1 + cols
        v4 = v3 + 1
        # Ajout des indices des sommets à la liste des faces
        faces.append((v1, v2, v4, v3))  # Ajoute les indices de la face à la liste

# Création d'un nouveau mesh
mesh = bpy.data.meshes.new(name="Grid")

# Ajout des sommets et des faces au mesh
mesh.from_pydata(vertices, [], faces)

# Mise à jour du mesh
mesh.update()

# Création d'un nouvel objet contenant le mesh
obj = bpy.data.objects.new(name="Grid_Object", object_data=mesh)

# Ajout de l'objet à la scène
scene = bpy.context.scene
scene.collection.objects.link(obj)
