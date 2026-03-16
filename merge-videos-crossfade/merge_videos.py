#!/usr/bin/env python3
"""
merge_videos.py
---------------
Fusionne toutes les vidéos situées dans le même dossier que ce script,
dans l'ordre alphabétique, avec un fondu enchaîné (cross-fade) d'1 seconde
entre chaque clip.

Dépendances :
    pip install moviepy
    # moviepy nécessite aussi ffmpeg : https://ffmpeg.org/download.html
    # Vérifier que ffmpeg est bien dans le PATH : ffmpeg -version

Utilisation :
    Placez ce script dans le dossier contenant vos vidéos, puis lancez :
        python merge_videos.py
    La vidéo fusionnée sera enregistrée dans le même dossier sous le nom
    "output_merged.mp4" (ou le nom de votre choix via --output).

Options :
    --output    Nom du fichier de sortie (défaut : output_merged.mp4)
    --fade      Durée du cross-fade en secondes (défaut : 1.0)
    --fps       Images par seconde de la vidéo finale (défaut : auto)
"""

import argparse
import os
import sys
import textwrap

# ---------------------------------------------------------------------------
# Vérification précoce de moviepy avant tout import lourd
# Supporte moviepy v1.x (moviepy.editor) ET v2.x (moviepy directement)
# ---------------------------------------------------------------------------
try:
    # moviepy v2.x
    from moviepy import CompositeVideoClip, VideoFileClip

    MOVIEPY_VERSION = 2
except ImportError:
    try:
        # moviepy v1.x
        from moviepy.editor import CompositeVideoClip, VideoFileClip

        MOVIEPY_VERSION = 1
    except ImportError:
        print(
            "\n[ERREUR] moviepy n'est pas installé ou est corrompu.\n"
            "Lancez : pip install moviepy\n"
            "Assurez-vous aussi que ffmpeg est installé et dans votre PATH.\n"
            "  macOS  : brew install ffmpeg\n"
            "  Ubuntu : sudo apt install ffmpeg\n"
            "  Windows: https://ffmpeg.org/download.html\n"
        )
        sys.exit(1)

# ---------------------------------------------------------------------------
# Extensions vidéo reconnues
# ---------------------------------------------------------------------------
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_videos(directory: str) -> list[str]:
    """Retourne les fichiers vidéo du dossier, triés alphabétiquement."""
    found = []
    for entry in os.scandir(directory):
        if entry.is_file() and os.path.splitext(entry.name)[1].lower() in VIDEO_EXTENSIONS:
            found.append(entry.path)
    return sorted(found, key=lambda p: os.path.basename(p).lower())


def build_crossfade(clips: list, fade_duration: float) -> CompositeVideoClip:
    """
    Assemble les clips avec un cross-fade de `fade_duration` secondes.

    Principe :
        - Clip 0 : démarre à t=0, occupe [0 … d0]
        - Clip 1 : démarre à t = d0 - fade_duration, avec crossfadein(fade_duration)
          ↳ pendant la dernière seconde du clip 0, le clip 1 monte en opacité
        - Clip 2 : démarre à t = (d0-f) + (d1-f), etc.
        - La durée totale = Σ di - f*(n-1)
    """
    if not clips:
        raise ValueError("La liste de clips est vide.")

    # S'assure que le fade ne dépasse pas le clip le plus court
    min_duration = min(c.duration for c in clips)
    if fade_duration >= min_duration:
        fade_duration = min_duration / 2
        print(
            "[AVERTISSEMENT] La durée du cross-fade a été ramenée à "
            f"{fade_duration:.2f}s pour s'adapter aux clips courts."
        )

    positioned = []
    start = 0.0

    for i, clip in enumerate(clips):
        if i == 0:
            # Premier clip : pas de fondu entrant
            positioned.append(clip.with_start(0) if MOVIEPY_VERSION >= 2 else clip.set_start(0))
        else:
            # Fondu entrant
            if MOVIEPY_VERSION >= 2:
                from moviepy.audio.fx import AudioFadeIn, AudioFadeOut
                from moviepy.video.fx import CrossFadeIn

                faded = clip.with_effects([CrossFadeIn(fade_duration)])
                if faded.audio:
                    faded = faded.with_audio(faded.audio.with_effects([AudioFadeIn(fade_duration)]))
                positioned.append(faded.with_start(start))
            else:
                faded = clip.crossfadein(fade_duration)
                if faded.audio:
                    faded = faded.set_audio(faded.audio.audio_fadein(fade_duration))
                positioned.append(faded.set_start(start))

        # Fondu sortant sur tous les clips sauf le dernier
        if i < len(clips) - 1:
            pos_clip = positioned[-1]
            if pos_clip.audio:
                if MOVIEPY_VERSION >= 2:
                    from moviepy.audio.fx import AudioFadeOut

                    pos_clip = pos_clip.with_audio(pos_clip.audio.with_effects([AudioFadeOut(fade_duration)]))
                else:
                    pos_clip = pos_clip.set_audio(pos_clip.audio.audio_fadeout(fade_duration))
                positioned[-1] = pos_clip

        # Calcul du point de départ du prochain clip (chevauchement = fade_duration)
        start += clip.duration - fade_duration

    total_duration = sum(c.duration for c in clips) - fade_duration * (len(clips) - 1)

    composite = CompositeVideoClip(positioned)
    if MOVIEPY_VERSION >= 2:
        composite = composite.with_duration(total_duration)
    else:
        composite = composite.set_duration(total_duration)
    return composite


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__doc__),
    )
    parser.add_argument(
        "--output",
        default="output_merged.mp4",
        help="Nom du fichier de sortie (défaut : output_merged.mp4)",
    )
    parser.add_argument(
        "--fade",
        type=float,
        default=1.0,
        help="Durée du cross-fade en secondes (défaut : 1.0)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=None,
        help="FPS de la vidéo finale (défaut : FPS du premier clip)",
    )
    parser.add_argument(
        "--codec",
        default="libx264",
        help="Codec vidéo ffmpeg (défaut : libx264)",
    )
    parser.add_argument(
        "--audio-codec",
        default="aac",
        help="Codec audio ffmpeg (défaut : aac)",
    )
    args = parser.parse_args()

    # --- Dossier du script ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, args.output)

    # --- Recherche des vidéos ---
    video_files = find_videos(script_dir)

    # Exclut le fichier de sortie si déjà présent dans le dossier
    video_files = [v for v in video_files if os.path.abspath(v) != os.path.abspath(output_path)]

    if not video_files:
        print("[ERREUR] Aucune vidéo trouvée dans :", script_dir)
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  moviepy v{MOVIEPY_VERSION}.x détecté")
    print(f"  {len(video_files)} vidéo(s) trouvée(s) — cross-fade : {args.fade}s")
    print(f"{'=' * 60}")
    for i, v in enumerate(video_files, 1):
        print(f"  {i:>3}. {os.path.basename(v)}")
    print(f"{'=' * 60}\n")

    if len(video_files) == 1:
        print("[INFO] Une seule vidéo détectée : aucun cross-fade à appliquer.")
        print("       La vidéo sera simplement re-encodée vers :", output_path)

    # --- Chargement des clips ---
    print("[1/3] Chargement des clips …")
    clips = []
    target_size = None  # on force tous les clips à la même résolution

    for path in video_files:
        clip = VideoFileClip(path)
        if target_size is None:
            target_size = (clip.w, clip.h)
        else:
            if (clip.w, clip.h) != target_size:
                print(
                    f"       Redimensionnement de '{os.path.basename(path)}' "
                    f"({clip.w}×{clip.h}) → {target_size[0]}×{target_size[1]}"
                )
                clip = clip.resize(target_size)
        clips.append(clip)

    fps = args.fps or clips[0].fps

    # --- Assemblage avec cross-fade ---
    if len(clips) == 1:
        final = clips[0]
    else:
        print("[2/3] Assemblage avec cross-fade …")
        final = build_crossfade(clips, args.fade)

    # --- Export ---
    print(f"[3/3] Export vers : {output_path}")
    print("      (Cela peut prendre plusieurs minutes selon la longueur des vidéos)\n")

    final.write_videofile(
        output_path,
        fps=fps,
        codec=args.codec,
        audio_codec=args.audio_codec,
        threads=os.cpu_count(),
        preset="medium",  # balance vitesse / qualité : ultrafast, fast, medium, slow
        logger="bar",  # affiche une barre de progression
    )

    # --- Nettoyage ---
    for clip in clips:
        clip.close()
    final.close()

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n✅  Vidéo fusionnée enregistrée : {output_path}  ({size_mb:.1f} Mo)\n")


if __name__ == "__main__":
    main()
