import cv2
import tensorflow as tf

# Load model deteksi objek (contoh: EfficientDet)
model = tf.saved_model.load("path/to/your/detector_model")

# Inisialisasi kamera (ganti angka 0 dengan indeks kamera yang sesuai)
cap = cv2.VideoCapture(0)

while True:
    # Ambil frame dari kamera
    ret, frame = cap.read()

    # Proses frame menggunakan model deteksi objek
    detections = model(frame)

    # Tampilkan hasil deteksi pada frame
    # Implementasikan logika tampilan hasil deteksi sesuai kebutuhan

    # Tampilkan frame
    cv2.imshow("Deteksi Objek", frame)

    # Jika pengguna menekan tombol 'q', keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()
