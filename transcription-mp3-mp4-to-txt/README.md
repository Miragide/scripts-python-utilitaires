# Transcription audio/vidéo → texte (Whisper)

Script : `retranscription de tous les fichiers mp3 ou mp4.py`

## Ce script
- Recherche un fichier MP3 dans le dossier courant.
- Prend le premier fichier MP3 trouvé (sinon remplacez `mp3` par `mp4` dans le script).
- Charge le modèle Whisper (`small` pour un bon équilibre vitesse/précision — sinon utilisez `tiny` ou `base` pour un résultat plus rapide).
- Transcrit l’audio.
- Sauvegarde la transcription dans un fichier texte (`*_transcription.txt`).

## Prérequis
- Python 3
- `openai-whisper` (package `whisper`)
- `ffmpeg` (obligatoire pour que Whisper puisse lire les fichiers audio/vidéo)

Installez Whisper ainsi :
```bash
pip install -U openai-whisper
```

### Installer FFmpeg (Windows)
Whisper a besoin de FFmpeg pour lire les fichiers audio. FFmpeg n’est pas installé
par défaut sous Windows, donc vous devez le télécharger et l’ajouter au `PATH`.

#### 1️⃣ Télécharger FFmpeg
Rendez-vous sur le site officiel : 👉 https://www.gyan.dev/ffmpeg/builds/  
Cliquez sur **"ffmpeg-git-full.7z"** (section **Release Builds**). Téléchargez
et extrayez le dossier `ffmpeg` sur votre ordinateur (exemple : `C:\\ffmpeg`).

#### 2️⃣ Ajouter FFmpeg au PATH (Windows)
Pour que Whisper puisse trouver FFmpeg, vous devez ajouter son chemin aux variables
d’environnement :

1. Ouvrez l’explorateur de fichiers et copiez le chemin de votre dossier FFmpeg  
   Exemple : `C:\\ffmpeg\\bin`
2. Recherchez **"Variables d’environnement"** dans la barre de recherche Windows.
3. Cliquez sur **"Modifier les variables d’environnement du système"**.
4. Dans la fenêtre qui s’ouvre, cliquez sur **"Variables d’environnement"**.
5. Dans la section **"Variables système"**, recherchez **"Path"**, sélectionnez-le et cliquez sur **"Modifier"**.
6. Cliquez sur **"Nouveau"**, collez le chemin `C:\\ffmpeg\\bin` et cliquez sur **OK**.
7. Redémarrez votre ordinateur pour appliquer les modifications.

#### 3️⃣ Vérifier l’installation de FFmpeg
Ouvrez Thonny ou une invite de commandes et tapez :
```bash
ffmpeg -version
```
Si vous voyez des informations sur FFmpeg, l’installation est réussie ! 🎉

## Utilisation
```bash
python "retranscription de tous les fichiers mp3 ou mp4.py"
```

## Choix du modèle Whisper
Whisper propose différents modèles selon vos besoins :
- `tiny` → Très rapide, mais moins précis.
- `base` → Bonne précision, rapide.
- `small` → Meilleur équilibre vitesse/précision.
- `medium` → Précision élevée, un peu plus lent.
- `large` → Très précis, mais plus long à traiter.
