import json
import subprocess
from pathlib import Path

from pdf_generate.create_pdf import create_pdf_from_img

with open("data.json", "r") as json_file:
    data = json.load(json_file)


def run_blender_script(my_script):

    executable_blender_path = data["Settings"]["blender"]["application_path"]

    command_blender = [
        executable_blender_path,
        "--background",
        "--python",
        my_script,
    ]

    subprocess.run(command_blender, check=True)


def main():

    name_calendar = f"{data['Settings']['save']['name']}{data['Dates']['year']['year']}{data['Settings']['save']['extension']}"
    path_img_folder = data["Settings"]["save"]["temp_render_path"]
    my_script = "blender_script/calendar_generate.py"

    run_blender_script(my_script)

    create_pdf_from_img(name_calendar, path_img_folder)


if __name__ == "__main__":
    main()
