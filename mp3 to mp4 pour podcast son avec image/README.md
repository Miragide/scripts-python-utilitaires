# MP3 vers MP4 (podcast audio + image)

Ce script crée rapidement une vidéo MP4 à partir d'un fichier audio (podcast, extrait musical, etc.) et d'une image fixe pour l'illustration.

## Prérequis
- Python 3.8 ou plus récent.
- [FFmpeg](https://ffmpeg.org/download.html) installé et accessible dans le `PATH`.
- Un fichier audio et une image dans le même dossier que `script.py`.

## Formats pris en charge
- **Audio** : .mp3, .wav, .m4a, .aac, .ogg, .flac, .wma
- **Image** : .jpg, .jpeg, .png, .bmp, .gif, .webp, .tiff

## Utilisation
1. Placez un fichier audio et une image dans le répertoire du script.
2. Exécutez :
   ```bash
   python3 script.py
   ```
3. Confirmez l'écrasement si un fichier de sortie existe déjà.

Le script :
- vérifie la présence de FFmpeg et la validité des fichiers,
- reprend la première image et le premier fichier audio trouvés dans le dossier,
- crée une vidéo `output_<nom_audio>.mp4` en copiant l'audio sans ré-encodage et en appliquant l'image comme visuel fixe.

## Notes
- La durée de la vidéo est automatiquement calée sur celle de l'audio.
- L'encodage vidéo utilise `libx264` avec un preset « stillimage » optimisé pour les images fixes.
- Une opération peut durer plusieurs minutes selon la longueur de l'audio et la puissance de la machine.
