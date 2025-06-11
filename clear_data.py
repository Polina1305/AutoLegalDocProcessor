import os
import fitz
from PIL import Image
import shutil


'''
Очистка данных перед обучением нейросети.
'''

INPUT_FOLDER = "Материалы ИИ ХАКАТОН"


# Переименование всех папок в формат 1..41
def rename_folders_and_files(root_directory):
    for folder_name in os.listdir(root_directory):
        if os.path.isdir(os.path.join(root_directory, folder_name)):
            old_folder_path = os.path.join(root_directory, folder_name)
            new_folder_name = str(int(folder_name.split()[1]))
            new_folder_path = os.path.join(root_directory, new_folder_name)
            os.rename(old_folder_path, new_folder_path)

            # Переименование файлов внутри каждой папки
            for file_name in os.listdir(new_folder_path):
                file_path = os.path.join(new_folder_path, file_name)
                if file_name.lower().endswith('.pdf'):
                    # Название для PDF файлов
                    if "договор аренды" in file_name.lower() or "договор" in file_name.lower():
                        new_file_name = "договор.pdf"
                    elif "расчет" in file_name.lower():
                        new_file_name = "расчёт.pdf"
                    elif "претензия" in file_name.lower():
                        new_file_name = "претензия.pdf"
                    else:
                        new_file_name = file_name
                    os.rename(file_path, os.path.join(new_folder_path, new_file_name.lower()))

                elif file_name.lower().endswith('.docx'):
                    new_docx_name = f"{new_folder_name}.docx"  # Название должно быть равно номеру папки
                    os.rename(file_path, os.path.join(new_folder_path, new_docx_name))
                elif file_name.lower().endswith('.doc'):
                    shutil.rmtree(new_folder_path)
                    break


rename_folders_and_files(INPUT_FOLDER)


# Конвертация всех пдфок в картинки
def pdf_to_images(pdf_path, output_directory):
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(os.path.join(output_directory, f"page_{page_number + 1}.jpg"))  # Сохранение изображения


def convert_pdfs_to_images(root_directory):
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name.lower().endswith('.pdf'):
                    pdf_document_type = file_name.split('.')[0]
                    output_directory = os.path.join(folder_path, pdf_document_type)
                    os.makedirs(output_directory, exist_ok=True)
                    pdf_to_images(file_path, output_directory)


convert_pdfs_to_images(INPUT_FOLDER)
