import cv2
import numpy as np
import matplotlib.pyplot as plt


# Функция для предварительной обработки и поиска контуров
def preprocess_and_find_contours(image):
    # Переводим в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Увеличиваем контрастность
    enhanced = cv2.equalizeHist(gray)

    # Размытие для удаления шума
    denoised = cv2.medianBlur(enhanced, 5)

    # Используем адаптивный порог для выделения объектов
    binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 7)

    # Применяем морфологическое закрытие для устранения мелких отверстий
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Находим контуры
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours, binary


# Путь к изображению
image_path = "/Users/dmitrij/Desktop/1/hand.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Ошибка: не удалось загрузить изображение.")
else:
    print("Изображение загружено успешно.")

# Обрабатываем изображение для поиска контуров
contours, binary_image = preprocess_and_find_contours(image)

# Создаем копию изображения для вывода
output_image = image.copy()

# Отображаем найденные контуры на изображении
cv2.drawContours(output_image, contours, -1, (255, 0, 0), 2)  # Синие контуры

# Показываем результат
plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

# Показываем бинарное изображение после обработки
plt.figure(figsize=(10, 5))
plt.imshow(binary_image, cmap='gray')
plt.axis("off")
plt.show()
