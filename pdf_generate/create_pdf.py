import json
from pathlib import Path

from PIL import Image
from PyPDF2 import PdfWriter

with open("data.json", "r") as json_file:
    data = json.load(json_file)

name_calendar = data["Settings"]["save"]["name"]


def delete_temp_folder(path_folder_to_delete: Path):
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
    # rerieves all jpeg paths in a list of string
    image_folder = Path.cwd() / path_imgs_folder
    image_paths = image_folder.glob("*.jpg")

    # convert all jpegs to pdf
    for image in image_paths:
        img = Image.open(image, "r")
        img_convert = img.convert("RGB")
        img_convert.save(f"{str(image)[:-3]}pdf")

    # retrieves all pdf paths in a list of string
    pdf_paths = image_folder.glob("*.pdf")

    # sort all pdf by their name ending who are an integer in ascending order
    pdf_paths_sorted = sorted(
        pdf_paths, key=lambda path: int(str(path).split("_")[-1].split(".")[0])
    )
    # create a PdfWriter instance to merge all pdf files into a single one
    merger = PdfWriter()
    pdf_out_folder = Path.cwd() / "***export_pdf"
    pdf_out_folder.mkdir()
    pdf_out_file = pdf_out_folder / name_pdf

    for pdf in pdf_paths_sorted:
        merger.append(pdf)
    merger.write(pdf_out_file)
    merger.close

    delete_temp_folder(image_folder)
