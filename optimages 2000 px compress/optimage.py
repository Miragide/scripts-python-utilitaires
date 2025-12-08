#!/usr/bin/env python3
from PIL import Image
from pathlib import Path
import os

def traiter_image(chemin, quality=80):
    try:
        taille_avant = os.path.getsize(chemin) / 1024  # Ko
        
        img = Image.open(chemin)
        
        # Convertir en RGB si nécessaire (pour les PNG avec transparence)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Redimensionner si largeur > 2000px
        if img.width > 2000:
            ratio = 2000 / img.width
            nouvelle_hauteur = int(img.height * ratio)
            img = img.resize((2000, nouvelle_hauteur), Image.LANCZOS)
        
        # Sauvegarder avec compression
        img.save(chemin, 'JPEG', quality=quality, optimize=True)
        
        taille_apres = os.path.getsize(chemin) / 1024  # Ko
        reduction = ((taille_avant - taille_apres) / taille_avant) * 100
        
        print(f"✓ {chemin.name}: {taille_avant:.0f}Ko → {taille_apres:.0f}Ko (-{reduction:.0f}%)")
    except Exception as e:
        print(f"✗ {chemin}: {e}")

# Parcourir tous les dossiers
for fichier in Path('.').rglob('*'):
    if fichier.suffix.lower() in ['.jpg', '.jpeg']:
        traiter_image(fichier, quality=80)
