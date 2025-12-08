# Recadrage et concaténation de vidéos

Script : `script.py`

Convertit toutes les vidéos du dossier en clips carrés 420×420 px (H.264 + AAC,
30 fps) puis les concatène séquentiellement en `output_420_concat.mp4`.

## Prérequis
- Python 3
- `ffmpeg-python`
- Binaire **FFmpeg** installé et disponible dans le PATH

Installation de la dépendance Python :
```bash
pip install ffmpeg-python
```

## Utilisation
```bash
python script.py
```
Le script crée un dossier temporaire pour les clips intermédiaires, puis assemble
tout dans `output_420_concat.mp4` au même emplacement.
