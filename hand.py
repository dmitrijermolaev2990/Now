import cv2
import numpy as np
import os

# Указываем путь к папке с изображением
excel_path = '/Users/dmitrij/Desktop/1/'
image_path = os.path.join(excel_path, 'hand.jpg')  # Подставь свое имя файла

# Загружаем изображение
image = cv2.imread(image_path)

if image is None:
    print(f"Ошибка: не удалось загрузить изображение по пути {image_path}")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Детекция краев с помощью Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Поиск линий методом Хафа
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Отображение найденных линий на изображении
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Показываем результат
    cv2.imshow("Hand Lines", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
