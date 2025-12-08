#!/usr/bin/env python3
from pathlib import Path

def renommer_images():
    # Parcourir tous les fichiers images
    dossiers = {}
    
    # Grouper les images par dossier parent
    for fichier in Path('.').rglob('*'):
        if fichier.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            dossier_parent = fichier.parent.name
            
            if dossier_parent not in dossiers:
                dossiers[dossier_parent] = []
            dossiers[dossier_parent].append(fichier)
    
    # Renommer les images de chaque dossier
    for dossier, fichiers in dossiers.items():
        fichiers.sort()  # Trier par ordre alphabétique
        
        for index, fichier in enumerate(fichiers, start=1):
            extension = fichier.suffix
            nouveau_nom = f"{dossier}_{index:03d}{extension}"
            nouveau_chemin = fichier.parent / nouveau_nom
            
            # Éviter d'écraser un fichier existant
            if nouveau_chemin.exists() and nouveau_chemin != fichier:
                print(f"⚠ Existe déjà: {nouveau_chemin}")
                continue
            
            fichier.rename(nouveau_chemin)
            print(f"✓ {fichier.name} → {nouveau_nom}")

if __name__ == "__main__":
    renommer_images()
