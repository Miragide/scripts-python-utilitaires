# Normalisation son

Script Python utilisant FFmpeg pour normaliser le volume d'un fichier audio ou vidéo avec le filtre `loudnorm`.

## Fonctionnement
- Le script recherche automatiquement le premier fichier présent dans le dossier courant avec l'une des extensions prises en charge (`.mp3`, `.mp4`, `.wav`, `.m4a`, `.avi`, `.mkv`, `.flac`).
- FFmpeg est exécuté avec le filtre `loudnorm` (I = -16 LUFS, TP = -1.5 dB, LRA = 11) afin d'obtenir un volume homogène.
- La piste vidéo est copiée sans réencodage lorsque c'est pertinent grâce à l'option `-c:v copy`.
- Le fichier normalisé est enregistré dans le même dossier avec le suffixe `_normalized` avant l'extension d'origine.

## Prérequis
- Python 3.8 ou plus.
- FFmpeg installé et accessible dans le PATH (`ffmpeg -version`).

## Utilisation
1. Placez le script et le fichier média à normaliser dans le même dossier.
2. Exécutez la commande suivante :
   ```bash
   python3 script.py
   ```
3. Surveillez la sortie terminal pour vérifier qu'un fichier a été détecté et que la normalisation s'est bien déroulée.
4. Récupérez le fichier généré : `NOMFICHIER_normalized.EXT`.

## Notes
- Si aucun fichier compatible n'est trouvé, le script s'arrête avec un message d'erreur explicite.
- En cas d'absence d'FFmpeg ou d'erreur de traitement, un message d'échec est affiché.
