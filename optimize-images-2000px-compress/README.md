# Optimisation et renommage d'images

Scripts : `optimage.py` et `imgrenamerwithfoldername.py`

- `optimage.py` : parcourt récursivement les images JPEG. Si la largeur dépasse
  2000 px, l'image est redimensionnée, puis compressée en qualité 80 par défaut.
- `imgrenamerwithfoldername.py` : renomme les images d'un dossier en préfixant
  le nom du dossier et en ajoutant un compteur (`MonDossier_001.jpg`).

## Prérequis communs
- Python 3
- `Pillow`

Installation :
```bash
pip install pillow
```

## Utilisation
Depuis ce dossier :
```bash
python optimage.py
# ou
python imgrenamerwithfoldername.py
```
**Les fichiers sont modifiés sur place** : gardez une sauvegarde avant de lancer
ces scripts sur des originaux.
