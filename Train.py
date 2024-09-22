import cv2
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Đọc dữ liệu từ thư mục dataset
path = '/TTNT/OpenCv/dataset'
data = []
labels = []

# Danh sách nhãn cụ thể
names = ['Bo', 'Thi', 'Trump', 'Musk', 'Quan', 'Hoan']  # Danh sách tên sinh viên

def getImagesAndLabels(path, names):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.png'))]
    
    for imagePath in imagePaths:
        img = cv2.imread(imagePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        img = cv2.resize(img, (64, 64))  
        data.append(img)
        
        # Gán nhãn dựa trên tên tệp
        student_name = os.path.basename(imagePath).split('.')[0]  # Lấy tên file
        if student_name in names:
            label = names.index(student_name)  # Gán nhãn tương ứng với vị trí trong danh sách
            labels.append(label)

    return np.array(data), np.array(labels)

data, labels = getImagesAndLabels(path, names)
data = data.astype('float32') / 255.0  # Chuẩn hóa dữ liệu
data = np.expand_dims(data, axis=-1)  # Thêm chiều cho kênh màu

# Kiểm tra số lớp
num_classes = len(names)
print(f'Số lớp: {num_classes}')

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Kiểm tra xem các nhãn có nằm trong khoảng từ 0 đến num_classes - 1 không
if np.max(y_train) >= num_classes or np.min(y_train) < 0:
    print("Có nhãn không hợp lệ trong dữ liệu huấn luyện!")
    exit()

# Chuyển đổi nhãn thành dạng one-hot encoding
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# Xây dựng mô hình CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))
# Biên dịch mô hình
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print("\n Bắt đầu huấn luyện")
# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Lưu mô hình
model.save('/TTNT/OpenCv/trainer/face_recognition_model.keras')

print("\n Huấn luyện xong và mô hình đã được lưu.")
