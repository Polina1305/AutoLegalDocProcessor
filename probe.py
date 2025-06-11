import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def calculate_distance_between_2_points(p1, p2):
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis


def order_points(pts):
    pts = pts.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def store_process_image(file_name, image):
    path = file_name
    cv2.imwrite(path, image)


image_path = "img.jpg"
image = cv2.imread(image_path)
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresholded_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
inverted_image = cv2.bitwise_not(thresholded_image)
dilated_image = cv2.dilate(inverted_image, None, iterations=5)

contours, _ = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

rectangular_contours = []
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    if len(approx) == 4:
        rectangular_contours.append(approx)

max_area = 0
contour_with_max_area = None
for contour in rectangular_contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        contour_with_max_area = contour

contour_with_max_area_ordered = order_points(contour_with_max_area)

existing_image_width = image.shape[1]
existing_image_width_reduced_by_10_percent = int(existing_image_width * 0.9)

distance_between_top_left_and_top_right = calculate_distance_between_2_points(contour_with_max_area_ordered[0], contour_with_max_area_ordered[1])
distance_between_top_left_and_bottom_left = calculate_distance_between_2_points(contour_with_max_area_ordered[0], contour_with_max_area_ordered[3])

aspect_ratio = distance_between_top_left_and_bottom_left / distance_between_top_left_and_top_right

new_image_width = existing_image_width_reduced_by_10_percent
new_image_height = int(new_image_width * aspect_ratio)

pts1 = np.float32(contour_with_max_area_ordered)
pts2 = np.float32([[0, 0], [new_image_width, 0], [new_image_width, new_image_height], [0, new_image_height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
perspective_corrected_image = cv2.warpPerspective(image, matrix, (new_image_width, new_image_height))

color_red = (0, 0, 255)  # BGR (здесь красный цвет)
color_green = (0, 255, 0)
radius = 5  # Размер точки
thickness = 2  # Толщина -1 означает заполненную точку

x1_dolg = new_image_width - new_image_width // 4
y1_dolg = new_image_height - 50
x2_dolg = x1_dolg + 90
y2_dolg = y1_dolg + 45

x1_peni = new_image_width - new_image_width // 2 + new_image_width // 20
y1_peni = new_image_height - 50
x2_peni = x1_peni + 80
y2_peni = y1_peni + 45

# Остаток задолженность
cv2.rectangle(perspective_corrected_image, (x1_dolg, y1_dolg), (x2_dolg, y2_dolg), color_red, thickness)


# Остаток Пени
cv2.rectangle(perspective_corrected_image, (x1_peni, y1_peni), (x2_peni, y2_peni), color_green, thickness)

# Выделенные области на изображении
dolg_image = perspective_corrected_image[y1_dolg:y2_dolg, x1_dolg:x2_dolg]
peni_image = perspective_corrected_image[y1_peni:y2_peni, x1_peni:x2_peni]

# Преобразование областей в текст с помощью Tesseract
dolg_text = pytesseract.image_to_string(dolg_image)  # --psm 6 для анализа блока текста
peni_text = pytesseract.image_to_string(peni_image)
print(dolg_text, peni_text)
try:
    dolg_float = dolg_text.replace('\n', '').replace(',', '.')
    dolg_float = float(dolg_float)

    peni_float = peni_text.replace('\n', '').replace(',', '.')
    peni_float = float(peni_float)

    print(peni_float, dolg_float)
except Exception as e:
    print()


store_process_image('output.jpg', perspective_corrected_image)
