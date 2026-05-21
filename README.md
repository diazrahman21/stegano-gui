# 🔐 Analisis Keamanan Steganografi Citra - DCT vs IWT

Aplikasi GUI modern untuk membandingkan dua metode steganografi citra berbasis **DCT (Discrete Cosine Transform)** dan **IWT (Integer Wavelet Transform)** menggunakan framework **Streamlit**.

## 📋 Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Sistem Kebutuhan](#sistem-kebutuhan)
- [Instalasi](#instalasi)
- [Cara Menjalankan](#cara-menjalankan)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Metrik Evaluasi](#metrik-evaluasi)
- [Troubleshooting](#troubleshooting)

## 🎯 Fitur Utama

### 1. **Halaman Utama**
- Judul dan deskripsi aplikasi
- Penjelasan singkat metode DCT dan IWT
- Tabel metrik dan cara penggunaan
- Informasi teknis lengkap

### 2. **Single Image Processing**
- Upload satu gambar (PNG/JPG/JPEG)
- Preprocessing otomatis (grayscale + resize ke 512×512)
- Preview citra asli dengan histogram
- Pilihan watermark:
  - Watermark acak otomatis
  - Upload file TXT untuk pesan rahasia
- Proses embedding DCT dan IWT
- Visualisasi citra hasil penyisipan
- Histogram perbandingan
- Ekstraksi dan rekonstruksi pesan (jika menggunakan TXT)
- Tabel metrik perbandingan
- Grafik visualisasi metrik
- Kesimpulan otomatis
- Download hasil (PNG/CSV)

### 3. **Batch Processing**
- Upload banyak gambar sekaligus
- Proses otomatis untuk semua gambar
- Generate watermark acak per gambar
- Tabel detail hasil semua gambar
- Tabel ringkasan (rata-rata & std dev)
- Grafik perbandingan
- Preview sampel gambar (max 6)
- Download hasil detail dan ringkasan (CSV)

### 4. **Konfigurasi Parameter di Sidebar**
- Ukuran citra target (256-1024 px, default 512)
- Ukuran watermark (32-128 px, default 64)
- Alpha DCT (1.0-50.0, default 10.0)
- Alpha IWT (0.1-10.0, default 2.0)
- Wavelet IWT (haar, db2, db4)

## 💻 Sistem Kebutuhan

- **OS:** Windows, macOS, atau Linux
- **Python:** 3.8 atau lebih tinggi
- **RAM:** Minimal 4 GB (recommended 8 GB untuk batch processing)
- **Storage:** 500 MB untuk instalasi dependencies

## 📦 Instalasi

### Step 1: Clone atau Unduh Proyek
```bash
cd "d:\project saya\Steganografi gui"
```

### Step 2: Buat Virtual Environment (Recommended)
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

> **Catatan:** Proses instalasi dapat memakan waktu 5-10 menit, terutama untuk OpenCV.

## 🚀 Cara Menjalankan

Dari folder proyek, jalankan:

```bash
streamlit run app.py
```

Aplikasi akan membuka di browser secara otomatis pada `http://localhost:8501`

### Jika Browser Tidak Terbuka Otomatis
Buka browser dan akses: `http://localhost:8501`

## 📖 Panduan Penggunaan

### 📸 Single Image Processing

1. **Upload Gambar**
   - Klik area upload atau drag-drop gambar
   - Format: PNG, JPG, JPEG
   - Gambar akan otomatis dikonversi ke grayscale dan resize ke 512×512

2. **Pilih Watermark**
   - **Watermark Acak:** Gunakan watermark random 64×64 (recommended)
   - **Upload TXT:** Masukkan pesan rahasia dari file teks
     - Maksimal: 512 bit ÷ 8 = 64 karakter
     - Jika melebihi, akan ditampilkan error

3. **Konfigurasi Parameter (Sidebar)**
   - Sesuaikan alpha DCT dan IWT sesuai kebutuhan
   - Ubah ukuran citra jika diperlukan

4. **Mulai Proses**
   - Klik tombol **"🚀 Mulai Proses Steganografi"**
   - Tunggu proses embedding dan evaluasi selesai

5. **Lihat Hasil**
   - Citra hasil penyisipan (DCT & IWT)
   - Histogram perbandingan
   - Tabel metrik
   - Grafik visualisasi
   - Kesimpulan analisis
   - Ekstraksi pesan (jika menggunakan TXT)

6. **Download**
   - Stego DCT (PNG)
   - Stego IWT (PNG)
   - Histogram (PNG)
   - Grafik Metrik (PNG)
   - Hasil CSV

### 🎞️ Batch Processing

1. **Upload Gambar Multiple**
   - Upload 2 atau lebih gambar sekaligus
   - Format: PNG, JPG, JPEG

2. **Mulai Proses Batch**
   - Klik tombol **"🚀 Mulai Proses Batch"**
   - Proses otomatis untuk semua gambar

3. **Lihat Hasil**
   - Tabel detail (filename, method, metrik)
   - Tabel ringkasan (mean & std dev per method)
   - Grafik perbandingan
   - Preview sampel gambar

4. **Download**
   - Detail CSV
   - Ringkasan CSV
   - Grafik (PNG)

## 📊 Metrik Evaluasi

### Metrik Kualitas (Scikit-Image)

| Metrik | Rumus | Interpretasi | Rentang |
|--------|-------|--------------|---------|
| **MSE** | $\frac{1}{N}\sum(I-I')^2$ | Semakin kecil ✓ | 0 - ∞ |
| **PSNR** | $10\log_{10}(\frac{MAX^2}{MSE})$ | Semakin besar ✓ | 0 - ∞ dB |
| **SSIM** | Kesamaan struktur | Semakin besar ✓ | 0 - 1 |

### Metrik Keamanan (NumPy)

| Metrik | Deskripsi | Interpretasi | Rentang |
|--------|-----------|--------------|---------|
| **NPCR** | Number of Pixel Change Rate | Semakin besar ✓ | 0 - 100% |
| **UACI** | Unified Average Changed Intensity | Semakin besar ✓ | 0 - 100% |

## 🏗️ Struktur Proyek

```
Steganografi gui/
├── app.py                      # Aplikasi Streamlit utama
├── requirements.txt            # Dependencies
├── README.md                   # Dokumentasi ini
└── (hasil eksekusi otomatis disimpan di temp)
```

### File-File Penting dalam app.py

```python
# Preprocessing & Konversi
- preprocess_image()           # Grayscale + resize
- text_to_binary()            # Konversi teks ke biner
- binary_to_text()            # Konversi biner ke teks

# Embedding & Ekstraksi
- embed_dct()                 # Penyisipan DCT
- embed_iwt_hh()              # Penyisipan IWT pada subband HH
- extract_dct()               # Ekstraksi dari DCT
- extract_iwt()               # Ekstraksi dari IWT

# Metrik & Evaluasi
- compute_npcr()              # Hitung NPCR
- compute_uaci()              # Hitung UACI
- evaluate_all()              # Hitung semua metrik

# Visualisasi
- plot_images_and_histograms() # Visualisasi citra & histogram
- plot_metrics_comparison()    # Grafik perbandingan metrik
- plot_batch_metrics()         # Grafik batch metrics

# Kesimpulan
- generate_conclusion()        # Generate kesimpulan otomatis
```

## 🔍 Penjelasan Metode

### DCT (Discrete Cosine Transform)

**Karakteristik:**
- Transformasi frekuensi berbasis blok 8×8
- Memanfaatkan dua koefisien: posisi (3,4) dan (4,3)
- Aturan embedding: bit 1 → c1 > c2, bit 0 → c2 > c1

**Kelebihan:**
- Mudah diimplementasikan
- Kualitas visual baik untuk alpha optimal
- Cepat dan efisien

**Kekurangan:**
- Rentan terhadap perubahan amplitudo

### IWT (Integer Wavelet Transform)

**Karakteristik:**
- Transformasi wavelet berbasis dekomposisi 1-level
- Memodifikasi subband HH dengan scaling alpha
- Menggunakan wavelet Haar (atau db2, db4)

**Kelebihan:**
- Operasi integer (tidak ada loss dalam quantization)
- Cocok untuk frekuensi tinggi
- Lebih robust untuk keamanan

**Kekurangan:**
- Sedikit lebih kompleks
- Kecepatan lebih lambat dari DCT

## 💡 Tips Penggunaan Optimal

1. **Untuk Hasil Terbaik:**
   - Gunakan gambar natural (foto) minimal 512×512 px
   - Coba berbagai nilai alpha untuk menemukan trade-off optimal
   - Alpha DCT 10-15 biasanya bagus untuk kualitas
   - Alpha IWT 2-3 untuk keamanan baik

2. **Batch Processing:**
   - Gunakan untuk membandingkan banyak gambar secara sistematis
   - Hasilnya tersimpan dalam CSV untuk analisis lanjutan
   - Preview maksimal 6 gambar untuk kinerja UI optimal

3. **Interpretasi Hasil:**
   - Jika PSNR > 40 dB: kualitas sangat baik
   - Jika PSNR 30-40 dB: kualitas baik
   - Jika NPCR > 50%: perubahan piksel signifikan (keamanan baik)
   - SSIM > 0.95: kemiripan visual sangat tinggi

4. **Download & Dokumentasi:**
   - Download hasil PNG untuk visualisasi
   - Download CSV untuk analisis statistik lebih lanjut
   - Gunakan untuk laporan skripsi

## ⚙️ Troubleshooting

### 1. **Error: "AttributeError: module 'pywt' has no attribute 'dwt2'"**
```bash
pip install --upgrade PyWavelets
```

### 2. **Error: "ModuleNotFoundError: No module named 'cv2'"**
```bash
pip install opencv-python
```

### 3. **Error: "Image file not recognized"**
- Pastikan format gambar adalah PNG/JPG/JPEG
- Cek ukuran file tidak terlalu besar (> 50 MB)
- Coba gambar lain untuk verifikasi

### 4. **Aplikasi Lambat / Crash pada Batch Processing**
- Reduce ukuran citra target (dari 512 ke 256)
- Process lebih sedikit gambar sekaligus
- Pastikan RAM cukup (free at least 2 GB)

### 5. **Browser Tidak Terbuka Otomatis**
```bash
# Manual access
# Buka browser dan kunjungi: http://localhost:8501
```

### 6. **Port 8501 Sudah Digunakan**
```bash
streamlit run app.py --server.port 8502
```

## 📝 Catatan Penting

✅ **Program ini:**
- ✓ Tidak bergantung pada Google Colab
- ✓ Dapat dijalankan fully lokal
- ✓ Semua file hasil dapat diunduh
- ✓ Mendukung GUI modern & responsif dengan Streamlit
- ✓ Cocok untuk demo & presentasi skripsi

❌ **Limitasi:**
- Batch processing best untuk max 20-50 gambar (tergantung spesifikasi PC)
- Pesan TXT max 64 karakter (kapasitas watermark 64×64 bit)
- Gambar terbaik ukuran 512×512 atau kelipatan 8

## 📞 Support & Kontribusi

Jika ada error atau saran perbaikan:
1. Cek troubleshooting section di atas
2. Verifikasi Python version (3.8+)
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 📄 Lisensi

Dibuat untuk keperluan skripsi akademik. Penggunaan bebas untuk tujuan non-komersial.

---

**Dibuat dengan ❤️ untuk analisis steganografi citra**

**Last Updated:** Januari 2025
