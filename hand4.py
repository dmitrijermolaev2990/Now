import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# Загрузка предобученной модели U-Net (можно найти предобученные модели на GitHub)
# В этом примере используем заранее подготовленную модель для сегментации (например, U-Net или DeepLabV3)

# Если у вас есть заранее обученная модель U-Net, загрузите её
# В данном примере используем предварительно обученную модель DeepLabV3
model = tf.keras.applications.DenseNet201(weights='imagenet', input_shape=(None, None, 3))

# Путь к изображению
image_path = "/Users/dmitrij/Desktop/1/hand.jpg"
image = cv2.imread(image_path)

# Проверим загрузку изображения
if image is None:
    print("Ошибка: не удалось загрузить изображение.")
else:
    print("Изображение загружено успешно.")

# Преобразуем изображение в нужный формат для подачи в модель
image_resized = cv2.resize(image, (256, 256))  # Преобразуем изображение в размер, необходимый для модели
image_input = np.expand_dims(image_resized, axis=0) / 255.0  # Нормализуем изображение

# Применяем модель
predictions = model.predict(image_input)

# Выводим результат (если это сегментация, изображение будет с маской)
# Важно: в модели сегментации будет маска, и на её основе можно будет выделить кривые
plt.figure(figsize=(10, 5))
plt.imshow(predictions[0])
plt.axis("off")
plt.show()
