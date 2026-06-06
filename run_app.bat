@echo off
REM Run script untuk menjalankan aplikasi di Windows

echo.
echo ============================================================
echo  Aplikasi Analisis Steganografi DCT vs IWT
echo ============================================================
echo.

set "PYTHON_EXE="
if exist .venv\Scripts\python.exe (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else if exist venv\Scripts\python.exe (
    set "PYTHON_EXE=venv\Scripts\python.exe"
)

if not defined PYTHON_EXE (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo Silakan jalankan setup.bat terlebih dahulu
    pause
    exit /b 1
)

REM Cek apakah Streamlit terinstall di environment lokal
"%PYTHON_EXE%" -m pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Streamlit belum terinstall di virtual environment!
    echo Silakan jalankan setup.bat terlebih dahulu
    pause
    exit /b 1
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
"%PYTHON_EXE%" -m streamlit run app.py

pause
