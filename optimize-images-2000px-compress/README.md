# Optimisation d'images

Scripts : `optimage.py` et `imgrenamerwithfoldername.py`

- `optimage.py` : compresse toutes les images JPEG trouvées récursivement. Les
  fichiers dépassant 2000 px de largeur sont redimensionnés, puis enregistrés
  en JPEG compressé (qualité 80 par défaut).
- `imgrenamerwithfoldername.py` : renomme chaque image d'un dossier en
  préfixant le nom du dossier et en ajoutant un compteur (`MonDossier_001.jpg`).

## Prérequis communs
- Python 3
- `Pillow`

Installez la dépendance via :
```bash
pip install pillow
```

## Utilisation
Exécutez le script voulu depuis le répertoire :
```bash
python optimage.py
# ou
python imgrenamerwithfoldername.py
```
Les fichiers sont modifiés directement : conservez une sauvegarde au besoin.
