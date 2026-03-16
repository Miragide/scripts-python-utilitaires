# Fusionner des vidéos avec cross-fade

Ce script fusionne toutes les vidéos présentes dans le même dossier, triées
par ordre alphabétique, en ajoutant un fondu enchaîné (cross-fade) entre
chaque clip.

## Dépendances

```bash
pip install moviepy
```

MoviePy nécessite aussi FFmpeg installé sur la machine (`ffmpeg -version`).

## Utilisation

Placez `merge_videos.py` dans un dossier contenant vos vidéos, puis lancez :

```bash
python merge_videos.py
```

La sortie est enregistrée sous `output_merged.mp4` par défaut.

## Options

- `--output` : nom du fichier de sortie (défaut : `output_merged.mp4`)
- `--fade` : durée du cross-fade en secondes (défaut : `1.0`)
- `--fps` : FPS final (défaut : FPS du premier clip)
- `--codec` : codec vidéo ffmpeg (défaut : `libx264`)
- `--audio-codec` : codec audio ffmpeg (défaut : `aac`)
