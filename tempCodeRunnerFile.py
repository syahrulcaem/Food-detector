import cv2
import tkinter as tk
from pyzbar.pyzbar import decode
import numpy as np

def detect_and_decode(frame):
    # Ubah frame ke dalam skala abu-abu
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi barcode menggunakan pyzbar
    barcodes = decode(gray)

    # Loop melalui barcode yang terdeteksi
    for barcode in barcodes:
        # Ambil koordinat pojok dari barcode
        points = barcode.polygon if barcode.polygon is not None else barcode.rect

        if len(points) == 4:
            pts = []
            for pt in points:
                pts.append([pt.x, pt.y])

            pts = sorted(pts, key=lambda x: x[1])

            # Gambar kotak di sekitar barcode
            pts = pts if len(pts) == 4 else [pts[0], pts[1], pts[3], pts[2]]  # Urutkan ulang titik jika diperlukan
            pts = pts + [pts[0]]  # Tambahkan titik pertama lagi untuk menutup poligon
            pts = np.array(pts, dtype=int)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Ambil data dari barcode
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            # Tampilkan data barcode di GUI
            result_label.config(text=f"Barcode Type: {barcode_type}, Data: {barcode_data}")

    return frame

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Create the main Tkinter window
root = tk.Tk()
root.title("Barcode Scanner")

# Create GUI elements
result_label = tk.Label(root, font=("Arial", 12), justify="left")
result_label.pack(pady=10)

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()

    # Panggil fungsi untuk mendeteksi dan mendecode barcode
    frame_with_barcode = detect_and_decode(frame)

    # Tampilkan frame dengan barcode di jendela
    cv2.imshow('Barcode Scanner', frame_with_barcode)

    # Hentikan loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()

root.mainloop()
