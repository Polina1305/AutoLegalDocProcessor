import fitz  # PyMuPDF
from PIL import Image


def pdf_to_images(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    return images


# Пример использования
pdf_file_path = "договор.pdf"
images = pdf_to_images(pdf_file_path)

# Сохранение изображений (необязательно)
for i, img in enumerate(images):
    img.save(f"output_image_{i}.jpg")
