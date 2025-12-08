import os
from rembg import remove
from PIL import Image

# Liste des extensions prises en charge
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# Obtenir le chemin du dossier courant
current_dir = os.path.dirname(os.path.abspath(__file__))

# Parcourir tous les fichiers du dossier
for filename in os.listdir(current_dir):
    if filename.lower().endswith(SUPPORTED_EXTENSIONS):
        input_path = os.path.join(current_dir, filename)
        output_name = os.path.splitext(filename)[0] + '_nofond.png'
        output_path = os.path.join(current_dir, output_name)

        # Charger et traiter l'image
        with Image.open(input_path) as img:
            img_no_bg = remove(img)
            img_no_bg.save(output_path)

        print(f"✅ Fond retiré pour : {filename} → {output_name}")

print("🎉 Traitement terminé pour toutes les images.")
