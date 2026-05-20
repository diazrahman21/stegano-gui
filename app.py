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
def embed_iwt_ll(cover_img, watermark_bits, alpha=2.0, wavelet='haar'):
    """Embedding watermark pada subband LL menggunakan IWT"""
    cover_int = cover_img.astype(np.int16)
    LL, (LH, HL, HH) = pywt.dwt2(cover_int, wavelet)

    wm_ll = cv2.resize(watermark_bits.astype(np.float32), 
                       (LL.shape[1], LL.shape[0]), 
                       interpolation=cv2.INTER_NEAREST)
    wm_sign = (wm_ll * 2.0) - 1.0

    LL_embedded = LL + alpha * wm_sign
    stego_recon = pywt.idwt2((LL_embedded, (LH, HL, HH)), wavelet)
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
def extract_iwt(stego_img, wavelet='haar'):
    """Ekstraksi watermark dari stego IWT"""
    stego_int = stego_img.astype(np.int16)
    LL, _ = pywt.dwt2(stego_int, wavelet)

    LL_min, LL_max = LL.min(), LL.max()
    LL_norm = (LL - LL_min) / (LL_max - LL_min + 1e-12)
    extracted = (LL_norm > 0.5).astype(np.uint8)
    extracted_resized = cv2.resize(extracted.astype(np.float32), (64, 64), 
                                   interpolation=cv2.INTER_NEAREST)

    return extracted_resized.astype(np.uint8)

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
def process_batch_images(uploaded_files, target_size, wm_size, alpha_dct, alpha_iwt, wavelet):
    """Proses batch gambar"""
    batch_rows = []
    batch_preview = []

    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            img_bytes = uploaded_file.read()
            cover = preprocess_image(img_bytes, target_size)

            # Generate watermark per gambar
            rng = np.random.default_rng(42 + idx)
            watermark = rng.integers(0, 2, wm_size, dtype=np.uint8)

            # Embedding
            stego_dct_img = embed_dct(cover, watermark, alpha=alpha_dct)
            stego_iwt_img = embed_iwt_ll(cover, watermark, alpha=alpha_iwt, wavelet=wavelet)

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

    return batch_rows, batch_preview

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

    with col2:
        st.image("https://via.placeholder.com/300x200?text=Steganografi", use_column_width=True)

    st.markdown("---")

    st.markdown("""
    #### 🔬 Metode Steganografi

    **DCT (Discrete Cosine Transform)**
    - Transformasi frekuensi berbasis blok 8×8
    - Memanfaatkan koefisien DCT (3,4) dan (4,3)
    - Aturan embedding: bit 1 → c1 > c2, bit 0 → c2 > c1
    - Cocok untuk menjaga kualitas visual pada citra natural

    **IWT (Integer Wavelet Transform)**
    - Transformasi wavelet berbasis subband LL
    - Menggunakan dekomposisi Haar 1-level
    - Modifikasi langsung pada koefisien LL dengan scaling alpha
    - Efektif untuk menyembunyikan informasi di frekuensi rendah

    #### 📊 Metrik Evaluasi

    | Metrik | Kategori | Interpretasi | Rumus |
    |--------|----------|--------------|-------|
    | **MSE** | Kualitas | Kecil ✓ | $\\frac{1}{N}\\sum(I-I')^2$ |
    | **PSNR** | Kualitas | Besar ✓ | $10\\log_{10}(\\frac{MAX^2}{MSE})$ |
    | **SSIM** | Kualitas | Besar ✓ | Kesamaan struktur (0-1) |
    | **NPCR** | Keamanan | Besar ✓ | % piksel berbeda |
    | **UACI** | Keamanan | Besar ✓ | Rata-rata perubahan intensitas |

    #### 🎯 Cara Menggunakan
    1. Pilih tab **"Single Image"** untuk proses satu gambar
    2. Atau pilih tab **"Batch Processing"** untuk proses banyak gambar
    3. Set parameter pada sidebar kiri
    4. Upload gambar dan pilihan watermark
    5. Klik tombol "Mulai Proses Steganografi"
    6. Download hasil yang diinginkan
    """)

    st.info("💡 **Tip:** Untuk hasil terbaik, gunakan gambar grayscale dengan ukuran minimal 512×512 piksel")

# ============================================================================
# HALAMAN SINGLE IMAGE
# ============================================================================
def page_single_image(target_size, wm_size, alpha_dct, alpha_iwt, wavelet):
    st.title("📸 Single Image Processing")
    st.markdown("Analisis steganografi untuk satu gambar")

    # Upload gambar
    st.markdown("### 1️⃣ Input Citra")
    uploaded_image = st.file_uploader("Upload gambar (PNG/JPG/JPEG)", type=['png', 'jpg', 'jpeg'])

    if uploaded_image is None:
        st.info("⬆️ Silakan upload gambar terlebih dahulu")
        return

    # Preprocess citra
    try:
        cover_gray = preprocess_image(uploaded_image.getvalue(), target_size)
    except Exception as e:
        st.error(f"❌ Error preprocessing citra: {str(e)}")
        return

    # Info citra
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nama File", uploaded_image.name)
    with col2:
        st.metric("Ukuran Citra", f"{cover_gray.shape[0]}×{cover_gray.shape[1]}")
    with col3:
        st.metric("Ukuran File", f"{uploaded_image.size / 1024:.2f} KB")

    # Preview citra asli
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Preview Citra Asli")
        st.image(cover_gray, use_column_width=True, clamp=True)
    with col2:
        st.subheader("Histogram Citra Asli")
        fig_hist, ax = plt.subplots(figsize=(8, 4))
        ax.hist(cover_gray.ravel(), bins=256, range=(0, 255), color='steelblue', alpha=0.8)
        ax.set_xlabel('Intensitas Piksel')
        ax.set_ylabel('Frekuensi')
        ax.grid(alpha=0.3)
        st.pyplot(fig_hist, use_container_width=True)

    # ===== INPUT WATERMARK =====
    st.markdown("### 2️⃣ Input Pesan / Watermark")

    watermark_choice = st.radio("Pilih sumber watermark:", 
                                ["Watermark Acak", "Upload File TXT"])

    use_text_message = False
    original_text = None
    watermark = None

    if watermark_choice == "Upload File TXT":
        txt_file = st.file_uploader("Upload file TXT", type=['txt'])

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
                    watermark = np.array([int(bit) for bit in message_binary_padded], 
                                        dtype=np.uint8).reshape(wm_size)
                    use_text_message = True

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

    if watermark_choice == "Watermark Acak" or watermark is None:
        if watermark is None:
            np.random.seed(42)
            watermark = np.random.randint(0, 2, wm_size, dtype=np.uint8)

        st.subheader("Contoh Watermark Acak (5×5)")
        st.text(f"{watermark[:5, :5]}")

    # ===== TOMBOL PROSES =====
    if st.button("🚀 Mulai Proses Steganografi", key="process_single", use_container_width=True):
        with st.spinner("⏳ Sedang memproses... Mohon tunggu"):
            # Embedding
            stego_dct = embed_dct(cover_gray, watermark, alpha=alpha_dct)
            stego_iwt = embed_iwt_ll(cover_gray, watermark, alpha=alpha_iwt, wavelet=wavelet)

            # Ekstraksi
            extracted_dct = extract_dct(stego_dct, alpha=alpha_dct)
            extracted_iwt = extract_iwt(stego_iwt, wavelet=wavelet)

            # Metrik
            metrics_dct = evaluate_all(cover_gray, stego_dct)
            metrics_iwt = evaluate_all(cover_gray, stego_iwt)
            df_metrics = pd.DataFrame([metrics_dct, metrics_iwt], index=['DCT', 'IWT']).round(4)

        st.success("✅ Proses selesai!")

        # ===== OUTPUT CITRA =====
        st.markdown("### 3️⃣ Output Citra")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Citra Asli")
            st.image(cover_gray, use_column_width=True, clamp=True)

        with col2:
            st.subheader("Stego DCT")
            st.image(stego_dct, use_column_width=True, clamp=True)

        with col3:
            st.subheader("Stego IWT")
            st.image(stego_iwt, use_column_width=True, clamp=True)

        # Histogram
        st.markdown("### 📊 Histogram Citra")
        fig_hist_compare = plot_images_and_histograms(cover_gray, stego_dct, stego_iwt)
        st.pyplot(fig_hist_compare, use_container_width=True)

        # ===== OUTPUT EKSTRAKSI PESAN =====
        if use_text_message:
            st.markdown("### 4️⃣ Output Ekstraksi Pesan")

            extracted_binary_dct = ''.join(extracted_dct.flatten().astype(str))
            extracted_binary_iwt = ''.join(extracted_iwt.flatten().astype(str))

            reconstructed_msg_dct = binary_to_text(extracted_binary_dct)
            reconstructed_msg_iwt = binary_to_text(extracted_binary_iwt)

            acc_dct = np.mean(extracted_dct == watermark) * 100
            acc_iwt = np.mean(extracted_iwt == watermark) * 100

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Pesan Asli**")
                st.text_area("", value=original_text, height=100, disabled=True)

            with col2:
                st.markdown("**Ekstraksi DCT**")
                st.text_area("", value=reconstructed_msg_dct, height=100, disabled=True)
                st.metric("Akurasi DCT", f"{acc_dct:.2f}%")

            with col3:
                st.markdown("**Ekstraksi IWT**")
                st.text_area("", value=reconstructed_msg_iwt, height=100, disabled=True)
                st.metric("Akurasi IWT", f"{acc_iwt:.2f}%")

        # ===== TABEL METRIK =====
        st.markdown("### 5️⃣ Tabel Metrik Perbandingan")
        st.dataframe(df_metrics, use_container_width=True)

        # ===== GRAFIK PERBANDINGAN =====
        st.markdown("### 6️⃣ Grafik Perbandingan")
        fig_compare = plot_metrics_comparison(df_metrics)
        st.pyplot(fig_compare, use_container_width=True)

        # ===== KESIMPULAN =====
        st.markdown("### 7️⃣ Kesimpulan Analisis")
        conclusion_text = generate_conclusion(df_metrics)
        st.markdown(conclusion_text)

        # ===== DOWNLOAD =====
        st.markdown("### 📥 Download Hasil")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="📥 Stego DCT (PNG)",
                data=get_image_download_buffer(stego_dct),
                file_name=f"stego_dct_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

        with col2:
            st.download_button(
                label="📥 Stego IWT (PNG)",
                data=get_image_download_buffer(stego_iwt),
                file_name=f"stego_iwt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

        with col3:
            st.download_button(
                label="📥 Histogram (PNG)",
                data=get_download_buffer(fig_hist_compare),
                file_name=f"histogram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="📥 Grafik Metrik (PNG)",
                data=get_download_buffer(fig_compare),
                file_name=f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

        with col2:
            st.download_button(
                label="📥 Hasil CSV",
                data=get_csv_download_buffer(df_metrics.reset_index()),
                file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col3:
            st.write("")

# ============================================================================
# HALAMAN BATCH PROCESSING
# ============================================================================
def page_batch_processing(target_size, wm_size, alpha_dct, alpha_iwt, wavelet):
    st.title("🎞️ Batch Processing")
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

    # Proses batch
    if st.button("🚀 Mulai Proses Batch", key="process_batch", use_container_width=True):
        with st.spinner(f"⏳ Sedang memproses {len(uploaded_files)} gambar..."):
            batch_rows, batch_preview = process_batch_images(
                uploaded_files, target_size, wm_size, alpha_dct, alpha_iwt, wavelet
            )

        if not batch_rows:
            st.error("❌ Tidak ada gambar valid yang berhasil diproses")
            return

        batch_df = pd.DataFrame(batch_rows)
        cols = ['filename', 'method', 'MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']
        batch_df = batch_df[cols].round(4)

        st.success(f"✅ Berhasil memproses {len(batch_df) // 2} gambar!")

        # ===== TABEL DETAIL =====
        st.markdown("### 2️⃣ Tabel Detail Hasil")
        metrics_list = ['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']
        detail_formatted = format_detail_table(batch_df, metrics_list)
        st.dataframe(detail_formatted.round(4), use_container_width=True)

        # ===== TABEL PER GAMBAR (DCT VS IWT) =====
        st.markdown("### 3️⃣ Tabel Per Gambar (DCT vs IWT)")
        per_image_df = build_per_image_table(batch_df, ['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)'])
        st.dataframe(per_image_df.round(4), use_container_width=True)

        # ===== TABEL RINGKASAN =====
        st.markdown("### 4️⃣ Tabel Ringkasan (Rata-rata & Std Dev)")
        summary_df = batch_df.groupby('method')[['MSE', 'PSNR (dB)', 'SSIM', 'NPCR (%)', 'UACI (%)']].agg(
            ['mean', 'std']
        ).round(4)
        st.dataframe(summary_df, use_container_width=True)

        # ===== GRAFIK PERBANDINGAN =====
        st.markdown("### 5️⃣ Grafik Perbandingan")
        fig_batch = plot_batch_metrics(batch_df)
        st.pyplot(fig_batch, use_container_width=True)

        # ===== PREVIEW CITRA =====
        st.markdown("### 6️⃣ Preview Citra (Maksimal 6 Gambar)")

        for preview_idx, preview in enumerate(batch_preview):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**Cover: {preview['name']}**")
                st.image(preview['cover'], use_column_width=True, clamp=True)

            with col2:
                st.markdown("**Stego DCT**")
                st.image(preview['stego_dct'], use_column_width=True, clamp=True)

            with col3:
                st.markdown("**Stego IWT**")
                st.image(preview['stego_iwt'], use_column_width=True, clamp=True)

            if preview_idx < len(batch_preview) - 1:
                st.divider()

        # ===== DOWNLOAD =====
        st.markdown("### 📥 Download Hasil")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="📥 Detail CSV",
                data=get_csv_download_buffer(batch_df),
                file_name=f"batch_detail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                label="📥 Ringkasan CSV",
                data=get_csv_download_buffer(summary_df.reset_index()),
                file_name=f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col3:
            st.download_button(
                label="📥 Grafik (PNG)",
                data=get_download_buffer(fig_batch),
                file_name=f"batch_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Sidebar - Parameter Configuration
    st.sidebar.title("⚙️ Konfigurasi Parameter")
    st.sidebar.markdown("---")

    # Image settings
    st.sidebar.subheader("📐 Ukuran Citra")
    target_size_input = st.sidebar.number_input(
        "Ukuran target (px):",
        value=512,
        min_value=256,
        max_value=1024,
        step=256
    )
    target_size = (target_size_input, target_size_input)

    # Watermark settings
    st.sidebar.subheader("🎨 Watermark")
    wm_size_input = st.sidebar.number_input(
        "Ukuran watermark (px):",
        value=64,
        min_value=32,
        max_value=128,
        step=32
    )
    wm_size = (wm_size_input, wm_size_input)

    # DCT parameters
    st.sidebar.subheader("DCT Parameter")
    alpha_dct = st.sidebar.slider(
        "Alpha DCT:",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=1.0
    )

    # IWT parameters
    st.sidebar.subheader("IWT Parameter")
    alpha_iwt = st.sidebar.slider(
        "Alpha IWT:",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1
    )

    wavelet = st.sidebar.selectbox(
        "Wavelet IWT:",
        options=['haar', 'db2', 'db4']
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tips Parameter:**\n\n"
        "• **Alpha DCT** lebih besar = watermark lebih kuat tapi distorsi lebih besar\n"
        "• **Alpha IWT** lebih besar = watermark lebih terlihat\n"
        "• **Haar** wavelet paling cepat, db4 lebih presisi"
    )

    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.title("📱 Navigasi")

    pages = {
        "🏠 Beranda": page_home,
        "📸 Single Image": page_single_image,
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
        "© 2025 - All Rights Reserved"
    )

if __name__ == "__main__":
    main()
