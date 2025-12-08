# MP4 vers MP3

Script : `script.py`

Convertit tous les fichiers `.mp4` du dossier courant en fichiers audio `.mp3`
de même nom.

## Prérequis
- Python 3
- `ffmpeg-python` (wrapper)
- Binaire **FFmpeg** présent dans le PATH

Installation rapide :
```bash
pip install ffmpeg-python
# Installez FFmpeg pour votre OS puis ajoutez-le au PATH
```

## Utilisation
```bash
python script.py
```
Chaque vidéo génère un fichier MP3 correspondant dans le même dossier.
