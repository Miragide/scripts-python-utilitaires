from PIL import Image
import os

# Répertoire du script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Extensions d'image prises en charge
extensions = ('.jpg', '.jpeg', '.png')

# Lister toutes les images du dossier
image_files = sorted([
    f for f in os.listdir(current_dir)
    if f.lower().endswith(extensions)
])

if not image_files:
    print("Aucune image trouvée.")
else:
    images = []
    for file in image_files:
        img_path = os.path.join(current_dir, file)
        img = Image.open(img_path).convert("RGB")
        images.append(img)

    # Nom du PDF de sortie
    output_pdf = os.path.join(current_dir, "fusion_images.pdf")

    # Enregistrer toutes les images dans un seul PDF
    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    print(f"{len(images)} image(s) fusionnée(s) dans {output_pdf}")
