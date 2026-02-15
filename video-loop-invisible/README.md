# Vidéo loopable invisible (overlay + fondu)

Ce script crée une version **loopable** d'une vidéo en superposant le début sur la fin pendant une durée de fondu (4 s par défaut).

## Objectif

Obtenir un MP4 qui se lit en boucle sans coupure visible à la jonction **fin → début** :

- pas de ping-pong (pas d'inversion)
- pas de simple remplacement brutal
- superposition progressive du segment initial sur la fin

## Principe

Pour une vidéo de durée `T` et un fondu `d` (4 s par défaut) :

1. la vidéo complète sert de base ;
2. le segment `[0, d]` est extrait ;
3. ce segment est décalé sur `[T-d, T]` ;
4. son opacité monte progressivement de 0% à 100% ;
5. la sortie est trimmée pour que la fin corresponde au début et boucle proprement.

Si une piste audio est présente, la même logique est appliquée : fondu sortant de la fin + fondu entrant du début superposé.

## Prérequis

- Python 3.9+
- FFmpeg installé et disponible dans le `PATH` (`ffmpeg` et `ffprobe`)

## Utilisation

### Mode CLI

```bash
python3 script.py input.mp4 output.mp4
```

Options utiles :

- `--fade 4.0` : durée du fondu/superposition (en secondes)
- `--no-audio` : désactive la gestion audio
- `--crf 18` : qualité H.264
- `--preset medium` : preset x264

Exemple :

```bash
python3 script.py source.mp4 source_loop.mp4 --fade 4 --crf 18 --preset slow
```

### Mode GUI minimal (Tkinter)

Si `input` et `output` ne sont pas fournis, une fenêtre de sélection s'ouvre automatiquement.

## Vérification de la boucle

```bash
ffplay -loop 0 -i output.mp4
```

La jonction fin→début doit être imperceptible.
