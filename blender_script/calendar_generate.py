import calendar
import json
from pathlib import Path

import bpy

months = calendar.month_name
days = calendar.day_name


data_path = str(Path.cwd() / "data.json")

with open(data_path, "r") as json_file:
    data = json.load(json_file)

name_calendar = data["Settings"]["save"]["name"]
render_output_folder = Path.cwd() / data["Settings"]["save"]["temp_render_path"]

font_roman = str(Path.cwd() / data["Fonts"]["regular_path"])
font_bold = str(Path.cwd() / data["Fonts"]["bold_path"])


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


def create_plane(mesh_pos: list[float], mesh_dim: list[float], color):
    """Create a plane with a specific coordonate and size and a material associate

    Args:
        mesh_pos (list): coordonate x, y, z of the mesh
        mesh_dim (list): scale factor x, y for un 2d mesh
        color (bpy.Material): Material with a specific color
    """
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
    year: int,
    month: int,
    date_pos: list[float],
    date_scale: list[float],
    cell_size: float,
    item_one_pos: list[float],
    item_one_scale: list[float],
    item_one_offset: float,
):
    """Create the design of a specific month with all dates.

    Args:
        year (int): year of the calendar
        month (int): the number of the month
        date_pos (list[float]): coordonates of the date
        date_scale (list[float]): size of the date
        cell_size (float): the offset distance between dates
        item_one_pos (list[float]): coordonates of the item
        item_one_scale (list[float]): size of the item
        item_one_offset (float): the offset distance between each item
    """

    # Generate an objet calendar for a specified month
    cal = calendar.Calendar().itermonthdates(year, month)

    # Define coordonates of the first date
    x, y = date_pos[0], date_pos[1]

    final_x = x + 6 * cell_size

    # For loop each date of the month
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
            day_text.active_material = white_material

        day_text.scale = date_scale

        x += cell_size

        # If we are at the end of the date line, we reset x and go down to next line with y offset
        if x > final_x:
            create_plane(line_pos, item_one_scale, gray_material)
            x = date_pos[0]
            y -= cell_size + 0.08

            temp_list = list(line_pos)
            temp_list[1] -= item_one_offset
            line_pos = tuple(temp_list)


def render_setting(
    cam_pos: list[float],
    resolution: list[int],
    ortho_scale: int,
    light_pos: list[float],
    light_scale: list[float],
    light_power: int,
    output_path: Path,
):
    """Add all elments and settings for a render scene like cam, light...
    And save the render file, a jpeg, in a specific folder.

    Args:
        cam_pos (list[float]): coordonates of the camera
        resolution (list[int]): resolution of the jpeg image render file
        ortho_scale (int): type of the camera
        light_pos (list[float]): coordonates of the light
        light_scale (list[float]): size of the light
        light_power (int): intensity of the light
        output_path (Path): path of the render file.
    """
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

    bpy.context.scene.camera = camera

    bpy.ops.render.render(write_still=True)

    bpy.data.images["Render Result"].save_render(str(output_path))


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


for month_num in range(1, 13):
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
        align=("RIGHT", "TOP"),
    )

    # create day's name line
    offset = data["Dates"]["cell"]["cell_size"]
    day_pos_init = data["Dates"]["day"]["day_pos"]
    for day in range(7):
        day = days[day][:1]
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
