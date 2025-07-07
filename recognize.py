import cv2
from mtcnn import MTCNN
from keras_facenet import FaceNet
import joblib
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.6
CONFIDENCE_THRESHOLD = 0.8

detector = MTCNN()
embedder = FaceNet()

model = joblib.load('D:/OpenCv/OpenCv/data/face_model.pkl')
label_encoder = joblib.load('D:/OpenCv/OpenCv/data/label_encoder.pkl')

with open('D:/OpenCv/OpenCv/data/known_embeddings.pkl', 'rb') as f:
    known = pickle.load(f)

known_embeddings = known['embeddings']
known_names = known['names']

cam = cv2.VideoCapture(0)

print("🎥 Nhấn 'q' để thoát.")
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

            # 1. Dự đoán bằng model
            pred_prob = model.predict_proba([embedding])[0]
            max_index = np.argmax(pred_prob)
            confidence = pred_prob[max_index]

            if confidence > CONFIDENCE_THRESHOLD:
                name = label_encoder.inverse_transform([max_index])[0]
            else:
                # 2. So sánh cosine nếu model không chắc chắn
                sims = cosine_similarity([embedding], known_embeddings)[0]
                best_index = np.argmax(sims)
                best_score = sims[best_index]
                name = known_names[best_index] if best_score > SIMILARITY_THRESHOLD else "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        except:
            pass

    cv2.imshow("Diem Danh", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()