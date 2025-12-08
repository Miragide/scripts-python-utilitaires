# OCR Images → Texte

Script : `script.py`

Extrait le texte de toutes les images du dossier à l'aide d'EasyOCR (langue
française) et exporte les résultats dans `resultats_textes_easyocr.csv`.

## Prérequis
- Python 3
- `easyocr`
- `pandas`
- `Pillow`

Installez-les par exemple via :
```bash
pip install easyocr pandas pillow
```

## Utilisation
```bash
python script.py
```
Le CSV généré contient le nom de chaque image et le texte détecté.
