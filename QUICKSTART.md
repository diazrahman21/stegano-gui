# 🚀 QUICK START - Mulai dalam 5 Menit

## 1. Instalasi Dependencies (2 menit)

### Windows PowerShell:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux Terminal:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Tunggu sampai semua library selesai terinstall. Ini yang paling lama!

## 2. Jalankan Aplikasi (1 menit)

```bash
streamlit run app.py
```

Browser akan otomatis terbuka ke `http://localhost:8501`

Jika tidak, buka browser dan ketik URL tersebut.

## 3. Gunakan Aplikasi (2 menit)

### Untuk Single Image:
1. Klik tab **"📸 Single Image"**
2. Upload gambar Anda
3. Pilih watermark (random atau TXT)
4. Klik **"🚀 Mulai Proses Steganografi"**
5. Lihat hasil dan download

### Untuk Multiple Images:
1. Klik tab **"🎞️ Batch Processing"**
2. Upload beberapa gambar sekaligus
3. Klik **"🚀 Mulai Proses Batch"**
4. Download hasil CSV & grafik

## 📌 Tips Penting

| Kebutuhan | Rekomendasi |
|-----------|-------------|
| Format Gambar | PNG atau JPG |
| Ukuran Gambar | 512×512 px atau lebih besar |
| Pesan TXT | Max 64 karakter |
| Untuk Batch | Max 20 gambar sekaligus |

## ⚙️ Setting Parameter (Optional)

Semua setting ada di **sidebar kiri**:

- **Alpha DCT:** Default 10.0 (biarkan aja)
- **Alpha IWT:** Default 2.0 (biarkan aja)
- **Ukuran Citra:** Default 512×512 (biarkan aja)

Untuk hasil cepat, gunakan default saja!

## 🎯 File Hasil

Setelah proses, Anda bisa download:
- ✅ Stego DCT (gambar hasil penyisipan DCT)
- ✅ Stego IWT (gambar hasil penyisipan IWT)
- ✅ Grafik perbandingan metrik
- ✅ CSV hasil evaluasi

## ❌ Jika Ada Error

### Error 1: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Error 2: Port sudah digunakan
```bash
streamlit run app.py --server.port 8502
```

### Error 3: Gambar tidak terbaca
- Pastikan format PNG atau JPG
- Cek ukuran file tidak terlalu besar
- Coba gambar lain

## 📊 Lihat Hasil Langsung

Semua hasil divisualisasi di GUI:
- ✓ Preview citra asli dan hasil penyisipan
- ✓ Histogram perbandingan
- ✓ Tabel metrik (MSE, PSNR, SSIM, NPCR, UACI)
- ✓ Grafik bar perbandingan metode
- ✓ Kesimpulan otomatis metode mana yang lebih baik

## 🎓 Untuk Presentasi Skripsi

Gunakan file yang diunduh:
1. **Screenshot GUI** - Tunjukkan interface yang user-friendly
2. **Gambar hasil** (stego_dct.png, stego_iwt.png) - Tunjukkan visual
3. **Grafik metrik** - Jelaskan perbandingan metode
4. **CSV hasil** - Lampirkan di appendix laporan

## ✅ Selesai!

Anda sekarang siap menggunakan aplikasi steganografi. Selamat menganalisis! 🎉

Untuk info lengkap, buka `README.md`
