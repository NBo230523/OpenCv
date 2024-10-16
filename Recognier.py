import cv2
import dlib
import numpy as np
import os
# import time

# Đường dẫn đến các tệp mô hình
predictor_path = "/TTNT/OpenCv/shape_predictor_68_face_landmarks.dat"
face_encoder_path = "/TTNT/OpenCv/dlib_face_recognition_resnet_model_v1.dat"

# Tính dung lượng của các tệp mô hình
# predictor_size = os.path.getsize(predictor_path) / (1024 * 1024)  # MB
# face_encoder_size = os.path.getsize(face_encoder_path) / (1024 * 1024)  # MB

# Khởi tạo các mô hình
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
face_encoder = dlib.face_recognition_model_v1(face_encoder_path)

# Danh sách tên sinh viên và vector nhận diện khuôn mặt
names = []
face_descriptors = []  # Lưu các vector nhận diện
recognized_ids = set()  # Tập hợp ID đã nhận diện

# Đọc dữ liệu từ thư mục dataset
dataset_path = '/TTNT/OpenCv/dataset'  # Thay đổi nếu cần
for filename in os.listdir(dataset_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        name = filename.split('.')[0]  # Lấy tên từ tên tệp
        names.append(name)
        image_path = os.path.join(dataset_path, filename)  # Tạo đường dẫn đầy đủ
        img = cv2.imread(image_path)

        if img is None:
            print(f"Không thể đọc hình ảnh từ {image_path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            face_descriptor = face_encoder.compute_face_descriptor(img, shape)
            face_descriptors.append(np.array(face_descriptor))

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Không thể mở camera.")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("Không thể đọc khung hình từ camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    recognized_ids.clear()  # Reset tập hợp ID đã nhận diện

    # total_processing_time = 0  # Biến lưu tổng thời gian xử lý

    for face in faces:
        # start_time = time.time()  # Bắt đầu đếm thời gian
        shape = predictor(gray, face)
        face_descriptor = face_encoder.compute_face_descriptor(frame, shape)

        distances = [np.linalg.norm(face_descriptor - known_descriptor) for known_descriptor in face_descriptors]
        min_distance = min(distances)

        if min_distance < 0.6:
            index = distances.index(min_distance)
            name = names[index]
            recognized_ids.add(name)  # Thêm ID vào tập hợp đã nhận diện
            color = (0, 255, 0)  # Màu xanh cho khuôn mặt đã nhận diện
        else:
            name = "unknown"
            color = (0, 0, 255)  # Màu đỏ cho khuôn mặt không nhận diện

        # Tính toán thời gian nhận diện
        # end_time = time.time() # Kết thúc đếm thời gian
        # processing_time = end_time - start_time  # Thời gian xử lý tính bằng giây
        # total_processing_time += processing_time  # Cộng dồn thời gian vào tổng

        # Vẽ khung và hiển thị tên
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), color, 2)
        cv2.putText(frame, name, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        # Hiển thị thời gian nhận diện
        # cv2.putText(frame, f'Time: {processing_time:.3f} s', (face.left(), face.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Hiển thị tổng thời gian xử lý
    # avg_processing_time = total_processing_time / len(faces) if faces else 0
    # cv2.putText(frame, f'Trung binh: {avg_processing_time:.3f} s', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Hiển thị dung lượng của các tệp mô hình
    # cv2.putText(frame, f'shape_predictor: {predictor_size:.2f} MB', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    # cv2.putText(frame, f'face_recognition: {face_encoder_size:.2f} MB', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Hiển thị số lượng sinh viên đã nhận diện và tên của họ
    recognized_count = len(recognized_ids)
    names_recognized = ', '.join(recognized_ids)  # Tạo chuỗi tên đã nhận diện
    cv2.putText(frame, f"So sinh vien co mat: {recognized_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.putText(frame, f"Ten: {names_recognized}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow('Diem danh', frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:  # Nhấn 'Esc' để thoát
        break
    elif k == ord('r'):  # Nhấn 'r' để reset bộ đếm
        recognized_ids.clear()  # Xóa tập hợp đã nhận diện

cam.release()
cv2.destroyAllWindows()
