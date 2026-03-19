# MP3 vers MP4 (podcast audio + image)

Ce script crée une vidéo MP4 720p à partir de la première image et du premier fichier audio trouvés dans un dossier.

## Prérequis
- Python 3.10 ou plus récent.
- [FFmpeg](https://ffmpeg.org/download.html) installé et accessible dans le `PATH`.
- [Pillow](https://pypi.org/project/Pillow/) installé (`pip install pillow`).

## Formats pris en charge
- **Images** : `.jpeg`, `.jpg`, `.png`, `.bmp`, `.webp`, `.tiff`, `.tif`
- **Audio** : `.mp3`, `.wav`, `.aac`, `.ogg`, `.flac`, `.m4a`

## Utilisation
```bash
python3 script.py
python3 script.py /chemin/du/dossier
```

Le script :
- sélectionne la première image et le premier audio par ordre alphabétique ;
- redimensionne l'image en 1280×720 (mode cover avec crop centré) ;
- lit la durée exacte de l'audio avec `ffprobe` ;
- génère un MP4 H.264/AAC (`output_video.mp4`) optimisé pour l'upload YouTube.

## Correctif principal (écran noir)
Pour éviter les cas où la vidéo sortait noire :
- la durée est imposée avec `-t <durée_audio>` (plutôt que `-shortest`) ;
- la source image est injectée à `25 fps` pour garantir l'encodage d'au moins une frame visible.
