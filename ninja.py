import tkinter as tk
from tkinter import PhotoImage

class AplikasiGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Aplikasi GUI dengan Gambar Bergerak")

        # Mengatur ukuran dan warna latar belakang
        self.geometry("450x600")
        self.configure(bg="blue")

        # Membuat garis kuning di atas (persegi panjang)
        tk.Canvas(self, bg="yellow", height=10, width=450).pack()

        # Menambahkan frame untuk gambar dengan latar belakang biru
        frame_gambar = tk.Frame(self, bg="blue")
        frame_gambar.pack()

        # Menambahkan gambar ke dalam frame_gambar
        self.gambar = PhotoImage(file="ninja.gif")
        self.gambar_label = tk.Label(frame_gambar, image=self.gambar, bg="blue")
        self.gambar_label.pack()

        # Membuat garis kuning di tengah (persegi panjang)
        tk.Canvas(self, bg="yellow", height=10, width=450).pack()

        # Menambahkan frame untuk tombol dengan latar belakang kuning
        frame_tombol = tk.Frame(self, bg="yellow")
        frame_tombol.pack(pady=10)

        # Menambahkan tombol btn_kiri dan btn_kanan dengan warna merah dan hijau
        tk.Button(frame_tombol, text="Gerak Kiri", command=self.gerak_kiri, bg="red").pack(side="left", padx=10)
        tk.Button(frame_tombol, text="Gerak Kanan", command=self.gerak_kanan, bg="green").pack(side="right", padx=10)

        # Membuat garis kuning di bawah (persegi panjang)
        tk.Canvas(self, bg="yellow", height=10, width=450).pack()

    def gerak_kiri(self):
        current_x = self.gambar_label.winfo_x()
        self.gambar_label.place(x=current_x - 10, y=0)

    def gerak_kanan(self):
        current_x = self.gambar_label.winfo_x()
        self.gambar_label.place(x=current_x + 10, y=0)

if __name__ == "__main__":
    aplikasi = AplikasiGUI()
    aplikasi.mainloop()
