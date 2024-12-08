import cv2
import tensorflow as tf
import numpy as np

# Tải mô hình đã huấn luyện
model = tf.keras.models.load_model('D:/BTL TTNT/OpenCv/trainer/face_recognition_model.keras')

# Tạo ánh xạ từ ID người dùng đến tên
label_map = {0: 'Bernard Arnault', 1: 'Bruce Willis',
             2: 'Elon Musk', 3: 'Jeff Bezos', 
             4: 'Leonardo DiCaprio', 5: 'Mark Zuckerberg'}

# Đọc ảnh từ file
image_path = 'D:/BTL TTNT/OpenCv/dataset_human/Test/Unknow/NoOne.jpg'
frame = cv2.imread(image_path)

if frame is None:
    print("Không thể đọc ảnh từ:", image_path)
    exit()

# Chuyển ảnh sang ảnh xám
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Tải bộ phân loại Haar Cascade cho khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Phát hiện khuôn mặt sử dụng OpenCV Haar Cascade
faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Kiểm tra xem có khuôn mặt nào được phát hiện không
if len(faces_detected) == 0:
    # Nếu không phát hiện khuôn mặt, hiển thị khung màu đỏ quanh toàn bộ ảnh
    cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 2)  # Khung đỏ quanh ảnh

    # Tính toán vị trí hiển thị chữ ở giữa khung hình
    text = "No Face Detected"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 255)  # Màu đỏ
    thickness = 2
    
    # Lấy kích thước chữ
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    
    # Hiển thị chữ vào trung tâm của ảnh
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)
else:
    # Nếu có khuôn mặt được phát hiện, xử lý từng khuôn mặt
    for (x, y, w, h) in faces_detected:
        # Cắt khuôn mặt từ ảnh
        face_roi = gray[y:y + h, x:x + w]
        
        # Thay đổi kích thước ảnh khuôn mặt về 64x64
        face_resized = cv2.resize(face_roi, (64, 64))

        # Chuẩn hóa ảnh (chia cho 255 để giá trị từ 0-1)
        face_normalized = face_resized / 255.0
        face_normalized = face_normalized.reshape(1, 64, 64, 1)

        # Dự đoán ID người dùng
        prediction = model.predict(face_normalized)
        
        # Lấy chỉ số của lớp với xác suất cao nhất (label)
        label = np.argmax(prediction)
        
        # Lấy độ tự tin (xác suất) của dự đoán
        confidence = np.max(prediction)

        # Nếu độ tự tin thấp hơn 50% (hoặc ngưỡng nào đó), xem như là "Unknown"
        if confidence < 0.5:
            name = "Unknown"
            # Vẽ khung màu đỏ nếu là "Unknown"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            name = label_map.get(label, "Unknown")
            # Vẽ khung màu xanh lá nếu có nhận diện đúng
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Hiển thị tên người dùng và vẽ hình chữ nhật quanh khuôn mặt
        cv2.putText(frame, name, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)  # Chỉnh fontScale = 0.7

# Hiển thị kết quả nhận diện khuôn mặt
cv2.imshow('Face Recognition with OpenCV Haar Cascade', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
