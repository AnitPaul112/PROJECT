from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

# ✅ Tesseract er path (edit na korle cholbe jodi default install)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📄 PDF file name (same folder e thakte hobe)
pdf_path = r"D:\10 minute\HSC26-Bangla1st-Paper (1).pdf"

# 📸 Convert PDF to image (each page)
pages = convert_from_path(pdf_path, dpi=300)

# 📝 OCR result store korbe
full_text = ""

# 🔁 Loop each page
for i, page in enumerate(pages):
    image_path = f"page_{i+1}.png"
    page.save(image_path, "PNG")  # Save image

    # 🧠 OCR from image (Bangla)
    text = pytesseract.image_to_string(Image.open(image_path), lang="ben")
    full_text += f"\n--- Page {i+1} ---\n{text}"

    os.remove(image_path)  # Optional: delete image after use

# 💾 Save full text to output.txt
with open("bangla_output.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("✅ Bangla PDF OCR complete! Check bangla_output.txt")
