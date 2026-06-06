@echo off
REM Setup script untuk Windows
REM Jalankan: setup.bat

echo.
echo ============================================================
echo  Aplikasi Analisis Steganografi DCT vs IWT
echo  Setup Script untuk Windows
echo ============================================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python 3.8+ dari https://www.python.org/
    echo Pastikan "Add Python to PATH" dicentang saat instalasi.
    pause
    exit /b 1
)

echo [OK] Python terdeteksi
python --version

set "PYTHON_EXE="
if exist .venv\Scripts\python.exe (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else if exist venv\Scripts\python.exe (
    set "PYTHON_EXE=venv\Scripts\python.exe"
)

REM Buat virtual environment
echo.
echo [STEP 1/4] Membuat virtual environment...
if defined PYTHON_EXE (
    echo Virtual environment sudah ada. Skip...
) else (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal membuat virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment berhasil dibuat
    set "PYTHON_EXE=.venv\Scripts\python.exe"
)

REM Upgrade pip
echo.
echo [STEP 2/4] Upgrade pip...
"%PYTHON_EXE%" -m pip install --upgrade pip

REM Install requirements
echo.
echo [STEP 3/4] Install dependencies dari requirements.txt...
echo Ini mungkin memakan waktu beberapa menit...
echo.
"%PYTHON_EXE%" -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Gagal install dependencies!
    echo Silakan coba:
    echo   1. Pastikan file requirements.txt ada di folder ini
    echo   2. Cek koneksi internet
    echo   3. Coba ulang script ini
    pause
    exit /b 1
)

REM Generate sample images
echo.
echo [OPTIONAL] Generate sample images untuk testing...
"%PYTHON_EXE%" generate_samples.py

REM Selesai
echo.
echo ============================================================
echo  SETUP SELESAI!
echo ============================================================
echo.
echo Untuk menjalankan aplikasi, ketik:
echo   "%PYTHON_EXE%" -m streamlit run app.py
echo.
echo Atau klik run_app.bat
echo.
pause
