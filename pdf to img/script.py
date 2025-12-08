import fitz  # PyMuPDF
from PIL import Image
import os

# Dossier du script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Lister tous les fichiers PDF
pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]

if not pdf_files:
    print("Aucun fichier PDF trouvé.")
else:
    for pdf_file in pdf_files:
        print(f"Traitement de : {pdf_file}")
        try:
            doc = fitz.open(os.path.join(current_dir, pdf_file))
            base_name = os.path.splitext(pdf_file)[0]

            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=200)
                image_filename = f"{base_name}_page_{i + 1}.png"
                pix.save(os.path.join(current_dir, image_filename))
                print(f"  → Page {i + 1} enregistrée sous {image_filename}")

            doc.close()
        except Exception as e:
            print(f"Erreur avec {pdf_file} : {e}")

    print("Terminé.")
