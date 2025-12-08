# Conversion MP4 → MP3

Script : `script.py`

Cherche tous les fichiers `.mp4` dans le dossier courant, puis extrait la piste
audio en MP3 pour chacun (`nom.mp3`).

## Prérequis
- Python 3
- `ffmpeg-python`
- Binaire **FFmpeg** disponible dans le PATH

Installation de la dépendance Python :
```bash
pip install ffmpeg-python
```

## Utilisation
```bash
python script.py
```
Chaque MP3 est généré à côté de la vidéo source. Les erreurs FFmpeg sont
rapportées dans la console.
