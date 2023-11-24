import cv2
import tkinter as tk
from pyzbar.pyzbar import decode
import numpy as np
import requests

def detect_stars(frame):
    # Placeholder for star detection
    # You can replace this with your own star detection algorithm
    # For simplicity, let's assume we're detecting stars as circular objects
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)

    return frame

def detect_and_decode(frame, cap, root):
    # Deteksi barcode menggunakan pyzbar
    barcodes = decode(frame)

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

            # Dapatkan informasi nutrisi
            nutrition_info = get_nutrition_info(barcode_data)

            # Tampilkan informasi nutrisi di Tkinter
            if nutrition_info:
                display_nutrition_info(nutrition_info)
            else:
                result_label.config(text="Could not fetch nutrition information")

            # Matikan kamera setelah barcode terdeteksi
            cap.release()
            root.destroy()

            return None  # Stop further processing

    return frame

def get_nutrition_info(food_name):
    api_endpoint = f"https://world.openfoodfacts.org/api/v0/product/{food_name}.json"
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        data = response.json()
        return extract_nutrition_info(data)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def extract_nutrition_info(data):
    product_data = data.get('product', {})
    nutriments = product_data.get('nutriments', {})

    nutrients = {
        'Energy': nutriments.get('energy-kcal_100g', 'Not available'),
        'Fat': nutriments.get('fat_100g', 'Not available'),
        'Saturated Fat': nutriments.get('saturated-fat_100g', 'Not available'),
        'Trans Fat': nutriments.get('trans-fat_100g', 'Not available'),
        'Cholesterol': nutriments.get('cholesterol_100g', 'Not available'),
        'Carbohydrates': nutriments.get('carbohydrates_100g', 'Not available'),
        'Sugars': nutriments.get('sugars_100g', 'Not available'),
        'Fiber': nutriments.get('fiber_100g', 'Not available'),
        'Proteins': nutriments.get('proteins_100g', 'Not available'),
        'Salt': nutriments.get('salt_100g', 'Not available'),
    }

    return nutrients

def display_nutrition_info(nutrition_info):
    # Tampilkan informasi nutrisi di Tkinter
    for nutrient, value in nutrition_info.items():
        tk.Label(result_label, text=f"{nutrient}: {value}", font=("Arial", 12)).pack(pady=2)

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Create the main Tkinter window
root = tk.Tk()
root.title("Barcode Scanner and Nutrition Tracker")

# Create GUI elements
result_label = tk.Label(root, font=("Arial", 12), justify="left")
result_label.pack(pady=10)

def update():
    # Baca frame dari kamera
    ret, frame = cap.read()

    # Panggil fungsi untuk mendeteksi dan mendecode barcode
    frame_with_barcode = detect_and_decode(frame, cap, root)

    # Deteksi dan tampilkan bintang
    frame_with_stars = detect_stars(frame_with_barcode)

    # Tampilkan frame dengan barcode dan bintang di jendela
    cv2.imshow('Barcode Scanner and Star Detector', frame_with_stars)

    # Jalankan fungsi ini setiap 100 milidetik
    root.after(100, update)

# Jalankan fungsi update pertama kali
update()

# Jalankan aplikasi Tkinter
root.mainloop()

# Bebaskan sumber daya
cv2.destroyAllWindows()
