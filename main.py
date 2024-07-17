import cv2
import pymongo
from ultralytics import YOLO
from datetime import datetime

# Membuat koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["seeforme"]
collection = db["history"]

# Inisialisasi model YOLOv8
model = YOLO('model/best.pt')

# Pilihan untuk menentukan lokasi deteksi (indoor/outdoor)
location = input("Apakah deteksi dilakukan di 'indoor' atau 'outdoor'? ").strip().lower()
if location not in ['indoor', 'outdoor']:
    print("Pilihan tidak valid. Default ke 'indoor'.")
    location = 'indoor'

# Mulai video capture dari kamera
cap = cv2.VideoCapture(0)

while True:
    # Ambil frame dari kamera
    ret, frame = cap.read()
    if not ret:
        break

    # Lakukan deteksi
    results = model(frame)

    # Tampilkan hasil deteksi pada frame
    result_image = results[0].plot()  # Ambil elemen pertama dan tampilkan bounding box
    cv2.imshow("Deteksi YOLO", result_image)  # Gunakan OpenCV untuk menampilkan gambar

    # Simpan hasil deteksi ke MongoDB
    detection_time = datetime.now()

    for result in results:
        for box in result.boxes:
            class_name = model.names[int(box.cls)]
            confidence = float(box.conf)
            bounding_box = [int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(box.xyxy[0][3])]

            doc = {
                "object_name": class_name,
                "detection_time": detection_time,
                "location": location,
                "confidence": confidence,
                "bounding_box": bounding_box,
                "source": "camera"
            }
            collection.insert_one(doc)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan
cap.release()
cv2.destroyAllWindows()


# # *******************************************************************************
# import cv2
# import pymongo
# from ultralytics import YOLO
# from datetime import datetime

# # Membuat koneksi ke MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["seeforme"]
# collection = db["seeformecoll"]

# # Inisialisasi model YOLOv8
# model = YOLO('model/best.pt')

# # Pilihan untuk menentukan lokasi deteksi (indoor/outdoor)
# location = input("Apakah deteksi dilakukan di 'indoor' atau 'outdoor'? ").strip().lower()
# if location not in ['indoor', 'outdoor']:
#     print("Pilihan tidak valid. Default ke 'indoor'.")
#     location = 'indoor'

# # Mulai video capture dari kamera
# cap = cv2.VideoCapture(0)

# while True:
#     # Ambil frame dari kamera
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Lakukan deteksi
#     results = model(frame)

#     # Tampilkan hasil deteksi pada frame
#     result_image = results[0].plot()  # Ambil elemen pertama dan tampilkan bounding box
#     cv2.imshow("Deteksi YOLO", result_image)  # Gunakan OpenCV untuk menampilkan gambar

#     # Simpan nama objek hasil deteksi ke MongoDB
#     for result in results:
#         detected_objects = set()
#         detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         for box in result.boxes:
#             class_name = model.names[int(box.cls)]
#             detected_objects.add(class_name)

#         for obj in detected_objects:
#             collection.insert_one({
#                 "object_name": obj,
#                 "detection_time": detection_time,
#                 "location": location
#             })

#     # Tekan 'q' untuk keluar
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Bersihkan
# cap.release()
# cv2.destroyAllWindows()
# # *******************************************************************************



# # ===============================================================================
# import cv2
# import pymongo
# from ultralytics import YOLO

# # Membuat koneksi ke MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["see4me"]
# collection = db["see4mecoll"]

# # Inisialisasi model YOLOv8
# model = YOLO('model/best.pt')

# # Mulai video capture dari kamera
# cap = cv2.VideoCapture(0)

# while True:
#     # Ambil frame dari kamera
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Lakukan deteksi
#     results = model(frame)

#     # Tampilkan hasil deteksi pada frame
#     result_image = results[0].plot()  # Ambil elemen pertama dan tampilkan bounding box
#     cv2.imshow("Deteksi YOLO", result_image)  # Gunakan OpenCV untuk menampilkan gambar

#     # Simpan nama objek hasil deteksi ke MongoDB
#     for result in results:
#         detected_objects = set()

#         for box in result.boxes:
#             class_name = model.names[int(box.cls)]
#             detected_objects.add(class_name)

#         for obj in detected_objects:
#             collection.insert_one({"object_name": obj})

#     # Tekan 'q' untuk keluar
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Bersihkan
# cap.release()
# cv2.destroyAllWindows()

# # ============================================
# # from ultralytics import YOLO

# # model = YOLO('model/best.pt')

# # model.predict(source=0, show=True, conf=0.5)

# # ===============================================================================