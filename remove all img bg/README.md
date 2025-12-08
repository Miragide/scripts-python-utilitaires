# Suppression de fond d'images

Script : `script.py`

Retire l'arrière-plan de toutes les images `.jpg`, `.jpeg` et `.png` présentes
dans le dossier. Chaque image traitée génère un nouveau fichier suffixé
`_nofond.png`.

## Prérequis
- Python 3
- `rembg`
- `Pillow`

Installation recommandée :
```bash
pip install rembg pillow
```

## Utilisation
```bash
python script.py
```
Le traitement se fait directement dans le dossier courant.
