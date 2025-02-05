import cv2
import numpy as np
import os

# Путь к изображению
excel_path = '/Users/dmitrij/Desktop/1/'
image_path = os.path.join(excel_path, 'hand2.jpg')  # Подставь свое имя файла

# Загрузка изображения
image = cv2.imread(image_path)

if image is None:
    print(f"Ошибка: не удалось загрузить изображение по пути {image_path}")
else:
    # Перевод в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Адаптивная бинаризация для лучшего контраста
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 5)

    # Уменьшение шумов морфологическими операциями
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Отрисовка контуров (линий ладони)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 1)

    # Показываем результат
    cv2.imshow("Palm Lines Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
