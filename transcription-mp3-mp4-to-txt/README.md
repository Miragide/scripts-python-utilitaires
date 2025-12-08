# Transcription audio/vidéo → texte

Script : `retranscription de tous les fichiers mp3 ou mp4.py`

Détecte les fichiers `.mp4`, `.mp3` et `.m4a` dans le dossier, charge le modèle
Whisper (`small` par défaut) puis crée pour chaque média un fichier
`*_transcription.txt` contenant le texte.

## Prérequis
- Python 3
- `openai-whisper` (package `whisper`)

Installation :
```bash
pip install -U openai-whisper
```

## Utilisation
```bash
python "retranscription de tous les fichiers mp3 ou mp4.py"
```
Le modèle `small` offre un bon compromis précision/vitesse. Modifiez la ligne
`model = whisper.load_model("small")` dans le script si vous préférez `tiny` ou
`base`.
