"""
generate_samples.py

Script untuk generate sample images untuk testing aplikasi.
Run: python generate_samples.py
"""

import numpy as np
import cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_sample_directory():
    """Buat folder samples jika belum ada"""
    Path("samples").mkdir(exist_ok=True)
    print("✓ Folder 'samples' siap")

def generate_gradient_image(filename, width=512, height=512):
    """Generate gradient image untuk testing"""
    img = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        img[i, :] = int(255 * (i / height))
    cv2.imwrite(f"samples/{filename}", img)
    print(f"✓ Generated: {filename}")

def generate_noise_image(filename, width=512, height=512):
    """Generate noise image untuk testing"""
    np.random.seed(42)
    img = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    cv2.imwrite(f"samples/{filename}", img)
    print(f"✓ Generated: {filename}")

def generate_pattern_image(filename, width=512, height=512):
    """Generate pattern image untuk testing"""
    img = np.zeros((height, width), dtype=np.uint8)
    # Buat grid pattern
    for i in range(0, height, 32):
        img[i:i+16, :] = 255
    for j in range(0, width, 32):
        img[:, j:j+16] = 255
    cv2.imwrite(f"samples/{filename}", img)
    print(f"✓ Generated: {filename}")

def generate_text_image(filename, text="STEGANOGRAFI", width=512, height=512):
    """Generate image dengan teks untuk testing"""
    img = Image.new('L', (width, height), color=200)
    draw = ImageDraw.Draw(img)
    
    # Drawn text (simple, tanpa font external)
    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill=50)
    
    # Tambah some shapes
    draw.rectangle([50, 50, 150, 150], outline=100, width=3)
    draw.ellipse([width-150, height-150, width-50, height-50], outline=100, width=3)
    
    img.save(f"samples/{filename}")
    print(f"✓ Generated: {filename}")

def generate_checkerboard(filename, width=512, height=512, square_size=32):
    """Generate checkerboard pattern untuk testing"""
    img = np.zeros((height, width), dtype=np.uint8)
    for i in range(0, height, square_size):
        for j in range(0, width, square_size):
            if ((i // square_size) + (j // square_size)) % 2 == 0:
                img[i:i+square_size, j:j+square_size] = 255
    cv2.imwrite(f"samples/{filename}", img)
    print(f"✓ Generated: {filename}")

def generate_sample_text_file():
    """Generate sample text file untuk watermark"""
    sample_text = """
Ini adalah pesan rahasia untuk steganografi.
Pesan ini akan disembunyikan dalam gambar.
DCT dan IWT adalah dua metode transformasi berbeda.
Keamanan steganografi adalah prioritas utama.
"""
    with open("samples/sample_message.txt", "w", encoding='utf-8') as f:
        f.write(sample_text)
    print(f"✓ Generated: sample_message.txt")

def main():
    print("=" * 60)
    print("🎨 Generate Sample Images untuk Testing Aplikasi")
    print("=" * 60)
    
    create_sample_directory()
    
    print("\nGenerate test images...")
    generate_gradient_image("sample_gradient.png")
    generate_noise_image("sample_noise.png")
    generate_pattern_image("sample_pattern.png")
    generate_text_image("sample_text.png")
    generate_checkerboard("sample_checkerboard.png")
    
    print("\nGenerate sample text file...")
    generate_sample_text_file()
    
    print("\n" + "=" * 60)
    print("✅ Semua sample images berhasil dibuat!")
    print("📁 Folder: ./samples/")
    print("\nFile yang dihasilkan:")
    print("  • sample_gradient.png")
    print("  • sample_noise.png")
    print("  • sample_pattern.png")
    print("  • sample_text.png")
    print("  • sample_checkerboard.png")
    print("  • sample_message.txt")
    print("\nGunakan file ini untuk testing aplikasi Streamlit.")
    print("=" * 60)

if __name__ == "__main__":
    main()
