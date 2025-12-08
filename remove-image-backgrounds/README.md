# Suppression de fond d'images

Script : `script.py`

Supprime l'arrière-plan des images (`.jpg`, `.jpeg`, `.png`) présentes dans le
dossier et sauvegarde une version PNG avec suffixe `_nofond.png`.

## Prérequis
- Python 3
- `rembg`
- `Pillow`

Installation :
```bash
pip install rembg pillow
```

## Utilisation
```bash
python script.py
```
Chaque image traitée génère un nouveau fichier sans fond dans le même dossier.
