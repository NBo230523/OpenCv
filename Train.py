import cv2
import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Đường dẫn tới thư mục chứa dữ liệu
dataset_path = "D:/BTL TTNT/OpenCv/dataset_human/Train"

# Khởi tạo nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Danh sách lưu các đặc trưng ảnh và ID người dùng
faces = []
labels = []
label_map = {}

# Đọc dữ liệu từ các thư mục
current_label = 0
for folder_name in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder_name)
    if not os.path.isdir(folder_path):
        continue

    # Thêm ánh xạ từ tên thư mục vào ID
    label_map[folder_name] = current_label

    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)

        # Đọc ảnh và kiểm tra nếu ảnh được đọc thành công
        image = cv2.imread(image_path)
        if image is None:
            print(f"Không thể đọc ảnh từ: {image_path}")
            continue  # Bỏ qua ảnh này và tiếp tục với ảnh tiếp theo
        
        # Chuyển thành ảnh xám
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt trong ảnh
        faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces_detected:
            # Cắt khuôn mặt từ ảnh
            face = gray[y:y + h, x:x + w]
            
            # Thay đổi kích thước ảnh khuôn mặt về 64x64 để sử dụng với CNN
            face_resized = cv2.resize(face, (64, 64))

            # Lưu ảnh khuôn mặt và nhãn (chuyển tên thư mục thành ID)
            faces.append(face_resized)
            labels.append(current_label)

    # Tăng ID cho người tiếp theo
    current_label += 1

# Chuyển dữ liệu thành mảng NumPy và chuẩn hóa (chia cho 255 để giá trị từ 0-1)
faces = np.array(faces)
faces = faces / 255.0  # Chuẩn hóa ảnh

labels = np.array(labels)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(faces, labels, test_size=0.2, random_state=42)

# Thêm chiều thứ 3 cho ảnh (vì CNN yêu cầu ảnh có 3 chiều: chiều cao, chiều rộng và số kênh màu)
X_train = X_train.reshape(X_train.shape[0], 64, 64, 1)
X_test = X_test.reshape(X_test.shape[0], 64, 64, 1)

# Xây dựng mô hình CNN phức tạp hơn
model = tf.keras.Sequential([
    # Lớp Convolutional và Pooling đầu tiên
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),

    # Lớp Convolutional và Pooling thứ hai
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    # Lớp Convolutional và Pooling thứ ba
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    # Lớp Convolutional thứ tư (thêm một lớp Conv2D với bộ lọc lớn hơn)
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),

    # Lớp Batch Normalization
    tf.keras.layers.BatchNormalization(),

    # Lớp Dropout để giảm overfitting
    tf.keras.layers.Dropout(0.5),

    # Lớp Flatten để chuyển dữ liệu từ 2D sang 1D
    tf.keras.layers.Flatten(),

    # Lớp Dense mạnh mẽ với kích thước lớn hơn
    tf.keras.layers.Dense(512, activation='relu'),

    # Lớp Dense cuối cùng với số lớp đầu ra là số lượng người dùng
    tf.keras.layers.Dense(len(label_map), activation='softmax')  # Số lớp đầu ra = số người trong dataset
])

# Biên dịch mô hình
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Lưu mô hình đã huấn luyện
model.save('D:/BTL TTNT/OpenCv/trainer/face_recognition_model.keras')

print("Đã huấn luyện và lưu mô hình!")