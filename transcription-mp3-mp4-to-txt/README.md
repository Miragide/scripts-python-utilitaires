# Transcription audio/vidéo → texte

Script : `retranscription de tous les fichiers mp3 ou mp4.py`

Détecte tous les fichiers audio/vidéo (`.mp4`, `.mp3`, `.m4a`) du dossier et les
transcrit en texte avec le modèle Whisper. Chaque transcription est enregistrée
dans un fichier `*_transcription.txt`.

## Prérequis
- Python 3
- `openai-whisper` (package `whisper`)

Installez-le ainsi :
```bash
pip install -U openai-whisper
```

## Utilisation
```bash
python "retranscription de tous les fichiers mp3 ou mp4.py"
```
Le modèle téléchargé peut être volumineux (`small` par défaut). Adaptez le nom
du modèle dans le script si besoin (`tiny`, `base`, etc.).
