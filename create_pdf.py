import json
from pathlib import Path

from PIL import Image
from PyPDF2 import PdfWriter

with open("data.json", "r") as json_file:
    data = json.load(json_file)

name_calendar = data["Settings"]["save"]["name"]


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


if __name__ == "__main__":
    create_pdf_from_img(name_calendar)
