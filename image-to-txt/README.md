# OCR d'images → CSV

Script : `script.py`

Parcourt le dossier courant, détecte les images (`.png`, `.jpg`, `.jpeg`, `.bmp`,
`.tiff`, `.webp`) et effectue une reconnaissance de texte (EasyOCR en français).
Le résultat est enregistré dans `resultats_textes_easyocr.csv`.

## Prérequis
- Python 3
- `easyocr`
- `pandas`
- `pillow` (installé en dépendance d'EasyOCR)

Installation rapide :
```bash
pip install easyocr pandas pillow
```

## Utilisation
```bash
python script.py
```
Chaque ligne du CSV contient le nom de l'image et le texte détecté, concaténé
sur une seule colonne.
