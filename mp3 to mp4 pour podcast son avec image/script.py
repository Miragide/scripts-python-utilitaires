#!/usr/bin/env python3
"""
image_to_video.py
-----------------
Crée une vidéo MP4 720p à partir de la première image et du premier fichier
audio trouvés à la racine du répertoire courant.

Formats image supportés : JPEG, JPG, PNG, BMP, WEBP, TIFF
Formats audio supportés  : MP3, WAV, AAC, OGG, FLAC, M4A

Usage :
    python image_to_video.py               # utilise le répertoire courant
    python image_to_video.py /chemin/dossier
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


# ── Paramètres de sortie (YouTube 720p) ────────────────────────────────────────
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720
OUTPUT_FILE = "output_video.mp4"

IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".png", ".bmp", ".webp", ".tiff", ".tif"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"}


# ── Recherche des fichiers ──────────────────────────────────────────────────────
def find_first_file(directory: Path, extensions: set[str]) -> Path | None:
    """Retourne le premier fichier (ordre alphabétique) dont l'extension correspond."""
    candidates = sorted(
        f for f in directory.iterdir() if f.is_file() and f.suffix.lower() in extensions
    )
    return candidates[0] if candidates else None


# ── Redimensionnement de l'image ───────────────────────────────────────────────
def resize_image(
    image_path: Path,
    output_path: Path,
    width: int = OUTPUT_WIDTH,
    height: int = OUTPUT_HEIGHT,
) -> None:
    """
    Ouvre l'image, la redimensionne en 1280×720 en remplissant tout le cadre
    (crop centré si les proportions diffèrent), puis la sauvegarde en JPEG.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        src_w, src_h = img.size

        # Calcul du ratio pour couvrir entièrement le cadre (cover)
        ratio_w = width / src_w
        ratio_h = height / src_h
        ratio = max(ratio_w, ratio_h)

        new_w = round(src_w * ratio)
        new_h = round(src_h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

        # Crop centré pour obtenir exactement width × height
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        img = img.crop((left, top, left + width, top + height))

        img.save(output_path, "JPEG", quality=95)
        print(f"  Image redimensionnée : {src_w}×{src_h} → {width}×{height}")


# ── Durée de l'audio via ffprobe ───────────────────────────────────────────────
def get_audio_duration(audio_path: Path) -> float:
    """
    Retourne la durée en secondes du fichier audio grâce à ffprobe.
    Lève une RuntimeError si ffprobe échoue.
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(audio_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(
            f"ffprobe n'a pas pu lire la durée de '{audio_path}'.\n{result.stderr}"
        )
    duration = float(result.stdout.strip())
    print(f"  Durée audio détectée : {duration:.2f} s")
    return duration


# ── Création de la vidéo via FFmpeg ────────────────────────────────────────────
def build_video(image_path: Path, audio_path: Path, output_path: Path) -> None:
    """
    Appelle ffmpeg pour assembler l'image fixe et l'audio en MP4 720p.

    Correctifs écran noir :
    - On récupère la durée exacte avec ffprobe et on passe -t <durée>
      au lieu de -shortest (qui peut couper avant la première frame à 1 fps).
    - On utilise 25 fps (standard) pour garantir qu'au moins une frame
      soit encodée avant la fin du flux.
    """
    duration = get_audio_duration(audio_path)

    cmd = [
        "ffmpeg",
        "-y",
        # Image fixe en boucle à 25 fps — garantit que la frame est bien encodée
        "-loop",
        "1",
        "-framerate",
        "25",
        "-i",
        str(image_path),
        # Fichier audio
        "-i",
        str(audio_path),
        # Vidéo : H.264, tune stillimage, pixel format compatible
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-tune",
        "stillimage",
        "-crf",
        "23",
        "-vf",
        (
            f"scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:force_original_aspect_ratio=disable,"
            "format=yuv420p"
        ),
        # Durée exacte issue de ffprobe — évite l'écran noir de -shortest
        "-t",
        str(duration),
        # Audio : AAC 192 kbps stéréo
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ac",
        "2",
        # Optimisation pour le streaming / upload YouTube
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    print("\n  Lancement de FFmpeg…")
    print("  Commande :", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("\n── Erreur FFmpeg ──────────────────────────────")
        print(result.stderr)
        raise RuntimeError("FFmpeg a échoué. Voir le message ci-dessus.")

    print("  FFmpeg terminé avec succès.")


# ── Point d'entrée ─────────────────────────────────────────────────────────────
def main() -> None:
    # Répertoire cible (argument optionnel, sinon répertoire courant)
    directory = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    if not directory.is_dir():
        print(f"Erreur : '{directory}' n'est pas un répertoire valide.")
        sys.exit(1)

    print(f"Dossier analysé : {directory}\n")

    # ── Recherche des fichiers ─────────────────────────────────────────────────
    image_file = find_first_file(directory, IMAGE_EXTENSIONS)
    audio_file = find_first_file(directory, AUDIO_EXTENSIONS)

    if not image_file:
        print(f"Aucune image trouvée ({', '.join(IMAGE_EXTENSIONS)}).")
        sys.exit(1)
    if not audio_file:
        print(f"Aucun fichier audio trouvé ({', '.join(AUDIO_EXTENSIONS)}).")
        sys.exit(1)

    print(f"  Image  : {image_file.name}")
    print(f"  Audio  : {audio_file.name}")

    # ── Redimensionnement dans un fichier temporaire ───────────────────────────
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        resized_image = tmp_dir / "frame.jpg"
        resize_image(image_file, resized_image)

        # ── Création de la vidéo ───────────────────────────────────────────────
        output_path = directory / OUTPUT_FILE
        build_video(resized_image, audio_file, output_path)

        size_mb = output_path.stat().st_size / 1_048_576
        print(f"\n✅ Vidéo créée : {output_path}")
        print(f"   Taille      : {size_mb:.1f} Mo")
        print(f"   Résolution  : {OUTPUT_WIDTH}×{OUTPUT_HEIGHT} (720p)")
        print("   Codec vidéo : H.264 (libx264)")
        print("   Codec audio : AAC 192 kbps")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
