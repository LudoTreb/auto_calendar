import json
from pathlib import Path

from PIL import Image
from PyPDF2 import PdfWriter

with open("data.json", "r") as json_file:
    data = json.load(json_file)


pdf_out_folder = Path.cwd() / str(data["Settings"]["save"]["export_path"])


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
        print("The folder does not exist")


def merge_pdf_into_single_pdf(pdf_name: str, pdfs: list):
    """Generate one pdf file  from a several pdf files.

    Args:
        pdf_name (str): the name of the pdf file with extension .pdf
        pdfs (list): list of all pdf files
    """
    merger = PdfWriter()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(pdf_name)
    merger.close


def create_pdf_from_img(name_pdf: str, path_imgs_folder: str):
    """create one pdf from all images present in a list.

    Args:
        name_pdf (str): Path of the pdf file.
        paht_imgs_folder (_type_): Path of the images folder
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

    if not pdf_out_folder.exists():
        pdf_out_folder.mkdir()
        pdf_out_file = pdf_out_folder / name_pdf

        merge_pdf_into_single_pdf(pdf_out_file, pdf_paths_sorted)

    else:
        pdf_out_file = pdf_out_folder / name_pdf
        if pdf_out_file.exists():
            pdf_out_file.unlink()
            merge_pdf_into_single_pdf(pdf_out_file, pdf_paths_sorted)

    delete_temp_folder(image_folder)
