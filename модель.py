import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Загрузка предобученной модели DenseNet201
model = tf.keras.applications.DenseNet201(
    weights='/Users/dmitrij/Desktop/1/densenet201_weights.h5', input_shape=(224, 224, 3)
)

# Путь к изображению
image_path = "/Users/dmitrij/Desktop/1/hand.jpg"
image = cv2.imread(image_path)

# Проверим загрузку изображения
if image is None:
    print("Ошибка: не удалось загрузить изображение.")
else:
    print("Изображение загружено успешно.")

# Преобразуем изображение в нужный формат для подачи в модель
image_resized = cv2.resize(image, (224, 224))  # Преобразуем изображение в размер 224x224
image_input = np.expand_dims(image_resized, axis=0) / 255.0  # Нормализуем изображение

# Применяем модель для прогнозирования
predictions = model.predict(image_input)

# Отображаем исходное изображение
plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB))  # Преобразуем BGR в RGB
plt.axis("off")
plt.show()

# Декодируем предсказание
decoded_predictions = tf.keras.applications.densenet.decode_predictions(predictions)

# Выводим первые 3 предсказания
for i, (imagenet_id, label, score) in enumerate(decoded_predictions[0]):
    print(f"{i+1}: {label} (ID: {imagenet_id}) - Вероятность: {score:.2f}")
