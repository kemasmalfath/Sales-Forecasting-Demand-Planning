# 📈 Sales Forecasting & Demand Planning

> **Time-Series Forecasting** untuk memprediksi penjualan ritel 30 hari ke depan menggunakan **Holt-Winters Exponential Smoothing**, divisualisasikan dalam dashboard web interaktif berbasis **Flask & Plotly**.

---

## 🧠 Apa Itu Proyek Ini?

Bayangkan Anda adalah **manajer sebuah toko ritel**. Setiap hari, Anda mencatat berapa banyak barang yang terjual. Setelah 2 tahun, Anda memiliki **730 hari data penjualan**.

Pertanyaannya: *"Bisakah saya menebak berapa penjualan bulan depan berdasarkan data 2 tahun ini?"*

**Jawabannya: Bisa!** Dan itulah yang dilakukan proyek ini.

Proyek ini menggunakan teknik **Machine Learning / Statistik** untuk:
1. **Membaca pola tersembunyi** di dalam data penjualan (misalnya: hari Sabtu selalu ramai, bulan Desember selalu naik).
2. **Memprediksi masa depan** — memproyeksikan estimasi penjualan untuk 30 hari ke depan.
3. **Memberikan rekomendasi bisnis** — saran konkret seperti "tambah stok di hari Sabtu" atau "siapkan promosi di bulan sepi".

---

## 🔬 Konsep Data Science yang Digunakan

### 1. Time-Series Analysis (Analisis Runtun Waktu)
Data penjualan harian adalah contoh klasik dari **time-series** — yaitu data yang berurutan berdasarkan waktu. Berbeda dengan data biasa, urutan waktu sangat penting di sini karena penjualan hari ini dipengaruhi oleh penjualan kemarin.

### 2. Holt-Winters Exponential Smoothing
Ini adalah algoritma utama yang digunakan. Algoritma ini bekerja dengan memecah data menjadi **3 komponen**:

| Komponen | Penjelasan | Contoh |
|---|---|---|
| **Level** | Nilai dasar rata-rata penjualan | "Rata-rata toko ini menjual 120 unit/hari" |
| **Trend** | Apakah penjualan cenderung naik atau turun seiring waktu? | "Setiap bulan, penjualan naik sekitar 2%" |
| **Seasonality** | Pola berulang yang terjadi secara periodik | "Setiap hari Sabtu, penjualan naik 20%" |

Dengan memahami ketiga komponen ini, model dapat **meramalkan masa depan** dengan cukup akurat.

### 3. Train/Test Split (Validasi Model)
Untuk membuktikan bahwa model benar-benar "pintar" (bukan sekadar menghafal), data dibagi menjadi:
- **Data Latih (700 hari):** Digunakan untuk mengajari model mengenali pola.
- **Data Uji (30 hari):** Data yang *tidak pernah dilihat* oleh model, digunakan untuk mengukur seberapa akurat prediksinya.

### 4. Metrik Evaluasi Model

| Metrik | Nama Lengkap | Arti Sederhana |
|---|---|---|
| **MAE** | Mean Absolute Error | "Rata-rata, prediksi saya meleset sekitar X unit dari kenyataan" |
| **RMSE** | Root Mean Squared Error | "Sama seperti MAE, tapi lebih sensitif terhadap kesalahan besar" |
| **MAPE** | Mean Absolute Percentage Error | "Rata-rata, prediksi saya meleset sekitar X% dari kenyataan" |

> 💡 **Semakin kecil nilainya, semakin akurat modelnya.**

### 5. Seasonal Decomposition (Dekomposisi Musiman)
Proyek ini menganalisis **pola mingguan** (hari apa yang paling ramai?) dan **pola bulanan** (bulan apa yang paling laku?) untuk memberikan insight bisnis yang actionable.

---

## ✨ Fitur Dashboard

| Fitur | Deskripsi |
|---|---|
| **4 KPI Cards** | Total penjualan historis, prediksi 30 hari, tren naik/turun, dan akurasi model |
| **Grafik Utama Interaktif** | Penjualan aktual 90 hari terakhir + garis prediksi 30 hari ke depan (bisa di-zoom) |
| **Grafik Pola Mingguan** | Bar chart rata-rata penjualan per hari dalam seminggu |
| **Grafik Tren Bulanan** | Line chart penjualan total per bulan selama 12 bulan terakhir |
| **Evaluasi Model** | Metrik MAE, RMSE, MAPE untuk membuktikan akurasi model |
| **4 Insight Bisnis** | Rekomendasi berbasis data: analisis tren, puncak penjualan, saran stok, dan performa musiman |

---

## 🛠️ Tech Stack

| Kategori | Teknologi |
|---|---|
| **Backend** | Python, Flask |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Statsmodels (Holt-Winters Exponential Smoothing) |
| **Model Evaluation** | Scikit-Learn (MAE, RMSE) |
| **Data Visualization** | Plotly.js |
| **Frontend** | HTML5, CSS3, JavaScript |

---

## 📁 Struktur Proyek

```
Sales_Forecasting_Project/
│
├── app.py                  # Server Flask + logika forecasting
├── generate_data.py        # Generator data sintetis 2 tahun
├── requirements.txt        # Daftar library Python
├── README.md               # Dokumentasi proyek (file ini)
│
├── data/
│   └── sales_data.csv      # Dataset penjualan harian (730 hari)
│
├── static/
│   └── style.css           # Styling dashboard (minimalist, light mode)
│
└── templates/
    └── index.html           # Antarmuka dashboard + Plotly charts
```

---

## 🚀 Cara Menjalankan

### Prasyarat
- Python 3.10 atau lebih baru
- pip (Python package manager)

### Langkah-Langkah

```bash
# 1. Clone repositori
git clone https://github.com/kemasmalfath/Sales_Forecasting_Project.git
cd Sales_Forecasting_Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate data dummy (730 hari penjualan sintetis)
python generate_data.py

# 4. Jalankan aplikasi Flask
python app.py
```

Buka browser dan kunjungi: **http://127.0.0.1:5000**

---

## 📊 Alur Kerja Data Science

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  DATA COLLECTION │────▶│  PREPROCESSING   │────▶│  MODEL TRAINING     │
│  (730 hari CSV)  │     │  (Pandas, NumPy) │     │  (Holt-Winters)     │
└─────────────────┘     └──────────────────┘     └──────────┬──────────┘
                                                            │
                                                            ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   DEPLOYMENT    │◀────│  VISUALIZATION   │◀────│  MODEL EVALUATION   │
│   (Flask Web)   │     │  (Plotly.js)     │     │  (MAE, RMSE, MAPE)  │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
```

1. **Data Collection** — Membaca file CSV berisi riwayat penjualan harian selama 2 tahun.
2. **Preprocessing** — Membersihkan data, mengonversi tipe tanggal, mengurutkan secara kronologis.
3. **Model Training** — Melatih algoritma Holt-Winters pada 700 hari data latih.
4. **Model Evaluation** — Menguji akurasi model pada 30 hari data uji menggunakan MAE, RMSE, MAPE.
5. **Visualization** — Menampilkan hasil dalam 3 grafik interaktif Plotly.
6. **Deployment** — Menyajikan dashboard melalui server web Flask.

---

## 📖 Apa yang Saya Pelajari dari Proyek Ini

- Cara menerapkan **Time-Series Forecasting** pada kasus bisnis nyata.
- Perbedaan antara **ARIMA**, **Exponential Smoothing**, dan **Prophet** (dan kapan menggunakan masing-masing).
- Pentingnya **Train/Test Split** untuk memvalidasi model (bukan hanya melatih tanpa evaluasi).
- Cara menghitung dan menginterpretasikan **MAE, RMSE, MAPE** sebagai ukuran kualitas model.
- Cara menyajikan hasil analisis data dalam bentuk **dashboard web interaktif** yang mudah dipahami oleh non-teknikal (stakeholder bisnis).
- Integrasi end-to-end: dari **data mentah → model → visualisasi → web app**.

---

## 👤 Author

**Kemas Muhammad Alfath Iskandar**
- GitHub: [@kemasmalfath](https://github.com/kemasmalfath)
- LinkedIn: [Kemas Alfath](https://linkedin.com/in/alfath-iskandar-578115323/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
