# Concaténation et recadrage vidéo

Script : `script.py`

Convertit toutes les vidéos du dossier en clips carrés 420×420 px (H.264/AAC,
30 fps) puis les concatène sans ré-encodage final dans `output_420_concat.mp4`.

## Prérequis
- Python 3
- `ffmpeg-python`
- Binaire **FFmpeg** installé et accessible dans le PATH

Installation suggérée :
```bash
pip install ffmpeg-python
# Installez ensuite FFmpeg pour votre plateforme
```

## Utilisation
```bash
python script.py
```
Le script crée un dossier temporaire pour les conversions intermédiaires puis
produit la vidéo finale dans le répertoire courant.
