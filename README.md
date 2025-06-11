# AutoLegalDocProcessor

Система автоматической обработки юридических документов с компьютерным зрением и ML

## Описание
Проект представляет собой комплексное решение для:
-  Автоматической классификации юридических документов
-  Извлечения структурированных данных (договоры, претензии, расчеты)
-  Генерации новых документов на основе шаблонов
-  Обработки сканированных документов и PDF-файлов

## Технологический стек
| Категория | Технологии |
|-----------|------------|
| Язык | ![Python](https://img.shields.io/badge/Python-3.8+-blue) |
| OCR | ![Tesseract](https://img.shields.io/badge/Tesseract-5.0-green) |
| CV | ![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-brightgreen) |
| ML | ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange) ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-blue) |
| PDF | ![PyMuPDF](https://img.shields.io/badge/PyMuPDF-fitz-red) |
| DOCX | ![python-docx](https://img.shields.io/badge/python--docx-0.8-lightgrey) |
| Images | ![Pillow](https://img.shields.io/badge/Pillow-9.0-yellow) |

## Модели машинного обучения

### 1. Классификатор документов
```python
model = Sequential([
    Dense(128, input_shape=(X.shape[1],), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])
```
Тип: Бинарная классификация

Входные данные: Текст (векторизованный через CountVectorizer)

Выход: 0 - арбитражный суд, 1 - нет

2. Система извлечения информации
Гибридный подход:

-  Регулярные выражения (ключевые поля)
-  Fuzzy matching (неточные совпадения)
-  Юридические шаблоны

3. Обработчик изображений
-  Детекция областей (OpenCV)
-  Перспективная коррекция
-  Выделение табличных данных

Установка
```
# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Установка Tesseract OCR
# Для Windows (скачать с https://github.com/UB-Mannheim/tesseract/wiki)
# Для Linux:
sudo apt install tesseract-ocr libtesseract-dev

# 3. Запуск
python main.py --input_folder Материалы_ИИ_ХАКАТОН
Структура проекта
```
Структура проекта
```
project/
├── Материалы_ИИ_ХАКАТОН/       # Входные данные
├── templates/                  # Шаблоны документов
│   ├── fiz_p.docx              # Шаблон претензии
│   └── ...                     
├── processed/                  # Обработанные документы
├── models/                     # ML модели
│   └── classifier.h5           # Сохраненная модель
├── utils/
│   ├── pdf_processor.py        # Обработка PDF
│   ├── image_processor.py      # CV-обработка
│   ├── doc_generator.py        # Генерация DOCX
│   └── ml_models.py            # Модели ML
├── main.py                     # Точка входа
└── requirements.txt            # Зависимости
```
Примеры использования:

Обработка документа
```
from utils.pdf_processor import process_document
data = process_document("договор.pdf")
```
Генерация претензии
```
from utils.doc_generator import generate_claim
generate_claim(
    template_path="templates/fiz_p.docx",
    output_path="претензия_123.docx",
    data={
        "%UCHNUM%": "12345",
        "%DSUM%": "50000 руб"
    }
)
```
Контакты:

Автор: Полина

Email: smolyak-polina@mail.ru

GitHub: [github.com/yourprofile](https://github.com/Polina1305)

Лицензия 
MIT License
