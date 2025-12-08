import os
import unicodedata
import re

# Vérifie si un fichier est une image
def is_image(filename):
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
    return os.path.splitext(filename.lower())[1] in extensions

# Transforme un texte en nom optimisé pour le web
def slugify(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    root = os.getcwd()

    # Récupérer le premier dossier à la racine
    folders = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]
    if not folders:
        print("Aucun dossier trouvé à la racine.")
        return

    main_folder = os.path.join(root, folders[0])
    print(f"Dossier racine sélectionné : {main_folder}")

    # Parcours de tous les sous-dossiers
    for current_path, subdirs, files in os.walk(main_folder):
        
        # Récupère la liste des dossiers depuis le dossier principal jusqu'à l’actuel
        relative_path = os.path.relpath(current_path, main_folder)
        if relative_path == ".":
            folder_chain = [os.path.basename(main_folder)]
        else:
            folder_chain = [os.path.basename(main_folder)] + relative_path.split(os.sep)

        # Slug pour chaque dossier
        folder_chain_slug = [slugify(f) for f in folder_chain]

        # Chaîne cumulée
        prefix = "_".join(folder_chain_slug)

        for file in files:
            if is_image(file):
                old_path = os.path.join(current_path, file)

                # Nettoyer le nom d'origine
                name, ext = os.path.splitext(file)
                name_slug = slugify(name)

                # Nouveau nom complet
                new_name = f"{prefix}_{name_slug}{ext.lower()}"
                new_path = os.path.join(current_path, new_name)

                # Évite d’écraser un fichier existant
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renommé : {file} → {new_name}")
                else:
                    print(f"⚠️ Fichier déjà existant : {new_name}")

if __name__ == "__main__":
    main()
