import streamlit as st
import cv2
import pywt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity
from PIL import Image
import io
import os
from pathlib import Path
from datetime import datetime

# ============================================================================
# KONFIGURASI STREAMLIT
# ============================================================================
st.set_page_config(
    page_title="Analisis Keamanan Steganografi DCT vs IWT",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-base: #f6f7f9;
        --bg-panel: #ffffff;
        --bg-elev: #f1f3f6;
        --text-primary: #0f172a;
        --text-muted: #5b6474;
        --accent: #0ea5a4;
        --accent-strong: #0b8c8b;
        --border-soft: #e5e7eb;
        --shadow-soft: 0 10px 30px rgba(15, 23, 42, 0.08);
        --radius-lg: 18px;
        --radius-md: 12px;
        --radius-sm: 10px;
    }

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        color: var(--text-primary);
    }

    .stApp {
        background: radial-gradient(1200px 600px at 80% -10%, rgba(14, 165, 164, 0.08), transparent 55%),
                    radial-gradient(900px 500px at 10% 0%, rgba(15, 23, 42, 0.06), transparent 50%),
                    var(--bg-base);
    }

    .block-container {
        padding: 2.25rem 2.5rem 4rem;
        max-width: 1200px;
    }

    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    h1 {
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 0.25rem;
    }

    h2 {
        font-size: 1.6rem;
        margin-top: 1.6rem;
        border-bottom: 1px solid var(--border-soft);
        padding-bottom: 0.6rem;
    }

    h3 {
        font-size: 1.2rem;
        margin-top: 1.1rem;
    }

    p, li, span {
        color: var(--text-muted);
        line-height: 1.7;
        font-weight: 400;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--bg-panel);
        border-radius: var(--radius-md);
        padding: 0.35rem 0.4rem;
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-soft);
    }

    .stTabs [data-baseweb="tab-list"] button {
        border-radius: var(--radius-sm);
        padding: 0.4rem 0.85rem;
    }

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 0.98rem;
        font-weight: 600;
        color: var(--text-muted);
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: var(--bg-elev);
        border: 1px solid var(--border-soft);
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: var(--text-primary);
    }

    .stButton > button, .stDownloadButton > button {
        background: var(--accent);
        color: #ffffff;
        border: none;
        border-radius: 999px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 8px 18px rgba(14, 165, 164, 0.22);
        transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--accent-strong);
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(14, 165, 164, 0.28);
    }

    .stButton > button:focus, .stDownloadButton > button:focus {
        outline: 2px solid rgba(14, 165, 164, 0.4);
        outline-offset: 2px;
    }

    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    .stSelectbox select, .stFileUploader, .stDateInput input {
        border-radius: var(--radius-md);
        border: 1px solid var(--border-soft);
        background: var(--bg-panel);
        padding: 0.55rem 0.75rem;
        box-shadow: none;
        transition: border 0.15s ease, box-shadow 0.15s ease;
    }

    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus,
    .stSelectbox select:focus, .stFileUploader:focus-within, .stDateInput input:focus {
        border-color: rgba(14, 165, 164, 0.5);
        box-shadow: 0 0 0 3px rgba(14, 165, 164, 0.15);
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        color: var(--accent);
    }

    .stMetric {
        background: var(--bg-panel);
        border: 1px solid var(--border-soft);
        border-radius: var(--radius-md);
        padding: 0.85rem;
        box-shadow: var(--shadow-soft);
    }

    .stDataFrame, .stTable {
        border-radius: var(--radius-md);
        border: 1px solid var(--border-soft);
        overflow: hidden;
        box-shadow: var(--shadow-soft);
    }

    .stAlert {
        border-radius: var(--radius-md);
        border: 1px solid var(--border-soft);
        box-shadow: var(--shadow-soft);
    }

    .stSidebar {
        background: var(--bg-panel);
        border-right: 1px solid var(--border-soft);
    }

    .stSidebar .block-container {
        padding: 2rem 1.5rem;
    }

    .sidebar-section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0.9rem 0 0.35rem;
    }

    .sidebar-section-note {
        font-size: 0.82rem;
        color: var(--text-muted);
        font-style: italic;
        margin-bottom: 0.75rem;
    }

    .sidebar-param-card {
        background: var(--bg-elev);
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 0.75rem 0.85rem;
        margin-bottom: 0.6rem;
        box-shadow: none;
    }

    .sidebar-param-card .label {
        display: block;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.18rem;
    }

    .sidebar-param-card .value {
        display: block;
        font-size: 1.18rem;
        line-height: 1.2;
        font-weight: 700;
        color: var(--text-primary);
        word-break: break-word;
    }

    .sidebar-param-card .subvalue {
        display: block;
        margin-top: 0.1rem;
        font-size: 0.8rem;
        color: var(--text-muted);
    }

    .stSidebar .stMetric {
        padding: 0.4rem 0.35rem;
    }

    .stSidebar .stMetric [data-testid="stMetricLabel"] {
        font-size: 0.74rem;
        line-height: 1.2;
        color: var(--text-muted);
    }

    .stSidebar .stMetric [data-testid="stMetricValue"] {
        font-size: 1.15rem;
        line-height: 1.1;
    }

    .stSidebar .stSubheader {
        font-size: 1rem;
        margin-top: 0.85rem;
        margin-bottom: 0.35rem;
    }

    .success-box, .info-box {
        background-color: var(--bg-panel);
        border: 1px solid var(--border-soft);
        padding: 1rem 1.2rem;
        border-radius: var(--radius-md);
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem 1.25rem 3rem;
        }

        h1 {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNGSI PREPROCESSING CITRA
# ============================================================================
def preprocess_image(image_bytes, target_size=(512, 512)):
    """Konversi citra ke grayscale dan resize"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img_bgr is None:
        raise ValueError("File tidak dapat dibaca sebagai citra")
    
    # Konversi ke grayscale
    if len(img_bgr.shape) == 3:
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img_bgr
    
    # Resize
    img_resized = cv2.resize(img_gray, target_size, interpolation=cv2.INTER_AREA)
    
    return img_resized

# ============================================================================
# FUNGSI KONVERSI TEKS KE BINER
# ============================================================================
def text_to_binary(text):
    """Konversi teks ASCII ke string biner"""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary_str):
    """Konversi string biner kembali ke teks ASCII"""
    if len(binary_str) % 8 != 0:
        binary_str = binary_str[:-(len(binary_str) % 8)]
    text = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
    return text

# ============================================================================
# FUNGSI EMBEDDING DCT
# ============================================================================
def embed_dct(cover_img, watermark_bits, alpha=10.0):
    """Embedding watermark menggunakan DCT (block-wise 8x8)"""
    h, w = cover_img.shape
    stego = cover_img.astype(np.float32).copy()

    if h % 8 != 0 or w % 8 != 0:
        raise ValueError('Ukuran citra harus kelipatan 8 untuk embedding DCT')

    blocks_y, blocks_x = h // 8, w // 8
    if watermark_bits.shape != (blocks_y, blocks_x):
        raise ValueError(f'Ukuran watermark harus {(blocks_y, blocks_x)}')

    p1, p2 = (3, 4), (4, 3)

    for by in range(blocks_y):
        for bx in range(blocks_x):
            y0, y1 = by * 8, (by + 1) * 8
            x0, x1 = bx * 8, (bx + 1) * 8

            block = stego[y0:y1, x0:x1]
            dct_block = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

            b = int(watermark_bits[by, bx])
            c1, c2 = dct_block[p1], dct_block[p2]
            avg = (c1 + c2) / 2.0

            if b == 1:
                dct_block[p1] = avg + alpha / 2.0
                dct_block[p2] = avg - alpha / 2.0
            else:
                dct_block[p1] = avg - alpha / 2.0
                dct_block[p2] = avg + alpha / 2.0

            stego[y0:y1, x0:x1] = idct(idct(dct_block, axis=0, norm='ortho'), axis=1, norm='ortho')

    return np.clip(np.round(stego), 0, 255).astype(np.uint8)

# ============================================================================
# FUNGSI EMBEDDING IWT
# ============================================================================
def embed_iwt_hh(cover_img, watermark_bits, alpha=2.0, wavelet='haar'):
    """Embedding watermark pada subband HH menggunakan IWT"""
    cover_int = cover_img.astype(np.int16)
    LL, (LH, HL, HH) = pywt.dwt2(cover_int, wavelet)

    wm_hh = cv2.resize(watermark_bits.astype(np.float32),
                       (HH.shape[1], HH.shape[0]),
                       interpolation=cv2.INTER_NEAREST)
    wm_sign = (wm_hh * 2.0) - 1.0

    HH_embedded = HH + alpha * wm_sign
    stego_recon = pywt.idwt2((LL, (LH, HL, HH_embedded)), wavelet)
    stego_recon = np.clip(np.round(stego_recon), 0, 255).astype(np.uint8)
    stego_recon = cv2.resize(stego_recon, (cover_img.shape[1], cover_img.shape[0]), 
                             interpolation=cv2.INTER_AREA)

    return stego_recon

# ============================================================================
# FUNGSI EKSTRAKSI DCT
# ============================================================================
def extract_dct(stego_img, alpha=10.0):
    """Ekstraksi watermark dari stego DCT"""
    h, w = stego_img.shape
    extracted = np.zeros((h // 8, w // 8), dtype=np.uint8)

    if h % 8 != 0 or w % 8 != 0:
        raise ValueError('Ukuran citra harus kelipatan 8')

    p1, p2 = (3, 4), (4, 3)

    for by in range(h // 8):
        for bx in range(w // 8):
            y0, y1 = by * 8, (by + 1) * 8
            x0, x1 = bx * 8, (bx + 1) * 8

            block = stego_img[y0:y1, x0:x1].astype(np.float32)
            dct_block = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

            c1, c2 = dct_block[p1], dct_block[p2]
            extracted[by, bx] = 1 if c1 > c2 else 0

    return extracted

# ============================================================================
# FUNGSI EKSTRAKSI IWT
# ============================================================================
def extract_iwt(stego_img, cover_img=None, watermark_shape=(64, 64), wavelet='haar'):
    """Ekstraksi watermark dari stego IWT.

    Jika cover_img tersedia, ekstraksi dilakukan dari selisih koefisien HH
    stego dan cover. Ini sesuai dengan embedding yang menambah/mengurangi
    koefisien HH berdasarkan bit watermark.
    """
    stego_int = stego_img.astype(np.int16)
    _, (_, _, HH) = pywt.dwt2(stego_int, wavelet)

    if cover_img is not None:
        cover_int = cover_img.astype(np.int16)
        _, (_, _, HH_cover) = pywt.dwt2(cover_int, wavelet)
        signal = HH - HH_cover
    else:
        HH_min, HH_max = HH.min(), HH.max()
        signal = (HH - HH_min) / (HH_max - HH_min + 1e-12) - 0.5

    signal_resized = cv2.resize(signal.astype(np.float32),
                                (watermark_shape[1], watermark_shape[0]),
                                interpolation=cv2.INTER_AREA)
    return (signal_resized > 0).astype(np.uint8)

# ============================================================================
# FUNGSI METRIK KUALITAS & KEAMANAN
# ============================================================================
def compute_npcr(img1, img2):
    """Hitung NPCR (Number of Pixel Change Rate)"""
    img1 = img1.astype(np.uint8)
    img2 = img2.astype(np.uint8)
    diff = img1 != img2
    return (np.sum(diff) / diff.size) * 100.0

def compute_uaci(img1, img2):
    """Hitung UACI (Unified Average Changed Intensity)"""
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    return np.mean(np.abs(img1 - img2) / 255.0) * 100.0

def evaluate_all(cover, stego):
    """Hitung semua metrik evaluasi"""
    mse_val = mean_squared_error(cover, stego)
    psnr_val = peak_signal_noise_ratio(cover, stego, data_range=255)
    ssim_val = structural_similarity(cover, stego, data_range=255)
    npcr_val = compute_npcr(cover, stego)
    uaci_val = compute_uaci(cover, stego)

    return {
        'MSE': float(mse_val),
        'PSNR (dB)': float(psnr_val),
        'SSIM': float(ssim_val),
        'NPCR (%)': float(npcr_val),
        'UACI (%)': float(uaci_val),
    }

# ============================================================================
# FUNGSI VISUALISASI
# ============================================================================
def plot_images_and_histograms(cover, stego_dct, stego_iwt):
    """Visualisasi citra dan histogram"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    images = [cover, stego_dct, stego_iwt]
    titles = ['Citra Asli (Cover)', 'Stego DCT', 'Stego IWT']

    for i, (img, title) in enumerate(zip(images, titles)):
        axes[0, i].imshow(img, cmap='gray', vmin=0, vmax=255)
        axes[0, i].set_title(title, fontsize=12, fontweight='bold')
        axes[0, i].axis('off')

    for i, (img, title) in enumerate(zip(images, titles)):
        axes[1, i].hist(img.ravel(), bins=256, range=(0, 255), color='steelblue', alpha=0.8)
        axes[1, i].set_title(f'Histogram - {title}', fontsize=11)
        axes[1, i].set_xlabel('Intensitas Piksel')
        axes[1, i].set_ylabel('Frekuensi')
        axes[1, i].grid(alpha=0.3)

    plt.tight_layout()
    return fig

def plot_metrics_comparison(df_metrics):
    """Visualisasi perbandingan metrik"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    quality_cols = ['MSE', 'PSNR (dB)', 'SSIM']
    security_cols = ['NPCR (%)', 'UACI (%)']

    df_metrics[quality_cols].plot(kind='bar', ax=axes[0], rot=0, color=['#d62728', '#2ca02c', '#1f77b4'])
    axes[0].set_title('Perbandingan Kualitas (MSE, PSNR, SSIM)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Nilai Metrik')
    axes[0].set_xlabel('Metode')
    axes[0].legend(loc='best')
    axes[0].grid(axis='y', alpha=0.3)

    df_metrics[security_cols].plot(kind='bar', ax=axes[1], rot=0, color=['#ff7f0e', '#17becf'])
    axes[1].set_title('Perbandingan Keamanan (NPCR, UACI)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Persentase (%)')
    axes[1].set_xlabel('Metode')
    axes[1].legend(loc='best')
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def build_per_image_table(batch_df, metrics):
    """Bangun tabel per gambar dengan kolom metrik bertingkat (Metric: DCT vs IWT)."""
    # Pivot: index=filename, columns=method, values=metrics
    pivot_df = batch_df.pivot_table(
        index='filename',
        columns='method',
        values=metrics,
        aggfunc='first'
    )
    
    # Reorder columns: (Metric, Method) dengan urutan Metric pertama, Method kedua
    # Sehingga hasilnya: MSE-DCT, MSE-IWT, PSNR-DCT, PSNR-IWT, ...
    ordered_cols = [(metric, method) for metric in metrics for method in ['DCT', 'IWT']]
    pivot_df = pivot_df[ordered_cols]
    
    # Set nama level pada MultiIndex
    pivot_df.columns.names = ['Metric', 'Method']
    
    return pivot_df

def format_detail_table(batch_df, metrics):
    """Format tabel detail dengan kolom metrik bertingkat (Metric: DCT vs IWT)."""
    # Buat MultiIndex columns
    data_list = []
    
    for _, row in batch_df.iterrows():
        row_dict = {}
        row_dict[('', 'Filename')] = row['filename']
        row_dict[('', 'Method')] = row['method']
        
        for metric in metrics:
            row_dict[(metric, '')] = row[metric]
        
        data_list.append(row_dict)
    
    detail_df = pd.DataFrame(data_list)
    
    # Flatten MultiIndex columns untuk hasil yang lebih baik
    # Restructure: Group by filename+method, kemudian pivotkan metrics dengan DCT/IWT
    detail_grouped = batch_df.set_index(['filename', 'method'])[metrics].reset_index()
    
    # Pivot untuk mendapatkan struktur yang lebih baik
    result = detail_grouped.pivot_table(
        index='filename',
        columns='method',
        values=metrics,
        aggfunc='first'
    )
    
    # Reorder columns
    ordered_cols = [(metric, method) for metric in metrics for method in ['DCT', 'IWT']]
    result = result[ordered_cols]
    result.columns.names = ['Metric', 'Method']
    
    return result

def plot_batch_metrics(batch_df):
    """Visualisasi perbandingan metrik batch"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # Rata-rata per method
    summary = batch_df.groupby('method')[['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']].mean()

    metrics = [('MSE', 0, 0), ('PSNR (dB)', 0, 1), ('SSIM', 0, 2),
               ('NPCR (%)', 1, 0), ('UACI (%)', 1, 1)]

    for metric, row, col in metrics:
        summary[metric].plot(kind='bar', ax=axes[row, col], color=['#1f77b4', '#ff7f0e'])
        axes[row, col].set_title(f'Rata-rata {metric}', fontsize=11, fontweight='bold')
        axes[row, col].set_ylabel('Nilai')
        axes[row, col].set_xticklabels(axes[row, col].get_xticklabels(), rotation=45)
        axes[row, col].grid(axis='y', alpha=0.3)

    # Tabel ringkasan di cell kosong
    axes[1, 2].axis('off')
    summary_text = "Ringkasan Metrik:\n\n"
    for idx, row in summary.iterrows():
        summary_text += f"{idx}:\n"
        for col in summary.columns:
            summary_text += f"  {col}: {row[col]:.4f}\n"
    axes[1, 2].text(0.1, 0.5, summary_text, fontsize=9, family='monospace',
                    verticalalignment='center')

    plt.tight_layout()
    return fig

# ============================================================================
# FUNGSI KESIMPULAN
# ============================================================================
def generate_conclusion(df_metrics):
    """Generate kesimpulan otomatis"""
    conclusion = []

    # MSE
    mse_best = df_metrics['MSE'].idxmin()
    conclusion.append(f"🥇 **Metode dengan MSE terbaik:** {mse_best} ({df_metrics.loc[mse_best, 'MSE']:.4f})")

    # PSNR
    psnr_best = df_metrics['PSNR (dB)'].idxmax()
    conclusion.append(f"🥇 **Metode dengan PSNR terbaik:** {psnr_best} ({df_metrics.loc[psnr_best, 'PSNR (dB)']:.4f} dB)")

    # SSIM
    ssim_best = df_metrics['SSIM'].idxmax()
    conclusion.append(f"🥇 **Metode dengan SSIM terbaik:** {ssim_best} ({df_metrics.loc[ssim_best, 'SSIM']:.4f})")

    # NPCR
    npcr_best = df_metrics['NPCR (%)'].idxmax()
    conclusion.append(f"🥇 **Metode dengan NPCR terbaik:** {npcr_best} ({df_metrics.loc[npcr_best, 'NPCR (%)']:.4f}%)")

    # UACI
    uaci_best = df_metrics['UACI (%)'].idxmax()
    conclusion.append(f"🥇 **Metode dengan UACI terbaik:** {uaci_best} ({df_metrics.loc[uaci_best, 'UACI (%)']:.4f}%)")

    # Kualitas vs Keamanan
    mse_winner = df_metrics['MSE'].idxmin()
    psnr_winner = df_metrics['PSNR (dB)'].idxmax()
    ssim_winner = df_metrics['SSIM'].idxmax()
    quality_votes = {mse_winner: 1, psnr_winner: 1, ssim_winner: 1}
    quality_best = max(quality_votes, key=quality_votes.get)

    npcr_winner = df_metrics['NPCR (%)'].idxmax()
    uaci_winner = df_metrics['UACI (%)'].idxmax()
    security_votes = {npcr_winner: 1, uaci_winner: 1}
    security_best = max(security_votes, key=security_votes.get)

    conclusion.append(f"\n📊 **Kualitas Citra:** {quality_best} lebih unggul (MSE/PSNR/SSIM)")
    conclusion.append(f"🔒 **Keamanan Steganografi:** {security_best} lebih unggul (NPCR/UACI)")

    if quality_best == security_best:
        conclusion.append(f"\n✅ **Kesimpulan:** {quality_best} lebih konsisten unggul pada kualitas dan keamanan.")
    else:
        conclusion.append(f"\n⚠️ **Kesimpulan:** Terdapat trade-off antara kualitas dan keamanan.")
        conclusion.append(f"   - Pilih {quality_best} untuk memprioritaskan kualitas visual")
        conclusion.append(f"   - Pilih {security_best} untuk memprioritaskan keamanan steganografi")

    return "\n".join(conclusion)

# ============================================================================
# FUNGSI BATCH PROCESSING
# ============================================================================
def process_batch_images(uploaded_files, target_size, wm_size, alpha_dct, alpha_iwt, wavelet, watermark_mode='random', watermark_data=None):
    """Proses batch gambar dengan ekstraksi
    
    Args:
        watermark_mode: 'random' atau 'text'
        watermark_data: numpy array untuk embedding
    Returns:
        batch_rows: list of metric dicts
        batch_preview: list of image preview dicts
        extraction_results: list of extraction result dicts
    """
    batch_rows = []
    batch_preview = []
    batch_stego_all = []  # Simpan semua stego images untuk download
    extraction_results = []

    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            img_bytes = uploaded_file.read()
            cover = preprocess_image(img_bytes, target_size)

            # Generate atau gunakan watermark
            if watermark_mode == 'text' and watermark_data is not None:
                watermark = watermark_data
                original_message = None
            else:
                # Generate watermark acak per gambar
                rng = np.random.default_rng(42 + idx)
                watermark = rng.integers(0, 2, wm_size, dtype=np.uint8)
                original_message = None

            # Embedding
            stego_dct_img = embed_dct(cover, watermark, alpha=alpha_dct)
            stego_iwt_img = embed_iwt_hh(cover, watermark, alpha=alpha_iwt, wavelet=wavelet)

            # Ekstraksi
            extracted_dct = extract_dct(stego_dct_img, alpha=alpha_dct)
            extracted_iwt = extract_iwt(stego_iwt_img, cover, watermark.shape, wavelet=wavelet)

            # Hitung akurasi ekstraksi
            acc_dct = np.mean(extracted_dct == watermark) * 100
            acc_iwt = np.mean(extracted_iwt == watermark) * 100

            # Konversi ke teks jika watermark_mode adalah 'text'
            extracted_msg_dct = None
            extracted_msg_iwt = None
            if watermark_mode == 'text':
                extracted_binary_dct = ''.join(extracted_dct.flatten().astype(str))
                extracted_binary_iwt = ''.join(extracted_iwt.flatten().astype(str))
                extracted_msg_dct = binary_to_text(extracted_binary_dct)
                extracted_msg_iwt = binary_to_text(extracted_binary_iwt)

            # Metrik
            dct_m = evaluate_all(cover, stego_dct_img)
            iwt_m = evaluate_all(cover, stego_iwt_img)

            batch_rows.append({
                'filename': uploaded_file.name,
                'method': 'DCT',
                **dct_m
            })
            batch_rows.append({
                'filename': uploaded_file.name,
                'method': 'IWT',
                **iwt_m
            })

            # Simpan hasil ekstraksi
            extraction_results.append({
                'filename': uploaded_file.name,
                'watermark_mode': watermark_mode,
                'acc_dct': acc_dct,
                'acc_iwt': acc_iwt,
                'extracted_msg_dct': extracted_msg_dct,
                'extracted_msg_iwt': extracted_msg_iwt,
                'original_message': original_message,
                'extracted_dct': extracted_dct,
                'extracted_iwt': extracted_iwt,
            })

            # Simpan stego images untuk download (semua gambar)
            filename_without_ext = os.path.splitext(uploaded_file.name)[0]
            batch_stego_all.append({
                'filename': uploaded_file.name,
                'filename_base': filename_without_ext,
                'stego_dct': stego_dct_img,
                'stego_iwt': stego_iwt_img
            })

            # Preview
            if len(batch_preview) < 6:
                batch_preview.append({
                    'name': uploaded_file.name,
                    'cover': cover,
                    'stego_dct': stego_dct_img,
                    'stego_iwt': stego_iwt_img
                })

        except Exception as e:
            st.warning(f"⚠️ Gagal memproses {uploaded_file.name}: {str(e)}")
            continue

    return batch_rows, batch_preview, extraction_results, batch_stego_all

# ============================================================================
# FUNGSI DOWNLOAD
# ============================================================================
def get_download_buffer(fig):
    """Convert matplotlib figure ke buffer PNG"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return buf

def get_image_download_buffer(img_array):
    """Convert image array ke buffer PNG"""
    img_pil = Image.fromarray(img_array)
    buf = io.BytesIO()
    img_pil.save(buf, format='PNG')
    buf.seek(0)
    return buf

def get_csv_download_buffer(df):
    """Convert dataframe ke buffer CSV"""
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return buf

def render_sidebar_param_card(title, value, subtitle=None):
    """Render kartu parameter sidebar yang ringkas dan konsisten."""
    subtitle_html = f'<span class="subvalue">{subtitle}</span>' if subtitle else ''
    st.sidebar.markdown(
        f'''
        <div class="sidebar-param-card">
            <span class="label">{title}</span>
            <span class="value">{value}</span>
            {subtitle_html}
        </div>
        ''',
        unsafe_allow_html=True
    )

def get_zip_stego_images(batch_stego_all, method='both'):
    """Buat ZIP file berisi stego images
    
    Args:
        batch_stego_all: List of stego image data
        method: 'dct', 'iwt', atau 'both'
    
    Returns:
        BytesIO buffer containing ZIP file
    """
    import zipfile
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for item in batch_stego_all:
            filename_base = item['filename_base']
            
            if method in ['dct', 'both']:
                # Add DCT stego image
                img_dct_pil = Image.fromarray(item['stego_dct'])
                img_dct_buffer = io.BytesIO()
                img_dct_pil.save(img_dct_buffer, format='PNG')
                img_dct_buffer.seek(0)
                zip_file.writestr(f"stego_dct_{filename_base}.png", img_dct_buffer.getvalue())
            
            if method in ['iwt', 'both']:
                # Add IWT stego image
                img_iwt_pil = Image.fromarray(item['stego_iwt'])
                img_iwt_buffer = io.BytesIO()
                img_iwt_pil.save(img_iwt_buffer, format='PNG')
                img_iwt_buffer.seek(0)
                zip_file.writestr(f"stego_iwt_{filename_base}.png", img_iwt_buffer.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer

# ============================================================================
# HALAMAN UTAMA (HOME)
# ============================================================================
def page_home():
    st.title("🔐 Analisis Keamanan Steganografi Citra")
    st.markdown("### DCT vs IWT - Perbandingan Kualitas dan Keamanan")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        #### 📋 Deskripsi Aplikasi
        Aplikasi ini membandingkan dua metode steganografi citra untuk menganalisis:
        - **Kualitas Visual** citra yang disisipi watermark
        - **Keamanan Steganografi** terhadap deteksi perubahan piksel

        Metrik yang digunakan:
        - MSE, PSNR, SSIM (Kualitas)
        - NPCR, UACI (Keamanan)
        """)
    

    st.markdown("""
    #### 🔬 Metode Steganografi

    **DCT (Discrete Cosine Transform)**
    - Transformasi frekuensi berbasis blok 8×8
    - Memanfaatkan koefisien DCT (3,4) dan (4,3)
    - Aturan embedding: bit 1 → c1 > c2, bit 0 → c2 > c1
    - Cocok untuk menjaga kualitas visual pada citra natural

    **IWT (Integer Wavelet Transform)**
    - Transformasi wavelet berbasis subband HH
    - Menggunakan dekomposisi Haar 1-level
    - Modifikasi langsung pada koefisien HH dengan scaling alpha
    - Efektif untuk menyembunyikan informasi di frekuensi tinggi

    #### 📊 Metrik Evaluasi

    | Metrik | Kategori | Interpretasi | Rumus |
    |--------|----------|--------------|-------|
    | **MSE** | Kualitas | Kecil ✓ | $\\frac{1}{N}\\sum(I-I')^2$ |
    | **PSNR** | Kualitas | Besar ✓ | $10\\log_{10}(\\frac{MAX^2}{MSE})$ |
    | **SSIM** | Kualitas | Besar ✓ | Kesamaan struktur (0-1) |
    | **NPCR** | Keamanan | Besar ✓ | % piksel berbeda |
    | **UACI** | Keamanan | Besar ✓ | Rata-rata perubahan intensitas |

    #### 🎯 Cara Menggunakan
    1. Pilih tab **"Batch Processing"** untuk memproses banyak gambar sekaligus
    2. Set parameter pada sidebar kiri
    3. Upload gambar dan pilihan watermark
    4. Klik tombol "Mulai Proses Batch"
    5. Download hasil yang diinginkan
    """)

    st.info("💡 **Tip:** Untuk hasil terbaik, gunakan gambar grayscale dengan ukuran minimal 512×512 piksel")

# ============================================================================
# HALAMAN BATCH PROCESSING
# ============================================================================
def page_batch_processing(target_size, wm_size, alpha_dct, alpha_iwt, wavelet):
    st.title(" Batch Processing")
    st.markdown("Analisis steganografi untuk banyak gambar sekaligus")

    # Upload multiple images
    st.markdown("### 1️⃣ Upload Gambar")
    uploaded_files = st.file_uploader(
        "Upload beberapa gambar (PNG/JPG/JPEG)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )

    if not uploaded_files:
        st.info("⬆️ Silakan upload minimal 1 gambar")
        return

    st.info(f"📁 Anda telah upload {len(uploaded_files)} gambar")

    # ===== INPUT WATERMARK =====
    st.markdown("### 2️⃣ Input Pesan / Watermark")

    watermark_choice = st.radio("Pilih sumber watermark:", 
                                ["Watermark Acak", "Upload File TXT"])

    watermark_batch = None
    watermark_mode = 'random'

    if watermark_choice == "Upload File TXT":
        txt_file = st.file_uploader("Upload file TXT", type=['txt'], key='batch_txt')

        if txt_file is not None:
            try:
                original_text = txt_file.read().decode('utf-8', errors='ignore')
                message_binary = text_to_binary(original_text)

                # Cek kapasitas
                total_capacity = wm_size[0] * wm_size[1]
                if len(message_binary) > total_capacity:
                    st.error(f"❌ Pesan terlalu panjang! Maksimal {total_capacity // 8} karakter. "
                            f"Anda memasukkan {len(original_text)} karakter.")
                else:
                    message_binary_padded = message_binary.ljust(total_capacity, '0')
                    watermark_batch = np.array([int(bit) for bit in message_binary_padded], 
                                        dtype=np.uint8).reshape(wm_size)
                    watermark_mode = 'text'

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Nama File", txt_file.name)
                    with col2:
                        st.metric("Panjang Pesan", f"{len(original_text)} karakter")
                    with col3:
                        st.metric("Panjang Biner", f"{len(message_binary)} bit")
                    with col4:
                        st.metric("Kapasitas", f"{total_capacity} bit")

                    st.success("✅ Pesan berhasil dikonversi ke watermark")

            except Exception as e:
                st.error(f"❌ Error membaca file: {str(e)}")

    if watermark_choice == "Watermark Acak" or watermark_batch is None:
        st.info("✅ Watermark acak akan digunakan untuk setiap gambar (berbeda per gambar)")

    # Proses batch
    if st.button("🚀 Mulai Proses Batch", key="process_batch", use_container_width=True):
        # Container untuk progress
        progress_container = st.container()
        extraction_results_container = st.container()
        
        with progress_container:
            with st.spinner(f"⏳ Sedang memproses {len(uploaded_files)} gambar..."):
                batch_rows, batch_preview, extraction_results, batch_stego_all = process_batch_images(
                    uploaded_files, target_size, wm_size, alpha_dct, alpha_iwt, wavelet,
                    watermark_mode=watermark_mode, watermark_data=watermark_batch
                )

        if not batch_rows:
            st.error("❌ Tidak ada gambar valid yang berhasil diproses")
            return

        batch_df = pd.DataFrame(batch_rows)
        cols = ['filename', 'method', 'MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']
        batch_df = batch_df[cols].round(4)

        st.success(f"✅ Berhasil memproses {len(batch_df) // 2} gambar!")
        
        # ===== HASIL EKSTRAKSI PESAN =====
        if watermark_mode == 'text':
            with extraction_results_container:
                st.markdown("### 🔐 Hasil Ekstraksi Pesan")
                
                # Buat tabel akurasi ekstraksi
                extraction_acc_data = []
                for result in extraction_results:
                    extraction_acc_data.append({
                        'Gambar': result['filename'],
                        'Akurasi DCT (%)': f"{result['acc_dct']:.2f}%",
                        'Akurasi IWT (%)': f"{result['acc_iwt']:.2f}%"
                    })
                
                extraction_acc_df = pd.DataFrame(extraction_acc_data)
                st.dataframe(extraction_acc_df, use_container_width=True)
                
                # Tampilkan detail ekstraksi per gambar
                st.markdown("#### Detail Ekstraksi Per Gambar")
                
                for result_idx, result in enumerate(extraction_results):
                    with st.expander(f"📄 {result['filename']} - Akurasi DCT: {result['acc_dct']:.1f}%, IWT: {result['acc_iwt']:.1f}%"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Ekstraksi DCT**")
                            st.text_area(
                                "Pesan Terekstrak",
                                value=result['extracted_msg_dct'] or "N/A",
                                height=80,
                                disabled=True,
                                key=f"batch_extracted_dct_{result_idx}"
                            )
                            st.metric("Akurasi", f"{result['acc_dct']:.2f}%")
                        
                        with col2:
                            st.markdown("**Ekstraksi IWT**")
                            st.text_area(
                                "Pesan Terekstrak",
                                value=result['extracted_msg_iwt'] or "N/A",
                                height=80,
                                disabled=True,
                                key=f"batch_extracted_iwt_{result_idx}"
                            )
                            st.metric("Akurasi", f"{result['acc_iwt']:.2f}%")
        else:
            # Untuk watermark acak, tampilkan ringkas akurasi
            with extraction_results_container:
                st.markdown("### 🔐 Hasil Ekstraksi (Watermark Acak)")
                
                extraction_acc_data = []
                for result in extraction_results:
                    extraction_acc_data.append({
                        'Gambar': result['filename'],
                        'Akurasi DCT (%)': f"{result['acc_dct']:.2f}%",
                        'Akurasi IWT (%)': f"{result['acc_iwt']:.2f}%"
                    })
                
                extraction_acc_df = pd.DataFrame(extraction_acc_data)
                st.dataframe(extraction_acc_df, use_container_width=True)
        # ===== TABEL DETAIL =====
        st.markdown("### 3️⃣ Tabel Detail Hasil")
        metrics_list = ['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']
        detail_formatted = format_detail_table(batch_df, metrics_list)
        st.dataframe(detail_formatted.round(4), use_container_width=True)

        # ===== TABEL PER GAMBAR (DCT VS IWT) =====
        st.markdown("### 4️⃣ Tabel Per Gambar (DCT vs IWT)")
        per_image_df = build_per_image_table(batch_df, ['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)'])
        st.dataframe(per_image_df.round(4), use_container_width=True)

        # ===== TABEL RINGKASAN =====
        st.markdown("### 5️⃣ Tabel Ringkasan (Rata-rata & Std Dev)")
        summary_df = batch_df.groupby('method')[['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']].agg(
            ['mean', 'std']
        ).round(4)
        st.dataframe(summary_df, use_container_width=True)

        # ===== GRAFIK PERBANDINGAN =====
        st.markdown("### 6️⃣ Grafik Perbandingan")
        fig_batch = plot_batch_metrics(batch_df)
        st.pyplot(fig_batch, use_container_width=True)

        # ===== PREVIEW CITRA =====
        st.markdown("### 7️⃣ Preview Citra (Maksimal 6 Gambar)")

        for preview_idx, preview in enumerate(batch_preview):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**Cover: {preview['name']}**")
                st.image(preview['cover'], width="stretch", clamp=True)

            with col2:
                st.markdown("**Stego DCT**")
                st.image(preview['stego_dct'], width="stretch", clamp=True)

            with col3:
                st.markdown("**Stego IWT**")
                st.image(preview['stego_iwt'], width="stretch", clamp=True)

            if preview_idx < len(batch_preview) - 1:
                st.divider()

        # ===== KESIMPULAN =====
        st.markdown("### 8️⃣ Kesimpulan Analisis")
        batch_metrics_summary = batch_df.groupby('method')[['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']].mean().round(4)
        conclusion_text = generate_conclusion(batch_metrics_summary)
        st.markdown(conclusion_text)

        # ===== DOWNLOAD =====
        st.markdown("### 📥 Download Hasil")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label=" Detail CSV",
                data=get_csv_download_buffer(batch_df),
                file_name=f"batch_detail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                label=" Ringkasan CSV",
                data=get_csv_download_buffer(summary_df.reset_index()),
                file_name=f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col3:
            st.download_button(
                label=" Grafik (PNG)",
                data=get_download_buffer(fig_batch),
                file_name=f"batch_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

        # ===== DOWNLOAD STEGO IMAGES =====
        st.markdown("#### 🖼️ Download Gambar Stego")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label=" Semua Stego DCT (ZIP)",
                data=get_zip_stego_images(batch_stego_all, method='dct'),
                file_name=f"batch_stego_dct_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )

        with col2:
            st.download_button(
                label=" Semua Stego IWT (ZIP)",
                data=get_zip_stego_images(batch_stego_all, method='iwt'),
                file_name=f"batch_stego_iwt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )

        with col3:
            st.download_button(
                label=" Semua Stego (DCT+IWT ZIP)",
                data=get_zip_stego_images(batch_stego_all, method='both'),
                file_name=f"batch_stego_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Sidebar - Parameter Configuration
    st.sidebar.title("⚙️ Parameter Penelitian")
    st.sidebar.markdown("---")

    # Fixed parameters
    target_size = (512, 512)
    wm_size = (64, 64)
    alpha_dct = 10.0
    alpha_iwt = 2.0
    wavelet = 'haar'

    # Image settings - Display Only
    st.sidebar.subheader("📐 Ukuran Citra")
    render_sidebar_param_card("Ukuran Citra", f"{target_size[0]} × {target_size[1]} px")

    # Watermark settings - Display Only
    st.sidebar.subheader("🎨 Watermark")
    render_sidebar_param_card("Ukuran Watermark", f"{wm_size[0]} × {wm_size[1]} px")

    # DCT parameters - Display Only
    st.sidebar.subheader("🔵 DCT Parameter")
    render_sidebar_param_card("Alpha DCT", f"{alpha_dct:.2f}")

    # IWT parameters - Display Only
    st.sidebar.subheader("🟣 IWT Parameter")
    render_sidebar_param_card("Alpha IWT", f"{alpha_iwt:.2f}")
    render_sidebar_param_card("Wavelet", wavelet.upper())

    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.title("📱 Navigasi")

    pages = {
        "🏠 Beranda": page_home,
        "🎞️ Batch Processing": page_batch_processing
    }

    selected_page = st.sidebar.radio("Pilih halaman:", list(pages.keys()))

    # Render selected page
    if selected_page == "🏠 Beranda":
        pages[selected_page]()
    else:
        pages[selected_page](target_size, wm_size, alpha_dct, alpha_iwt, wavelet)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Aplikasi Analisis Keamanan Steganografi DCT vs IWT**\n\n"
        "Dibuat untuk analisis skripsi perbandingan metode steganografi citra.\n\n"
    )

if __name__ == "__main__":
    main()
