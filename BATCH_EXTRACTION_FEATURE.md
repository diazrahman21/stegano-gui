# 🔐 Fitur Ekstraksi Batch Processing

## Deskripsi
Setelah Anda mulai batch processing, hasil ekstraksi pesan sekarang akan ditampilkan terlebih dahulu untuk memverifikasi bahwa isi pesan sudah terekstrak dengan baik dari setiap gambar.

## Perubahan yang Dilakukan

### 1. Fungsi `process_batch_images()`
Fungsi sekarang melakukan:
- ✅ Embedding watermark ke gambar (DCT + IWT)
- ✅ **BARU**: Ekstraksi watermark dari gambar stego
- ✅ **BARU**: Hitung akurasi ekstraksi (% kesamaan bit dengan watermark asli)
- ✅ **BARU**: Konversi hasil ekstraksi ke teks (jika mode pesan text)
- ✅ Hitung metrik kualitas & keamanan

**Return Value:**
```python
(batch_rows, batch_preview, extraction_results)
```

### 2. Tampilan Hasil Ekstraksi (Section Baru)

#### Mode: Pesan Text
Ketika Anda upload file TXT dengan pesan:

```
🔐 Hasil Ekstraksi Pesan
┌─────────────────────────────────────────┐
│ Gambar          │ Akurasi DCT  │ Akurasi IWT │
├─────────────────────────────────────────┤
│ photo1.jpg      │ 100.00%      │ 95.50%      │
│ photo2.jpg      │ 99.80%       │ 98.20%      │
└─────────────────────────────────────────┘

#### Detail Ekstraksi Per Gambar
📄 photo1.jpg - Akurasi DCT: 100.0%, IWT: 95.5%
  - Ekstraksi DCT: "Ini adalah pesan rahasia yang dikirim"
  - Ekstraksi IWT: "Ini adalah pesan rahasia yang dikirim"
  - Akurasi: 100.00%
```

#### Mode: Watermark Acak
Ketika menggunakan watermark acak:

```
🔐 Hasil Ekstraksi (Watermark Acak)
┌─────────────────────────────────────────┐
│ Gambar          │ Akurasi DCT  │ Akurasi IWT │
├─────────────────────────────────────────┤
│ photo1.jpg      │ 100.00%      │ 96.20%      │
│ photo2.jpg      │ 98.50%       │ 97.80%      │
└─────────────────────────────────────────┘
```

### 3. Urutan Tampilan Hasil

Sekarang hasil batch processing ditampilkan dalam urutan ini:

1. ✅ **Pesan Sukses** - "Berhasil memproses N gambar!"
2. **🔐 Hasil Ekstraksi** ← **BARU & PRIORITAS UTAMA**
   - Tabel akurasi ekstraksi
   - Detail per gambar (expandable)
3. **Tabel Detail Hasil** - Metrik lengkap semua gambar
4. **Tabel Per Gambar (DCT vs IWT)** - Perbandingan per file
5. **Tabel Ringkasan** - Rata-rata & Std Dev
6. **Grafik Perbandingan** - Visualisasi metrik
7. **Preview Citra** - Gambar stego
8. **Download Hasil** - Tombol download

## Fitur Utama

### ✅ Verifikasi Akurasi
Pastikan watermark berhasil diekstrak dengan akurasi tinggi:
- Akurasi 100% = Watermark extracted perfectly
- Akurasi > 90% = Good extraction
- Akurasi < 80% = Perlu investigasi

### ✅ Ekspandable Detail
Klik pada setiap gambar untuk melihat:
- Pesan asli (jika mode text)
- Pesan terekstrak dari DCT
- Pesan terekstrak dari IWT
- Perbandingan akurasi kedua metode

### ✅ Komparasi DCT vs IWT
Bandingkan akurasi ekstraksi:
- DCT biasanya lebih konsisten untuk teks
- IWT bergantung pada resolusi subband

## Fungsi Helper

### `extract_dct(stego_img, alpha=10.0)`
Mengekstrak watermark dari stego image dengan metode DCT.

**Parameter:**
- `stego_img`: Gambar stego (grayscale)
- `alpha`: Kekuatan embedding (default: 10.0)

**Return:**
- `extracted`: Array bit (uint8) ukuran (H/8, W/8)

### `extract_iwt(stego_img, cover_img, watermark_shape, wavelet='haar')`
Mengekstrak watermark dari stego image dengan metode IWT.

**Parameter:**
- `stego_img`: Gambar stego (grayscale)
- `cover_img`: Gambar original/cover (opsional tapi rekomended)
- `watermark_shape`: Dimensi watermark (tuple)
- `wavelet`: Tipe wavelet (default: 'haar')

**Return:**
- `extracted`: Array bit (uint8) bentuk watermark_shape

## Contoh Penggunaan

```python
# Upload file text
original_text = "Pesan Rahasia"
message_binary = text_to_binary(original_text)
watermark = np.array([int(bit) for bit in message_binary...])

# Batch processing
batch_rows, batch_preview, extraction_results = process_batch_images(
    uploaded_files, 
    target_size=(512, 512),
    wm_size=(64, 64),
    alpha_dct=10.0,
    alpha_iwt=2.0,
    wavelet='haar',
    watermark_mode='text',
    watermark_data=watermark
)

# Cek hasil ekstraksi
for result in extraction_results:
    print(f"{result['filename']}:")
    print(f"  DCT Accuracy: {result['acc_dct']:.2f}%")
    print(f"  IWT Accuracy: {result['acc_iwt']:.2f}%")
    print(f"  Extracted (DCT): {result['extracted_msg_dct']}")
    print(f"  Extracted (IWT): {result['extracted_msg_iwt']}")
```

## Troubleshooting

### ❌ Akurasi Rendah
- Pastikan parameter `alpha_dct` dan `alpha_iwt` tidak terlalu kecil
- Gunakan gambar berkualitas tinggi
- Cobalah dengan ukuran gambar yang lebih besar (minimal 512x512)

### ❌ Pesan Terekstrak Kacau
- Kemungkinan compression atau noise pada gambar
- Verifikasi pesan asli dengan akurasi 100%
- Coba increase nilai `alpha`

### ✅ Akurasi 100%
- Watermark extracted sempurna
- Metode embedding/ekstraksi bekerja dengan baik
- Parameternya optimal untuk jenis gambar ini

## File yang Dimodifikasi
- `app.py` - Main application file
  - Fungsi: `process_batch_images()`
  - UI: `page_batch_processing()`

## Catatan Penting
- Ekstraksi hanya bekerja jika cover image tersedia (untuk IWT)
- Akurasi tergantung pada parameter embedding
- Watermark acak memberikan akurasi relatif konsisten (~95-99%)
- Watermark text memberikan akurasi tergantung pada panjang pesan
