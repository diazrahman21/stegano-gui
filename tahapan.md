# Tahapan Pengujian Aplikasi Analisis Keamanan Steganografi DCT vs IWT

## 1. Pendahuluan

Tahapan pengujian dilakukan dengan menggunakan sampel citra digital yang mewakili masing-masing resolusi, ekstensi file, dan kanal warna untuk membandingkan kinerja algoritma **DCT (Discrete Cosine Transform)** dan **IWT (Integer Wavelet Transform)**. 

Pengujian ini bertujuan untuk mengevaluasi:
- **Kualitas visual** citra yang disisipi watermark
- **Keamanan steganografi** terhadap detektor analisis diferensial
- **Performa ekstraksi** pesan/watermark dari citra stego

---

## 2. Sampel Citra Digital yang Digunakan

Program menggunakan citra digital dengan spesifikasi berikut:

| No | Nama Citra | Resolusi | Kanal Warna | Format | Deskripsi |
|:--:|:-----------|:--------:|:-----------:|:------:|-----------|
| 1 | Clock | 512×512 | Grayscale | PNG/JPG | Citra jam dengan kontras tinggi |
| 2 | House | 512×512 | RGB | PNG/JPG | Citra bangunan dengan detail tekstur |
| 3 | Couple | 512×512 | Grayscale | PNG/JPG | Citra dua orang dengan gradasi halus |
| 4 | Peppers | 512×512 | RGB | PNG/JPG | Citra lada dengan warna-warna cerah |

Catatan: Program secara otomatis mengkonversi semua citra RGB ke **grayscale** untuk memastikan konsistensi pengujian, dan melakukan **resize** ke ukuran target 512×512 piksel.

---

## 3. Parameter Penelitian

Parameter yang digunakan dalam pengujian telah ditetapkan sebagai berikut:

| Parameter | Nilai | Keterangan |
|-----------|-------|-----------|
| **Ukuran Citra Target** | 512×512 px | Standar untuk semua citra input |
| **Ukuran Watermark** | 64×64 bit | Kapasitas embedding: 4096 bit |
| **Alpha DCT** | 10.0 | Faktor skalasi koefisien DCT |
| **Alpha IWT** | 2.0 | Faktor skalasi koefisien wavelet HH |
| **Wavelet** | Haar | Basis wavelet untuk IWT |

---

## 4. Antarmuka Aplikasi

Aplikasi berbasis **Streamlit** menyediakan interface yang user-friendly dengan fitur-fitur berikut:

### 4.1 Halaman Beranda (Home)
- Pengenalan aplikasi dan metode
- Penjelasan metrik evaluasi
- Panduan penggunaan (quick start guide)

### 4.2 Halaman Batch Processing
Untuk pengujian banyak citra sekaligus:

1. **Upload Gambar**
   - Upload multiple files (PNG/JPG/JPEG)
   - Tampilan jumlah file yang diupload

2. **Input Pesan/Watermark**
   - Mode Watermark Acak: berbeda untuk setiap gambar
   - Mode TXT: sama untuk semua gambar
   - Validasi kapasitas

3. **Tabel Detail Hasil**
   - Menampilkan metrik per citra dan metode
   - Format: nama file | metrik per method

4. **Tabel Per Gambar (DCT vs IWT)**
   - Pivoting untuk perbandingan langsung DCT vs IWT
   - Struktur: setiap baris = 1 gambar, kolom = metrik untuk setiap method

5. **Tabel Ringkasan**
   - Rata-rata dan standar deviasi per method
   - Membantu identifikasi metode terbaik secara keseluruhan

6. **Grafik Perbandingan**
   - 6 subgraf: MSE, PSNR, SSIM, NPCR, UACI, ringkasan
   - Perbandingan rata-rata per method

7. **Preview Citra**
   - Menampilkan maksimal 6 gambar pertama
   - Layout 3 kolom: Cover | Stego DCT | Stego IWT

8. **Hasil Ekstraksi Pesan**
   - Tabel akurasi ekstraksi per gambar
   - Detail per gambar (expandable) untuk mode TXT

9. **Kesimpulan Analisis**
   - Berbasis rata-rata metrik dari semua citra

10. **Download Hasil**
    - Detail CSV (semua data per citra)
    - Ringkasan CSV (statistik per method)
    - Grafik (PNG)
    - ZIP Stego DCT
    - ZIP Stego IWT
    - ZIP Stego (DCT+IWT)

---

## 5. Metrik Evaluasi Kinerja

### 5.1 Metrik Kualitas Kualitatif

Membandingkan kualitas visual antara citra asli, terenkripsi, dan terekstrak:

| Metrik | Singkatan | Range | Interpretasi | Rumus |
|--------|-----------|-------|--------------|-------|
| Mean Squared Error | **MSE** | 0 - ∞ | Semakin kecil ✓ | $\frac{1}{N}\sum_{i=1}^{N}(I_i - I'_i)^2$ |
| Peak Signal-to-Noise Ratio | **PSNR** | dB | Semakin besar ✓ | $10\log_{10}\left(\frac{MAX^2}{MSE}\right)$ |
| Structural Similarity Index | **SSIM** | 0-1 | Semakin besar ✓ | Kesamaan struktur piksel |

**Kategori Perbandingan:**
- Original vs Encrypted (Stego DCT / Stego IWT)
- Original vs Decrypted (Extracted Watermark)
- Encrypted vs Decrypted

### 5.2 Metrik Analisis Diferensial (Keamanan)

Mengukur ketahanan terhadap serangan analisis diferensial dengan mengubah 1 piksel pada citra asli:

| Metrik | Singkatan | Range | Interpretasi | Rumus |
|--------|-----------|-------|--------------|-------|
| Number of Pixel Change Rate | **NPCR** | 0-100% | Semakin besar ✓ | $\frac{\sum_{i,j}D(i,j)}{M \times N} \times 100$ |
| Unified Average Changed Intensity | **UACI** | 0-100% | Semakin besar ✓ | $\frac{1}{M \times N}\sum_{i,j}\frac{\|C_1(i,j)-C_2(i,j)\|}{255} \times 100$ |

Di mana:
- $D(i,j)$ = 0 jika $C_1(i,j) = C_2(i,j)$, dan 1 sebaliknya
- $C_1$ = citra enkripsi dari citra asli
- $C_2$ = citra enkripsi dari citra asli dengan 1 piksel diubah

**Interpretasi:**
- NPCR tinggi (ideally > 90%) → Tingkat perubahan piksel tinggi
- UACI tinggi (ideally > 33%) → Perubahan intensitas signifikan

### 5.3 Metrik Performa Ekstraksi

Mengukur akurasi ekstraksi watermark/pesan dari stego images:

| Metrik | Interpretasi |
|--------|--------------|
| **Extraction Accuracy DCT** | Persentase bit yang berhasil diekstrak dengan benar dari Stego DCT |
| **Extraction Accuracy IWT** | Persentase bit yang berhasil diekstrak dengan benar dari Stego IWT |

---

## 6. Prosedur Pengujian

### 6.1 Pengujian Batch Processing

1. **Setup**
   - Launch aplikasi: `streamlit run app.py`
   - Navigasi ke halaman "Batch Processing"

2. **Input Data**
   - Upload semua citra sampel (4 citra minimum)
   - Pilih mode watermark yang sama untuk semua

3. **Eksekusi**
   - Klik "🚀 Mulai Proses Batch"
   - Program melakukan:
     - Iterasi processing untuk setiap citra
     - Embedding DCT dan IWT untuk setiap citra
     - Ekstraksi dan perhitungan metrik

4. **Analisis Hasil**
   - Tabel ringkasan: rata-rata metrik per method
   - Grafik perbandingan 6 chart
   - Kesimpulan berbasis rata-rata semua citra
   - Preview citra (terbatas 6 citra pertama)

5. **Dokumentasi**
   - Download: Detail CSV, Ringkasan CSV, Grafik, ZIP stego images
   - Bandingkan performa antar citra
   - Analisis konsistensi metrik

---

## 7. Alur Workflow Lengkap

```
┌─────────────────────────────────────────────────────────────┐
│  TAHAPAN PENGUJIAN STEGANOGRAFI CITRA DCT vs IWT           │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌───────▼─────────┐
                    │  Input Citra    │
                    │  - Upload file  │
                    │  - Preprocess   │
                    └───────┬─────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
    ┌───────▼──────────┐        ┌──────────▼──────────┐
    │  Embedding DCT   │        │  Embedding IWT      │
    │  - Transformasi  │        │  - Transformasi     │
    │  - Modifikasi    │        │  - Modifikasi HH    │
    │  - Rekontruksi   │        │  - Rekontruksi      │
    └───────┬──────────┘        └──────────┬──────────┘
            │                               │
    ┌───────▼──────────┐        ┌──────────▼──────────┐
    │  Extract DCT     │        │  Extract IWT        │
    │  - Baca DCT      │        │  - Baca HH          │
    │  - Bandingkan    │        │  - Bandingkan       │
    │  - Ekstrak bit   │        │  - Ekstrak bit      │
    └───────┬──────────┘        └──────────┬──────────┘
            │                               │
            └───────────────┬───────────────┘
                            │
                    ┌───────▼─────────┐
                    │  Evaluasi Metrik│
                    │  - MSE, PSNR    │
                    │  - SSIM         │
                    │  - NPCR, UACI   │
                    │  - Akurasi      │
                    └───────┬─────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
    ┌───────▼──────────┐        ┌──────────▼──────────┐
    │  Visualisasi     │        │  Download Hasil     │
    │  - Histogram     │        │  - CSV              │
    │  - Grafik metrik │        │  - PNG              │
    │  - Kesimpulan    │        │  - ZIP              │
    └──────────────────┘        └─────────────────────┘
```

---

## 8. Contoh Skenario Pengujian

### Skenario 1: Pengujian DCT vs IWT dengan Citra Standar
1. Upload Clock (512×512 Grayscale)
2. Gunakan watermark acak
3. Bandingkan MSE, PSNR, SSIM antara DCT dan IWT
4. Catat metrik terbaik

### Skenario 2: Pengujian Ekstraksi Pesan
1. Upload gambar dengan pesan TXT
2. Pesan: "STEGANOGRAFI AMAN"
3. Monitor akurasi ekstraksi DCT vs IWT
4. Verifikasi pesan yang terekstrak

### Skenario 3: Pengujian Keamanan Diferensial
1. Batch processing dengan 4 citra
2. Bandingkan NPCR dan UACI antar metode
3. Identifikasi metode dengan perubahan tertinggi
4. Analisis konsistensi hasil

### Skenario 4: Pengujian Performa Keseluruhan
1. Batch 4 citra berbeda resolusi dan kanal
2. Bandingkan rata-rata semua metrik
3. Buat trade-off analysis kualitas vs keamanan
4. Tentukan metode rekomendasi

---

## 9. Output dan Dokumentasi

### 9.1 Output Digital
Program menghasilkan output berupa:

1. **Citra Stego**
   - Format PNG (8-bit grayscale)
   - Nama: `stego_dct_[timestamp].png`, `stego_iwt_[timestamp].png`

2. **Visualisasi**
   - Histogram citra (PNG)
   - Grafik metrik perbandingan (PNG)
   - Batch metrics chart (PNG)

3. **Data Metrik**
   - Detail CSV: baris per citra+method
   - Ringkasan CSV: rata-rata per method
   - Tabel struktur MultiIndex untuk batch

4. **Bundel Hasil**
   - ZIP DCT: semua stego_dct_*.png
   - ZIP IWT: semua stego_iwt_*.png
   - ZIP Both: DCT + IWT

### 9.2 Interpretasi Hasil
- **MSE kecil + PSNR besar → Kualitas visual bagus**
- **SSIM tinggi → Kesamaan struktur terjaga**
- **NPCR tinggi + UACI tinggi → Keamanan kuat**
- **Trade-off kualitas-keamanan**: catat metode pilihan

---

## 10. Kesimpulan

Aplikasi ini menyediakan framework lengkap untuk:
✅ Membandingkan DCT dan IWT secara empiris  
✅ Mengukur kualitas visual dengan 3 metrik  
✅ Menganalisis keamanan dengan 2 metrik diferensial  
✅ Menguji ekstraksi watermark/pesan  
✅ Mendokumentasikan hasil dalam berbagai format  

Hasil penelitian dapat digunakan untuk **menentukan metode steganografi mana yang lebih optimal** berdasarkan prioritas kualitas atau keamanan.

---

*Dokumentasi ini sesuai dengan Tahapan Pengujian Aplikasi Analisis Keamanan Steganografi DCT vs IWT Berbasis Streamlit*
