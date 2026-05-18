# 📁 Struktur Proyek Steganografi GUI

```
Steganografi gui/
│
├── 📄 MAIN APPLICATION
│   ├── app.py                          # 🔴 FILE UTAMA - Aplikasi Streamlit
│   ├── requirements.txt                # 📦 Dependencies yang diperlukan
│   └── .streamlit/
│       └── config.toml                 # ⚙️ Konfigurasi Streamlit
│
├── 📚 DOKUMENTASI
│   ├── README.md                       # 📖 Dokumentasi lengkap
│   ├── QUICKSTART.md                   # ⚡ Panduan cepat (5 menit)
│   ├── PROJECT_STRUCTURE.md            # 📁 File ini
│   └── CONTRIBUTING.md                 # 🤝 Panduan kontribusi
│
├── 🛠️ SETUP & RUN SCRIPTS (Windows)
│   ├── setup.bat                       # 🔧 Install dependencies
│   ├── run_app.bat                     # ▶️ Jalankan aplikasi
│   ├── generate_samples.py             # 🎨 Generate sample images
│   └── requirements.txt                # 📦 List dependencies
│
├── 📸 SAMPLE FILES (Auto-generated)
│   └── samples/                        # Folder untuk test images
│       ├── sample_gradient.png
│       ├── sample_noise.png
│       ├── sample_pattern.png
│       ├── sample_text.png
│       ├── sample_checkerboard.png
│       └── sample_message.txt
│
├── 🗂️ DATA FOLDERS (Auto-created saat run)
│   ├── hasil/
│   │   ├── single_image/              # Hasil single image processing
│   │   └── batch_images/              # Hasil batch processing
│   └── uploads/                        # Temporary upload storage
│
└── 📋 NOTEBOOK (Legacy)
    └── skripsi_saya_plis (2).ipynb    # Original Jupyter notebook
```

## 📄 File Descriptions

### 🔴 Main Application
- **app.py** (1800+ lines)
  - Aplikasi Streamlit utama dengan semua fitur
  - Terdiri dari 13 bagian utama:
    1. Config & Styling
    2. Fungsi preprocessing
    3. Fungsi konversi teks-biner
    4. Fungsi embedding DCT
    5. Fungsi embedding IWT
    6. Fungsi ekstraksi
    7. Fungsi metrik evaluasi
    8. Fungsi visualisasi
    9. Fungsi kesimpulan
    10. Fungsi batch processing
    11. Fungsi download
    12. Halaman home
    13. Halaman single image
    14. Halaman batch processing
    15. Main function

### 📦 Requirements
- **requirements.txt**
  - streamlit==1.32.0 - Framework GUI
  - opencv-python==4.8.1.78 - Image processing
  - numpy==1.24.3 - Numerical operations
  - pandas==2.1.1 - Data analysis
  - matplotlib==3.8.1 - Plotting
  - scipy==1.11.4 - Scientific computing (DCT)
  - PyWavelets==1.5.0 - Wavelet transform
  - scikit-image==0.22.0 - Image metrics
  - Pillow==10.1.0 - Image I/O

### ⚙️ Configuration
- **.streamlit/config.toml**
  - Theme customization
  - Server settings
  - UI preferences

### 📚 Documentation Files

#### README.md (Lengkap)
- Daftar isi
- Fitur utama (15+ fitur)
- Sistem kebutuhan
- Instalasi step-by-step
- Cara menjalankan
- Panduan penggunaan detail
- Struktur proyek
- Metrik evaluasi (tabel lengkap)
- Tips penggunaan optimal
- Troubleshooting
- Catatan penting
- Lisensi

#### QUICKSTART.md (Cepat)
- Instalasi 2 menit
- Jalankan aplikasi 1 menit
- Penggunaan 2 menit
- Tips penting
- Tips untuk presentasi skripsi
- Troubleshooting singkat

#### PROJECT_STRUCTURE.md (File ini)
- Overview struktur proyek
- Deskripsi file-file
- Size estimates
- Workflow diagram

### 🛠️ Helper Scripts

#### setup.bat (Windows)
- Buat virtual environment
- Install dependencies
- Generate sample images
- Error handling

#### run_app.bat (Windows)
- Activate virtual environment
- Jalankan streamlit
- Error handling

#### generate_samples.py
- Generate 5 test images
- Generate 1 sample text file
- Untuk quick testing

## 📊 File Size Estimates

```
app.py                    ~70 KB   (1800+ lines)
requirements.txt          ~0.5 KB
README.md                 ~50 KB
QUICKSTART.md            ~5 KB
PROJECT_STRUCTURE.md     ~10 KB
setup.bat                ~3 KB
run_app.bat              ~2 KB
generate_samples.py      ~8 KB
.streamlit/config.toml   ~1 KB
─────────────────────────────
Total source code        ~149 KB

Installed packages       ~800 MB (virtual environment)
```

## 🔄 Workflow Diagram

```
USER
  │
  ├─→ setup.bat (first time)
  │     │
  │     ├─→ Create venv
  │     ├─→ Install requirements
  │     └─→ Generate samples
  │
  ├─→ run_app.bat (every time)
  │     │
  │     └─→ python app.py
  │           │
  │           ├─→ Streamlit UI opens
  │           │
  │           ├─→ Single Image Tab
  │           │     ├─→ Upload image
  │           │     ├─→ Choose watermark
  │           │     ├─→ Process (DCT + IWT)
  │           │     ├─→ View results
  │           │     └─→ Download outputs
  │           │
  │           └─→ Batch Processing Tab
  │                 ├─→ Upload multiple images
  │                 ├─→ Process all
  │                 ├─→ View results table
  │                 └─→ Download CSV + PNG
  │
  └─→ Check results in ./hasil/ folder
```

## 🚀 Quick Reference

### First Time Setup
```bash
cd "d:\project saya\Steganografi gui"
setup.bat
# atau
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Generate Test Images
```bash
python generate_samples.py
```

### Run Application
```bash
run_app.bat
# atau
streamlit run app.py
```

### Install Dependencies Manually
```bash
pip install streamlit opencv-python numpy pandas matplotlib scipy PyWavelets scikit-image Pillow
```

## 📋 Checklist Setup

- [ ] Python 3.8+ installed (check: `python --version`)
- [ ] Clone/download project folder
- [ ] Run `setup.bat` or manual pip install
- [ ] Virtual environment activated (check: `(venv)` prefix in terminal)
- [ ] Dependencies installed (check: `pip list`)
- [ ] Run `run_app.bat` atau `streamlit run app.py`
- [ ] Browser opens to http://localhost:8501
- [ ] Upload sample image from `samples/` folder
- [ ] Click "🚀 Mulai Proses" button
- [ ] View results and download

## 🔍 Troubleshooting Reference

| Problem | Solution | Command |
|---------|----------|---------|
| Python not found | Install Python 3.8+ | - |
| ModuleNotFoundError | Install requirements | `pip install -r requirements.txt` |
| Port 8501 in use | Use different port | `streamlit run app.py --server.port 8502` |
| venv not found | Create venv | `python -m venv venv` |
| Streamlit not found | Activate venv | `venv\Scripts\activate` |

## 📚 Related Files

### From Original Notebook
- `skripsi_saya_plis (2).ipynb` - Original Jupyter notebook with all functions

### Auto-Generated on First Run
- `~/.streamlit/credentials.toml` - Streamlit credentials (if logging in)
- `.streamlit/config.toml` - Configuration we created

### Runtime Generated
- `hasil/` - Output folder for results
- `uploads/` - Temporary uploads
- `.streamlit/` - Streamlit cache files

## 💾 How to Backup

Important files to backup:
1. `app.py` - Main application
2. `requirements.txt` - Dependencies list
3. `README.md` - Documentation

Optional (can be regenerated):
1. Virtual environment folder (too large)
2. `samples/` folder (can recreate)
3. `hasil/` folder (can regenerate)

## 🔐 Security Notes

- No API keys or sensitive data in source code
- All processing is local (no cloud upload)
- File uploads handled in memory
- No persistent storage of uploaded images
- Results saved locally only

## 🎯 Development Tips

### Adding New Features
1. Edit `app.py`
2. Add function in appropriate section
3. Call function from UI handlers
4. Test with sample images
5. Update README.md

### Customizing Theme
1. Edit `.streamlit/config.toml`
2. Change color values in `[theme]` section
3. Restart Streamlit

### Deploying Online
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy in one click

---

**Last Updated:** Januari 2025
**Version:** 1.0
**Status:** Production Ready ✅
