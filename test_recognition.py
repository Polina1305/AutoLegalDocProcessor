import fitz
import pytesseract
from PIL import Image
import re
from fuzzywuzzy import process

# Путь к вашему PDF файлу
pdf_path = 'Материалы ИИ ХАКАТОН/1/Претензия заполн.pdf'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_information(text):
    result = {}

    def find_best_match(word, choices):
        return process.extractOne(word, choices)

    # Извлечение номера договора
    match = re.search(r'договором\s+\w*\s+\w*\s+учкта\s+№\s*(\d+)', text, re.IGNORECASE)
    if match:
        result['%UCHNUM%'] = match.group(1)
    else:
        match = find_best_match('договор', text.split())
        if match[1] > 80:  # Устанавливаем порог схожести в 80 процентов
            result['%UCHNUM%'] = match[0]

    # Извлечение кадастрового номера и площади земельного участка
    match = re.search(r'земельный\s+участок\s+с\s+кадастровым\s+номером\s+(\d+)\s+площадью\s+(\d+)\s+\w*', text, re.IGNORECASE)
    if match:
        result['%UCHKADASTR%'] = match.group(1)
        result['%USCHSQ%'] = match.group(2)
    else:
        match = find_best_match('земельный участок', text.split())
        if match[1] > 80:  # Устанавливаем порог схожести в 80 процентов
            result['%UCHKADASTR%'] = match[0]

    # Извлечение суммы и периода задолженности
    match = re.search(r'на\s+сумму\s+(\d+)\s+за\s+период\s+с\s+(\d+)\s+по\s+(\d+)', text, re.IGNORECASE)
    if match:
        result['%DSUM%'] = match.group(1)
        result['%DOLGSTART%'] = match.group(2)
        result['%DOLGEND%'] = match.group(3)
    else:
        match = find_best_match('сумму', text.split())
        if match[1] > 80:  # Устанавливаем порог схожести в 80 процентов
            result['%DSUM%'] = match[0]

    # Извлечение информации о пенях
    match = re.search(r'уплатить\s+пеню\s+в\s+размере\s+(\d+)', text, re.IGNORECASE)
    if match:
        result['%PSUM%'] = match.group(1)
    else:
        match = find_best_match('пеню', text.split())
        if match[1] > 80:  # Устанавливаем порог схожести в 80 процентов
            result['%PSUM%'] = match[0]

    # Извлечение общей суммы задолженности
    match = re.search(r'общая\s+сумма\s+задолженности\s+по\s+арендной\s+плате\s+и\s+пеням\s+составляет\s+(\d+)', text, re.IGNORECASE)
    if match:
        result['%DOLGSUM%'] = match.group(1)
    else:
        match = find_best_match('задолженности', text.split())
        if match[1] > 80:  # Устанавливаем порог схожести в 80 процентов
            result['%DOLGSUM%'] = match[0]

    return result

def ocr_on_pdf(pdf_path):
    text = ''
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        image_list = page.get_pixmap()

        # Преобразование изображения в формат Pillow Image
        img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)

        # Применение OCR к изображению
        text += pytesseract.image_to_string(img, lang='rus')  # Укажите язык, если требуется другой язык

    pdf_document.close()
    return text





# Применение OCR к содержимому PDF с помощью pytesseract и PyMuPDF
ocr_text = ocr_on_pdf(pdf_path)
print(ocr_text)
res = extract_information(ocr_text)
print(res)
