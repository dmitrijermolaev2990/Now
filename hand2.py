import cv2
import numpy as np
import matplotlib.pyplot as plt

def skeletonize(img):
    skel = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while True:
        open_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
        temp = cv2.subtract(img, open_img)
        eroded = cv2.erode(img, element)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        if cv2.countNonZero(img) == 0:
            break
    return skel

def filter_contours(contours, min_length=50):
    filtered = []
    for cnt in contours:
        if cv2.arcLength(cnt, closed=False) > min_length:
            filtered.append(cnt)
    return filtered

# Путь к изображению
image_path = "/Users/dmitrij/Desktop/1/hand2.jpg"
image = cv2.imread(image_path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
equalized = cv2.equalizeHist(gray)
denoised = cv2.medianBlur(equalized, 5)

binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 15, 7)

kernel = np.ones((3, 3), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

skeleton = skeletonize(binary)

# Поиск длинных прямых линий
lines = cv2.HoughLinesP(skeleton, 1, np.pi / 180, threshold=40, minLineLength=80, maxLineGap=10)

# Поиск контуров (изогнутые линии) с фильтрацией
contours, _ = cv2.findContours(skeleton, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
filtered_contours = filter_contours(contours, min_length=100)

output_image = image.copy()

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Зеленые линии

cv2.drawContours(output_image, filtered_contours, -1, (255, 0, 0), 2)  # Синие изогнутые линии

plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()
