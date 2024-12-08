import cv2
from mtcnn import MTCNN
import os

# Mở camera
cam = cv2.VideoCapture(0)  # 0 là chỉ số của camera mặc định

# Kiểm tra xem camera có mở thành công không
if not cam.isOpened():
    print("\n Không thể mở camera. Vui lòng kiểm tra kết nối.")
    exit()

# Đặt kích thước camera
cam.set(3, 640)
cam.set(4, 480)

# Tải bộ phát hiện khuôn mặt
detector = MTCNN()

# Nhập ID và tên file từ người dùng
face_id = input('\n Nhập ID cho đối tượng: ')
file_name_prefix = input('Nhập tên đối tượng: ')  # Nhập tên file lưu trữ hình ảnh sinh viên sau khi phát diện

# Số lượng hình ảnh cần lấy
num_images = 10
count = 0

while count < num_images:
    # Đọc khung hình từ camera
    ret, frame = cam.read()
    
    # Kiểm tra xem khung hình có được đọc thành công không
    if not ret:
        print("\n Không thể đọc khung hình từ camera.")
        break

    # Phát hiện khuôn mặt
    faces = detector.detect_faces(frame)

    for face in faces:
        x, y, width, height = face['box']
        # Vẽ hình chữ nhật quanh khuôn mặt
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)

        # Lưu khuôn mặt vào thư mục dữ liệu với tên tùy chỉnh
        face_image = frame[y:y + height, x:x + width]
        cv2.imwrite(f"D:/BTL TTNT/OpenCv/dataset/{file_name_prefix}.{face_id}.{count + 1}.jpg", face_image)
        count += 1

        # Dừng nếu đã đủ số lượng hình ảnh
        if count >= num_images:
            break

    # Hiển thị khung hình với khuôn mặt được phát hiện
    cv2.imshow('Face Detect', frame)

    # Thoát vòng lặp khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ
cam.release()
cv2.destroyAllWindows()

print("\n Thoat")