@echo off
REM Run script untuk menjalankan aplikasi di Windows

echo.
echo ============================================================
echo  Aplikasi Analisis Steganografi DCT vs IWT
echo ============================================================
echo.

REM Cek apakah requirements terinstall
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Dependencies belum terinstall!
    echo Silakan jalankan setup.bat terlebih dahulu
    pause
    exit /b 1
)

REM Activate virtual environment jika ada
if exist venv\Scripts\activate.bat (
    echo [INFO] Mengaktifkan virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo [OK] Menjalankan aplikasi Streamlit...
echo Aplikasi akan terbuka di: http://localhost:8501
echo.
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.
echo ============================================================
echo.

REM Run streamlit
streamlit run app.py

pause
