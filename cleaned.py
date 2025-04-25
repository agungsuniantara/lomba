import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os
import numpy as np
import math

class AplikasiNutrisi:
    def __init__(self, window):
        # ------ PENGATURAN DASAR APLIKASI ------
        self.window = window
        self.window.title("Aplikasi Nutrisi")
        self.window.geometry("1000x750")
        
        # Mengatur tema warna aplikasi
        self.style = ttk.Style()
        
        # Menyiapkan data asupan kalori
        self.data_kalori = {}
        
        # Membaca data dari file kalori jika ada
        self.nama_file = "calorie_data.json"
        self.baca_data_kalori()
        
        # ------ BAGIAN HEADER APLIKASI ------
        self.bingkai_judul = ttk.Frame(self.window, padding=10)
        self.bingkai_judul.pack(fill=X, pady=(10, 5))
        
        self.judul_aplikasi = ttk.Label(
            self.bingkai_judul, 
            text="APLIKASI NUTRISI",
            font=('Helvetica', 22, 'bold'),
            bootstyle=PRIMARY
        )
        self.judul_aplikasi.pack()
        
        self.sub_judul = ttk.Label(
            self.bingkai_judul,
            text="Pantau kebutuhan nutrisi harian Anda",
            font=('Helvetica', 12),
            bootstyle=SECONDARY
        )
        self.sub_judul.pack(pady=5)
        
        # ------ BUAT TAB UNTUK NAVIGASI ------
        self.tab_utama = ttk.Notebook(self.window, bootstyle=INFO)
        self.tab_utama.pack(expand=True, fill=BOTH, padx=15, pady=10)
        
        # Tab 1: Pelacak Makronutrien 
        self.tab_makro = ttk.Frame(self.tab_utama, padding=10)
        self.tab_utama.add(self.tab_makro, text="Pelacak Makronutrien")
        
        # Tab 2: Asupan Kalori Harian
        self.tab_kalori = ttk.Frame(self.tab_utama, padding=10)
        self.tab_utama.add(self.tab_kalori, text="Asupan Kalori Harian")
        
        # Siapkan isi kedua tab
        self.buat_tab_makronutrien()
        self.buat_tab_kalori()
        
        # ------ BAGIAN FOOTER ------
        self.bingkai_footer = ttk.Frame(self.window, padding=5)
        self.bingkai_footer.pack(side=BOTTOM, fill=X)
        
        self.teks_footer = ttk.Label(
            self.bingkai_footer,
            text=f"© {datetime.now().year} Aplikasi Nutrisi - v2.1",
            font=('Helvetica', 8),
            bootstyle=SECONDARY
        )
        self.teks_footer.pack(side=BOTTOM, fill=X, pady=5)

    # ------ FUNGSI UNTUK TAB MAKRONUTRIEN ------
    def buat_tab_makronutrien(self):
        # Wadah utama tab makronutrien
        self.bingkai_makro = ttk.Frame(self.tab_makro, padding=10)
        self.bingkai_makro.pack(expand=True, fill=BOTH)
        
        # Mengatur ukuran kolom dan baris
        self.bingkai_makro.columnconfigure(0, weight=1)
        self.bingkai_makro.columnconfigure(1, weight=1)
        self.bingkai_makro.rowconfigure(1, weight=1)
        
        # ------ BAGIAN INPUT MAKRONUTRIEN ------
        self.bingkai_input_makro = ttk.Labelframe(
            self.bingkai_makro, 
            text="Input Makronutrien",
            padding=15,
            bootstyle=INFO
        )
        self.bingkai_input_makro.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Input karbohidrat
        ttk.Label(
            self.bingkai_input_makro, 
            text="Karbohidrat (g):",
            bootstyle=INFO
        ).grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        self.input_karbo = ttk.Entry(self.bingkai_input_makro, width=15)
        self.input_karbo.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        # Input protein
        ttk.Label(
            self.bingkai_input_makro, 
            text="Protein (g):",
            bootstyle=INFO
        ).grid(row=1, column=0, padx=5, pady=10, sticky='w')
        
        self.input_protein = ttk.Entry(self.bingkai_input_makro, width=15)
        self.input_protein.grid(row=1, column=1, padx=5, pady=10, sticky='w')
        
        # Input lemak
        ttk.Label(
            self.bingkai_input_makro, 
            text="Lemak (g):",
            bootstyle=INFO
        ).grid(row=2, column=0, padx=5, pady=10, sticky='w')
        
        self.input_lemak = ttk.Entry(self.bingkai_input_makro, width=15)
        self.input_lemak.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        
        # Tombol hitung
        self.tombol_hitung_makro = ttk.Button(
            self.bingkai_input_makro, 
            text="Hitung Makronutrien", 
            command=self.hitung_makro,
            bootstyle=SUCCESS
        )
        self.tombol_hitung_makro.grid(row=3, column=0, columnspan=2, padx=5, pady=15, sticky='ew')
        
        # ------ BAGIAN DIAGRAM MAKRONUTRIEN ------
        self.bingkai_diagram_makro = ttk.Labelframe(
            self.bingkai_makro, 
            text="Visualisasi Makronutrien",
            padding=15,
            bootstyle=PRIMARY
        )
        self.bingkai_diagram_makro.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        # Persiapan diagram pie chart
        self.gambar_makro = Figure(figsize=(5, 4), dpi=100)
        self.plot_makro = self.gambar_makro.add_subplot(111)
        self.canvas_makro = FigureCanvasTkAgg(self.gambar_makro, self.bingkai_diagram_makro)
        self.canvas_makro.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Diagram pie chart awal (kosong)
        self.plot_makro.pie([1], labels=['Masukkan data'], colors=['#f5f5f5'])
        self.plot_makro.set_title('Distribusi Makronutrien')
        self.canvas_makro.draw()
        
        # ------ BAGIAN HASIL ANALISIS MAKRO ------
        self.bingkai_hasil_makro = ttk.Labelframe(
            self.bingkai_makro, 
            text="Hasil Analisis Makronutrien",
            padding=15,
            bootstyle=SUCCESS
        )
        self.bingkai_hasil_makro.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Label hasil analisis
        self.label_hasil_makro = ttk.Label(
            self.bingkai_hasil_makro, 
            text="Masukkan data makronutrien untuk melihat analisis", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.label_hasil_makro.pack(fill=X, pady=5)
        
        self.label_detail_makro = ttk.Label(
            self.bingkai_hasil_makro, 
            text="", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.label_detail_makro.pack(fill=X, pady=5)

    # ------ FUNGSI UNTUK TAB KALORI ------
    def buat_tab_kalori(self):
        # Wadah utama tab kalori
        self.bingkai_kalori = ttk.Frame(self.tab_kalori, padding=10)
        self.bingkai_kalori.pack(expand=True, fill=BOTH)
        
        # Mengatur ukuran kolom dan baris
        self.bingkai_kalori.columnconfigure(0, weight=1)
        self.bingkai_kalori.columnconfigure(1, weight=1)
        self.bingkai_kalori.rowconfigure(1, weight=1)
        
        # ------ BAGIAN INPUT KALORI ------
        self.bingkai_input_kalori = ttk.Labelframe(
            self.bingkai_kalori, 
            text="Input Asupan Kalori",
            padding=15,
            bootstyle=INFO
        )
        self.bingkai_input_kalori.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Input usia
        ttk.Label(
            self.bingkai_input_kalori, 
            text="Usia:",
            bootstyle=INFO
        ).grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        self.input_usia = ttk.Entry(self.bingkai_input_kalori, width=15)
        self.input_usia.grid(row=0, column=1, padx=5, pady=10, sticky='w')

        # Input jenis kelamin
        ttk.Label(
            self.bingkai_input_kalori, 
            text="Jenis Kelamin:",
            bootstyle=INFO
        ).grid(row=1, column=0, padx=5, pady=10, sticky='w')
        
        self.pilihan_kelamin = tk.StringVar(value='')
        self.combo_kelamin = ttk.Combobox(
            self.bingkai_input_kalori, 
            textvariable=self.pilihan_kelamin, 
            width=15, 
            values=('Laki-laki', 'Wanita'),
            state="readonly"
        )
        self.combo_kelamin.grid(row=1, column=1, padx=5, pady=10, sticky='w')
        
        # Input tingkat aktivitas
        ttk.Label(
            self.bingkai_input_kalori, 
            text="Tingkat Aktivitas:",
            bootstyle=INFO
        ).grid(row=2, column=0, padx=5, pady=10, sticky='w')
        
        self.pilihan_aktivitas = tk.StringVar(value='')
        self.combo_aktivitas = ttk.Combobox(
            self.bingkai_input_kalori, 
            textvariable=self.pilihan_aktivitas, 
            width=15,
            values=('Sedentary', 'Ringan', 'Sedang', 'Aktif'),
            state="readonly"
        )
        self.combo_aktivitas.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        
        # Input kalori hari ini
        ttk.Label(
            self.bingkai_input_kalori, 
            text="Kalori Hari Ini:",
            bootstyle=INFO
        ).grid(row=3, column=0, padx=5, pady=10, sticky='w')
        
        self.input_kalori_hari_ini = ttk.Entry(self.bingkai_input_kalori, width=15)
        self.input_kalori_hari_ini.grid(row=3, column=1, padx=5, pady=10, sticky='w')
        
        # Tombol hitung kalori
        self.tombol_periksa_kalori = ttk.Button(
            self.bingkai_input_kalori, 
            text="Periksa Asupan Kalori", 
            command=self.periksa_kalori,
            bootstyle=SUCCESS
        )
        self.tombol_periksa_kalori.grid(row=4, column=0, columnspan=2, padx=5, pady=15, sticky='ew')
        
        # ------ BAGIAN DIAGRAM KALORI ------
        self.bingkai_diagram_kalori = ttk.Labelframe(
            self.bingkai_kalori, 
            text="Visualisasi Asupan Kalori Mingguan",
            padding=15,
            bootstyle=PRIMARY
        )
        self.bingkai_diagram_kalori.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        # Persiapan diagram batang
        self.gambar_kalori = Figure(figsize=(5, 4), dpi=100)
        self.plot_kalori = self.gambar_kalori.add_subplot(111)
        self.canvas_kalori = FigureCanvasTkAgg(self.gambar_kalori, self.bingkai_diagram_kalori)
        self.canvas_kalori.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # ------ BAGIAN HASIL ANALISIS KALORI ------
        self.bingkai_hasil_kalori = ttk.Labelframe(
            self.bingkai_kalori, 
            text="Hasil Analisis Kalori",
            padding=15,
            bootstyle=SUCCESS
        )
        self.bingkai_hasil_kalori.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Label hasil analisis kalori
        self.label_hasil_kalori = ttk.Label(
            self.bingkai_hasil_kalori, 
            text="Masukkan data untuk melihat analisis kalori", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.label_hasil_kalori.pack(fill=X, pady=5)
        
        self.label_detail_kalori = ttk.Label(
            self.bingkai_hasil_kalori, 
            text="", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.label_detail_kalori.pack(fill=X, pady=5)
        
        # Tampilkan diagram batang awal
        self.perbarui_diagram_batang()
        
    # ------ FUNGSI UNTUK MENGHITUNG MAKRONUTRIEN ------
    def hitung_makro(self):
        """Menghitung dan menampilkan distribusi makronutrien"""
        try:
            # Ambil nilai yang dimasukkan user
            karbo = float(self.input_karbo.get())
            protein = float(self.input_protein.get())
            lemak = float(self.input_lemak.get())
            
            # Konversi ke kalori
            # 1 gram karbohidrat = 4 kalori
            # 1 gram protein = 4 kalori
            # 1 gram lemak = 9 kalori
            kalori_karbo = karbo * 4  
            kalori_protein = protein * 4
            kalori_lemak = lemak * 9
            
            total_kalori = kalori_karbo + kalori_protein + kalori_lemak
            
            # Hitung persentase
            if total_kalori > 0:
                persen_karbo = (kalori_karbo / total_kalori) * 100
                persen_protein = (kalori_protein / total_kalori) * 100
                persen_lemak = (kalori_lemak / total_kalori) * 100
            else:
                persen_karbo = persen_protein = persen_lemak = 0
            
            # Perbarui diagram pie chart
            self.plot_makro.clear()
            nilai = [persen_karbo, persen_protein, persen_lemak]
            label = [f'Karbohidrat\n({persen_karbo:.1f}%)', 
                     f'Protein\n({persen_protein:.1f}%)', 
                     f'Lemak\n({persen_lemak:.1f}%)']
            warna = ['#3498db', '#2ecc71', '#e74c3c']  # Biru, Hijau, Merah
            jarak = (0.05, 0.05, 0.05)
            
            self.plot_makro.pie(nilai, labels=label, autopct='%1.1f%%', 
                             startangle=90, explode=jarak, colors=warna, shadow=True)
            self.plot_makro.set_title('Distribusi Makronutrien')
            self.gambar_makro.tight_layout()
            self.canvas_makro.draw()
            
            # Periksa keseimbangan dengan nilai yang direkomendasikan
            # Rekomendasi: 50% karbo, 20% protein, 30% lemak
            selisih_karbo = abs(persen_karbo - 50)
            selisih_protein = abs(persen_protein - 20)
            selisih_lemak = abs(persen_lemak - 30)
            
            selisih_rata = (selisih_karbo + selisih_protein + selisih_lemak) / 3
            
            # Tentukan status berdasarkan selisih rata-rata
            if selisih_rata <= 5:
                status = "sangat dekat dengan"
                self.label_hasil_makro.configure(bootstyle=SUCCESS)
            elif selisih_rata <= 10:
                status = "mendekati"
                self.label_hasil_makro.configure(bootstyle=INFO)
            elif selisih_rata <= 15:
                status = "sedikit berbeda dari"
                self.label_hasil_makro.configure(bootstyle=WARNING)
            else:
                status = "jauh berbeda dari"
                self.label_hasil_makro.configure(bootstyle=DANGER)
            
            # Format pesan hasil
            pesan = f"Keseimbangan makronutrien Anda {status} asupan yang direkomendasikan."
            rincian = f"Rincian Anda: {persen_karbo:.0f}% Karbohidrat, {persen_protein:.0f}% Protein, {persen_lemak:.0f}% Lemak."
            
            # Perbarui label hasil
            self.label_hasil_makro.config(text=pesan)
            self.label_detail_makro.config(text=rincian)
            
        except ValueError:
            # Jika input bukan angka, tampilkan pesan error
            messagebox.showerror("Error", "Masukkan nilai numerik yang valid.")
    
    # ------ FUNGSI UNTUK MEMBACA DATA KALORI DARI FILE ------
    def baca_data_kalori(self):
        """Membaca data riwayat kalori dari file"""
        # Data default untuk 7 hari terakhir
        hari_ini = datetime.now()
        for i in range(7):
            tanggal = (hari_ini - timedelta(days=i)).strftime("%Y-%m-%d")
            self.data_kalori[tanggal] = 0
        
        # Nilai default jika file tidak ada
        self.kalori_rekomendasi = 0
        self.kalori_minimum = 0
        self.kalori_maksimum = 0
        
        # Coba baca file jika ada
        if os.path.exists(self.nama_file):
            try:
                with open(self.nama_file, 'r') as file:
                    data = json.load(file)
                    
                    # Pastikan data untuk 7 hari terakhir ada
                    for i in range(7):
                        tanggal = (hari_ini - timedelta(days=i)).strftime("%Y-%m-%d")
                        if tanggal not in data:
                            data[tanggal] = 0
                    
                    # Hanya simpan data 7 hari terakhir
                    tanggal_untuk_disimpan = [(hari_ini - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
                    self.data_kalori = {k: data[k] for k in tanggal_untuk_disimpan if k in data}
                    
                    # Baca profil pengguna jika ada
                    if 'user_profile' in data:
                        self.profil_pengguna = data['user_profile']
                    else:
                        self.profil_pengguna = {}
                        
                    # Baca kalori rekomendasi jika ada
                    if 'recommended_calories' in data:
                        self.kalori_rekomendasi = data['recommended_calories']
                        self.kalori_minimum = data['min_calories']
                        self.kalori_maksimum = data['max_calories']
            except Exception as e:
                print(f"Error saat membaca data: {e}")
                self.profil_pengguna = {}
        else:
            self.profil_pengguna = {}
        
    # ------ FUNGSI UNTUK MENYIMPAN DATA KALORI KE FILE ------
    def simpan_data_kalori(self):
        """Menyimpan data riwayat kalori ke file"""
        data = {
            **self.data_kalori,
            'user_profile': self.profil_pengguna,
            'recommended_calories': self.kalori_rekomendasi,
            'min_calories': self.kalori_minimum,
            'max_calories': self.kalori_maksimum
        }
        try:
            with open(self.nama_file, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error saat menyimpan data: {e}")
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}")
    
    # ------ FUNGSI UNTUK MEMERIKSA ASUPAN KALORI HARIAN ------
    def periksa_kalori(self):
        """Memeriksa asupan kalori harian"""
        try:
            # Ambil nilai yang dimasukkan user
            usia = int(self.input_usia.get())
            jenis_kelamin = self.pilihan_kelamin.get()
            aktivitas = self.pilihan_aktivitas.get().lower()
            kalori_hari_ini = float(self.input_kalori_hari_ini.get())
            
            # Nilai berat dan tinggi default berdasarkan jenis kelamin
            if jenis_kelamin.lower() == 'laki-laki':
                berat = 70  # kg
                tinggi = 170  # cm
            else:  # wanita
                berat = 60  # kg
                tinggi = 160  # cm
            
            # Simpan ke profil pengguna
            self.profil_pengguna = {
                'age': usia,
                'gender': jenis_kelamin,
                'activity': aktivitas
            }
            
            # Hitung BMR menggunakan rumus Mifflin-St Jeor
            if jenis_kelamin.lower() == 'laki-laki':
                bmr = 10 * berat + 6.25 * tinggi - 5 * usia + 5
            else:  # wanita
                bmr = 10 * berat + 6.25 * tinggi - 5 * usia - 161
            
            # Faktor pengali berdasarkan tingkat aktivitas
            faktor_aktivitas = {
                'sedentary': 1.2,  # Sangat jarang olahraga
                'ringan': 1.375,   # Olahraga ringan 1-3 hari/minggu
                'sedang': 1.55,    # Olahraga sedang 3-5 hari/minggu
                'aktif': 1.725,    # Olahraga berat 6-7 hari/minggu
            }
            
            # Hitung kalori harian yang direkomendasikan
            kalori_rekomendasi = bmr * faktor_aktivitas.get(aktivitas, 1.2)
            
            # Perbarui nilai kalori rekomendasi
            self.kalori_rekomendasi = kalori_rekomendasi
            
            # Set rentang (±10% dari rekomendasi)
            self.kalori_minimum = math.ceil(kalori_rekomendasi * 0.97 / 100) * 100
            self.kalori_maksimum = math.ceil(kalori_rekomendasi * 1.05 / 100) * 100
            
            # Simpan kalori hari ini
            hari_ini = datetime.now().strftime("%Y-%m-%d")
            self.data_kalori[hari_ini] = kalori_hari_ini
            
            # Simpan data ke file
            self.simpan_data_kalori()
            
            # Perbarui diagram batang
            self.perbarui_diagram_batang()
            
            # Tentukan pesan status berdasarkan asupan kalori
            if kalori_hari_ini < self.kalori_minimum:
                if self.kalori_minimum - kalori_hari_ini <= 200:
                    status = f"sedikit rendah (kurang dari rentang yang direkomendasikan {self.kalori_minimum:.0f}-{self.kalori_maksimum:.0f} kkal)"
                    self.label_hasil_kalori.configure(bootstyle=WARNING)
                else:
                    status = f"rendah (kurang dari rentang yang direkomendasikan {self.kalori_minimum:.0f}-{self.kalori_maksimum:.0f} kkal)"
                    self.label_hasil_kalori.configure(bootstyle=DANGER)
            elif kalori_hari_ini > self.kalori_maksimum:
                if kalori_hari_ini - self.kalori_maksimum <= 200:
                    status = f"sedikit di atas rentang yang direkomendasikan ({self.kalori_minimum:.0f}-{self.kalori_maksimum:.0f} kkal untuk profil Anda)"
                    self.label_hasil_kalori.configure(bootstyle=WARNING)
                else:
                    status = f"di atas rentang yang direkomendasikan ({self.kalori_minimum:.0f}-{self.kalori_maksimum:.0f} kkal untuk profil Anda)"
                    self.label_hasil_kalori.configure(bootstyle=DANGER)
            else:
                status = f"dalam rentang yang direkomendasikan ({self.kalori_minimum:.0f}-{self.kalori_maksimum:.0f} kkal untuk profil Anda)"
                self.label_hasil_kalori.configure(bootstyle=SUCCESS)
            
            # Perbarui label hasil
            pesan = f"Asupan kalori Anda {status}."
            self.label_hasil_kalori.config(text=pesan)
            
        except ValueError:
            # Jika input bukan angka, tampilkan pesan error
            messagebox.showerror("Error", "Masukkan nilai numerik yang valid.")
    
    # ------ FUNGSI UNTUK MEMPERBARUI DIAGRAM BATANG ------
    def perbarui_diagram_batang(self):
        """Memperbarui diagram batang dengan data kalori terbaru"""
        self.plot_kalori.clear()
        
        # Dapatkan 7 hari terakhir sebagai nama hari dengan tanggal
        hari_ini = datetime.now()
        tanggal = [(hari_ini - timedelta(days=i)) for i in range(6, -1, -1)]
        label_x = [d.strftime("%d/%m") for d in tanggal]
        kunci_tanggal = [d.strftime("%Y-%m-%d") for d in tanggal]
        
        # Dapatkan nilai kalori
        kalori = [self.data_kalori.get(tanggal, 0) for tanggal in kunci_tanggal]
        
        # Buat diagram batang
        x = np.arange(len(label_x))
        batang = self.plot_kalori.bar(x, kalori, width=0.6)
        
        # Warnai batang berdasarkan rentang kalori
        for i, batang in enumerate(batang):
            kal = kalori[i]
            if kal == 0:
                batang.set_color('#cccccc')  # Abu-abu untuk data kosong
            elif kal < self.kalori_minimum and self.kalori_minimum > 0:
                batang.set_color('#ff9f1a')  # Oranye untuk kalori rendah
            elif kal > self.kalori_maksimum and self.kalori_maksimum > 0:
                batang.set_color('#e74c3c')  # Merah untuk kalori tinggi
            else:
                batang.set_color('#2ecc71')  # Hijau untuk kalori baik
                
            # Tambahkan label nilai di atas batang
            tinggi = batang.get_height()
            if tinggi > 0:
                self.plot_kalori.text(batang.get_x() + batang.get_width()/2., tinggi + 50,
                                    f"{tinggi:.0f}", ha='center', va='bottom')
        
        # Atur batas sumbu y
        kalori_tertinggi = max(max(kalori) if kalori else 0, self.kalori_maksimum * 1.2) 
        if kalori_tertinggi <= 0:
            kalori_tertinggi = 3000  # Nilai default jika tidak ada data
        self.plot_kalori.set_ylim(0, kalori_tertinggi * 1.2)
        
        # Tambahkan garis rentang rekomendasi
        if self.kalori_rekomendasi > 0:
            self.plot_kalori.axhline(y=self.kalori_rekomendasi, color='green', linestyle='-', linewidth=2, label=f'Rekomendasi: {self.kalori_rekomendasi:.0f} kkal')
            self.plot_kalori.axhline(y=self.kalori_minimum, color='orange', linestyle='--', linewidth=1, label=f'Min: {self.kalori_minimum:.0f} kkal')  
            self.plot_kalori.axhline(y=self.kalori_maksimum, color='red', linestyle='--', linewidth=1, label=f'Max: {self.kalori_maksimum:.0f} kkal')
            
            # Tambahkan area berwarna untuk rentang yang direkomendasikan
            self.plot_kalori.axhspan(self.kalori_minimum, self.kalori_maksimum, alpha=0.1, color='green')
        
        # Atur label sumbu x
        self.plot_kalori.set_xticks(x)
        self.plot_kalori.set_xticklabels(label_x, rotation=45)
        
        # Tambahkan label dan judul
        self.plot_kalori.set_xlabel("Tanggal")
        self.plot_kalori.set_ylabel("Kalori")
        self.plot_kalori.set_title('Asupan Kalori 7 Hari Terakhir')
        
        # Tambahkan legenda jika ada rekomendasi kalori
        if self.kalori_rekomendasi > 0:
            self.plot_kalori.legend(loc='upper right', fontsize='small')
        
        # Perbarui tampilan
        self.gambar_kalori.tight_layout()
        self.canvas_kalori.draw()
    
    # ------ FUNGSI SAAT MENUTUP APLIKASI ------
    def saat_ditutup(self):
        # Simpan data sebelum menutup aplikasi
        self.simpan_data_kalori()
        self.window.destroy()

# ------ PROGRAM UTAMA ------
if __name__ == "__main__":
    # Buat window aplikasi dengan tema 'vapor'
    window = ttk.Window(themename="vapor")
    
    # Jalankan aplikasi
    app = AplikasiNutrisi(window)
    
    # Atur fungsi yang akan dijalankan saat menutup aplikasi
    window.protocol("WM_DELETE_WINDOW", app.saat_ditutup)
    
    # Jalankan loop utama aplikasi
    window.mainloop()