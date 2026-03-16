# Transcription musique → CSV (tranches de 4 secondes)

Ce script transcrit une chanson MP3 avec **Whisper** puis crée un tableau CSV qui indique les paroles prononcées à chaque tranche temporelle.

## Pourquoi des tranches de 4 secondes ?

Objectif : générer ensuite des clips vidéo de **5 secondes** avec **1 seconde de transition (fondu)** entre les clips, sans décalage image/paroles.

La fenêtre de paroles doit alors couvrir uniquement la partie "nette" du clip :

```text
fenêtre CSV = durée clip - durée fondu
      4s    =     5s      -     1s
```

C'est pour cela que `--window` est réglé par défaut à `4.0` dans le script.

Règle générale :
- fondu 1s + clips 5s → `--window 4`
- fondu 2s + clips 5s → `--window 3`

## Script

Fichier : `song_transcribe.py`

Fonctionnement :
1. cherche le premier fichier `.mp3` dans le dossier ciblé ;
2. transcrit avec Whisper (timestamps par mot quand disponibles) ;
3. regroupe les mots par fenêtres fixes (4 s par défaut) ;
4. génère un CSV avec les colonnes :
   - `Timecode`
   - `Contenu`
   - `Durée (s)`

## Installation

```bash
pip install openai-whisper mutagen
```

Whisper nécessite aussi `ffmpeg` installé sur la machine.

## Utilisation

Depuis le dossier contenant le MP3 (ou en utilisant `--dir`) :

```bash
python song_transcribe.py
```

Exemples :

```bash
# Valeurs par défaut : modèle small, fenêtres de 4s
python song_transcribe.py

# Changer la taille de fenêtre
python song_transcribe.py --window 3

# Changer le modèle et le fichier de sortie
python song_transcribe.py --model medium --output paroles.csv

# Chercher le mp3 dans un autre dossier
python song_transcribe.py --dir /chemin/vers/dossier
```

## Sortie

Le script produit `transcription.csv` (par défaut), prêt pour piloter une génération de clips segmentés.
