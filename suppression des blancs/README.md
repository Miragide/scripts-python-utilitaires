# Suppression des blancs dans une vidéo

Ce dossier contient un script Python qui supprime automatiquement les passages silencieux d'une vidéo à l'aide de MoviePy. Il détecte les segments où le niveau sonore passe en dessous d'un seuil pendant une durée minimale, puis recolle les parties utiles en laissant un léger temps de respiration avant et après chaque coupe.

## Pré-requis
- Python 3.8 ou plus récent
- [MoviePy](https://zulko.github.io/moviepy/) et [NumPy](https://numpy.org/)

Installe les dépendances dans ton environnement (idéalement un virtualenv) :

```bash
pip install moviepy numpy
```

## Utilisation
1. Place ta vidéo source dans le même dossier que le script et renomme-la en `input.mp4` (ou modifie `INPUT_VIDEO` dans le script).
2. Ajuste au besoin les paramètres en haut de `script.py` :
   - `SILENCE_THRESHOLD` : seuil d'amplitude en dessous duquel le son est considéré comme silencieux (0 à 1).
   - `MIN_SILENCE_DURATION` : durée minimale (en secondes) d'un silence pour qu'il soit coupé.
   - `SAFE_MARGIN` : marge (en secondes) conservée avant et après chaque silence pour éviter les coupes trop brutales.
3. Exécute le script :

```bash
python script.py
```

Le fichier final sera exporté sous le nom `output_cut.mp4` dans le même dossier.

## Notes
- Le script charge la piste audio, calcule l'amplitude maximale par frame audio, détecte les plages silencieuses, puis concatène les sous-clips non silencieux.
- Si tu utilises un autre format d'entrée ou de sortie, adapte `INPUT_VIDEO` et `OUTPUT_VIDEO` dans le script.
