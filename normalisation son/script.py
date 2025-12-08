import subprocess
import os
from pathlib import Path

# Extensions supportées
EXTENSIONS = ['.mp3', '.mp4', '.wav', '.m4a', '.avi', '.mkv', '.flac']

# Trouver le premier fichier média
fichier = None
for ext in EXTENSIONS:
    fichiers = list(Path('.').glob(f'*{ext}'))
    if fichiers:
        fichier = fichiers[0]
        break

if not fichier:
    print("❌ Aucun fichier média trouvé")
    exit(1)

print(f"📁 Fichier trouvé: {fichier}")

# Nom du fichier de sortie
sortie = f"{fichier.stem}_normalized{fichier.suffix}"

# Normalisation audio avec FFMPEG (loudnorm filter)
print("🔊 Normalisation en cours...")
cmd = [
    'ffmpeg',
    '-i', str(fichier),
    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
    '-c:v', 'copy',  # Copie la vidéo sans réencodage
    '-y',  # Écrase si existe
    sortie
]

try:
    subprocess.run(cmd, check=True)
    print(f"✅ Fichier normalisé: {sortie}")
except subprocess.CalledProcessError:
    print("❌ Erreur lors de la normalisation")
except FileNotFoundError:
    print("❌ FFMPEG n'est pas installé")
