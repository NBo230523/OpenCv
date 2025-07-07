import cv2
from mtcnn import MTCNN
from keras_facenet import FaceNet
import pickle
import os

# Nhập thông tin
name = input("Nhập tên người mới: ")
cam = cv2.VideoCapture(0)
detector = MTCNN()
embedder = FaceNet()

if not os.path.exists(f'D:/OpenCv/OpenCv/data/dataset/{name}'):
    os.makedirs(f'D:/OpenCv/OpenCv/data/dataset/{name}')

count = 0
embeddings = []

print("📸 Nhấn 'q' để dừng.")
while True:
    ret, frame = cam.read()
    if not ret:
        break
    faces = detector.detect_faces(frame)
    for face in faces:
        x, y, w, h = face['box']
        x, y = max(0, x), max(0, y)
        cropped = frame[y:y+h, x:x+w]
        try:
            resized = cv2.resize(cropped, (160, 160))
            embedding = embedder.embeddings([resized])[0]
            embeddings.append(embedding)
            count += 1
            cv2.imwrite(f"D:/OpenCv/OpenCv/data/dataset/{name}/{count}.jpg", cropped)
        except:
            pass

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Them sinh vien", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 10:
        break

cam.release()
cv2.destroyAllWindows()

# Ghi vào known_embeddings.pkl
if os.path.exists('D:/OpenCv/OpenCv/data/known_embeddings.pkl') and os.path.getsize('D:/OpenCv/OpenCv/data/known_embeddings.pkl') > 0:
    with open('D:/OpenCv/OpenCv/data/known_embeddings.pkl', 'rb') as f:
        data = pickle.load(f)
else:
    data = {'embeddings': [], 'names': []}

data['embeddings'].extend(embeddings)
data['names'].extend([name] * len(embeddings))

with open('D:/OpenCv/OpenCv/data/known_embeddings.pkl', 'wb') as f:
    pickle.dump(data, f)


print(f"✅ Đã thêm {count} ảnh của {name} vào dữ liệu.")
