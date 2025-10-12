import os
import cv2
import numpy as np
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import joblib
import pickle
import random

# Hàm tăng cường dữ liệu (data augmentation)
def augment_image(img):
    augmentations = []

    # Lật ảnh ngang
    if random.random() > 0.5:
        img = cv2.flip(img, 1)
    augmentations.append(img)

    # Dịch ảnh
    rows, cols, _ = img.shape
    dx = random.randint(-10, 10)
    dy = random.randint(-10, 10)
    M_translate = np.float32([[1, 0, dx], [0, 1, dy]])
    translated = cv2.warpAffine(img, M_translate, (cols, rows))
    augmentations.append(translated)

    # Xoay ảnh
    angle = random.uniform(-15, 15)
    M_rotate = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotated = cv2.warpAffine(img, M_rotate, (cols, rows))
    augmentations.append(rotated)

    # Làm mờ nhẹ
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    augmentations.append(blurred)

    # Thay đổi độ sáng
    brightness = random.uniform(0.7, 1.3)
    bright = np.clip(img * brightness, 0, 255).astype(np.uint8)
    augmentations.append(bright)

    return augmentations  # Trả về nhiều ảnh augment


embedder = FaceNet()
dataset_dir = 'D:/OpenCv/OpenCv/data/dataset'
X, y = [], []

for person in os.listdir(dataset_dir):
    person_path = os.path.join(dataset_dir, person)
    if not os.path.isdir(person_path):
        continue

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)
        img = cv2.imread(image_path)
        try:
            img = cv2.resize(img, (160, 160))
            # Thêm ảnh gốc
            embedding = embedder.embeddings([img])[0]
            X.append(embedding)
            y.append(person)

            # Thêm ảnh augment
            aug_images = augment_image(img)
            for aug_img in aug_images:
                aug_embedding = embedder.embeddings([aug_img])[0]
                X.append(aug_embedding)
                y.append(person)
        except Exception as e:
            print(f"Bỏ qua ảnh lỗi: {image_path} ({e})")

# Huấn luyện SVM
le = LabelEncoder()
y_encoded = le.fit_transform(y)
model = SVC(kernel='linear', probability=True)
model.fit(X, y_encoded)

# Lưu model và encoder
joblib.dump(model, 'D:/OpenCv/OpenCv/data/face_model.pkl')
joblib.dump(le, 'D:/OpenCv/OpenCv/data/label_encoder.pkl')

# Lưu toàn bộ embedding
with open('D:/OpenCv/OpenCv/data/known_embeddings.pkl', 'wb') as f:
    pickle.dump({'embeddings': X, 'names': y}, f)

print("✅ Huấn luyện xong model với data augmentation và đã lưu embedding.")
