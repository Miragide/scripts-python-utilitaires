#!/usr/bin/env python3
"""
Concatène toutes les vidéos placées dans le dossier du script, les convertit en carré
420 × 420 px puis les assemble séquentiellement dans un seul fichier
`output_420_concat.mp4`.

Cette version n’utilise **plus MoviePy** mais la combinaison :
- le binaire **FFmpeg** (obligatoire, installable depuis https://ffmpeg.org/ );
- la bibliothèque fine **ffmpeg‑python** (wrapper Python léger autour de FFmpeg).

Installation rapide :
    pip install ffmpeg-python  # wrapper
    # téléchargez FFmpeg pour votre OS et ajoutez‑le au PATH.

Avantages :
- Aucun souci de compatibilité d’API MoviePy ;
- Encodage uniforme (H.264 + AAC, 30 fps) garantissant une concaténation sans ré‑encodage final ;
- Script plus rapide grâce à l’usage direct de FFmpeg.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import List

import ffmpeg  # pip install ffmpeg-python (wrapper, pas le binaire)

# --- Réglages -----------------------------------------------------------------
TARGET_SIZE = 420   # dimension du carré (px)
FPS = 30            # fréquence d'images imposée à chaque clip
VALID_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.avi', '.webm'}
OUTPUT_NAME = 'output_420_concat.mp4'
# -----------------------------------------------------------------------------

def collect_video_paths(directory: Path) -> List[Path]:
    """Retourne la liste triée des vidéos valides présentes dans *directory*."""
    return sorted(
        p for p in directory.iterdir()
        if p.suffix.lower() in VALID_EXTENSIONS and p.name != OUTPUT_NAME
    )

def process_video(src: Path, dst: Path) -> None:
    """Redimensionne/recadre *src* → *dst* (carré 420 px, H.264 + AAC, 30 fps)."""
    (
        ffmpeg
        .input(str(src))
        .output(
            str(dst),
            vf=f'scale={TARGET_SIZE}:{TARGET_SIZE}:force_original_aspect_ratio=increase,'
               f'crop={TARGET_SIZE}:{TARGET_SIZE}',
            r=FPS,
            vcodec='libx264',
            acodec='aac',
            movflags='faststart',
            pix_fmt='yuv420p',
            loglevel='error',
        )
        .overwrite_output()
        .run()
    )

def concat_videos(file_list: Path, output: Path) -> None:
    """Concatène sans ré‑encodage les vidéos listées dans *file_list* vers *output*."""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', str(file_list),
        '-c', 'copy',
        str(output)
    ]
    subprocess.run(cmd, check=True)

def main() -> None:
    root = Path(__file__).resolve().parent
    sources = collect_video_paths(root)

    if not sources:
        print('Aucune vidéo trouvée dans', root)
        return

    print(f"→ {len(sources)} vidéo(s) détectée(s). Préparation…")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        processed: List[Path] = []

        # 1. Conversion individuelle (scale/crop/encode)
        for idx, src in enumerate(sources):
            tmp_out = tmpdir_path / f'clip_{idx:03d}.mp4'
            print(f'   • Traitement : {src.name}')
            process_video(src, tmp_out)
            processed.append(tmp_out)

        # 2. Création de la liste pour le concat demuxer
        list_file = tmpdir_path / 'concat_list.txt'
        with list_file.open('w', encoding='utf-8') as f:
            for p in processed:
                f.write(f"file '{p.as_posix()}'\n")

        # 3. Concaténation sans ré-encodage
        print('→ Concaténation…')
        concat_videos(list_file, root / OUTPUT_NAME)

    print(f'\n✓ Vidéo finale créée : {OUTPUT_NAME}')

if __name__ == '__main__':
    main()
