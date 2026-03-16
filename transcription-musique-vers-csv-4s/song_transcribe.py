#!/usr/bin/env python3
"""
song_transcribe.py
------------------
Transcrit le premier fichier MP3 trouvé à la racine du répertoire courant
avec OpenAI Whisper (timestamps par mot), puis génère un CSV avec :
  - Timecode (début de la fenêtre, format MM:SS)
  - Contenu (paroles dans cette fenêtre de 4 secondes)
  - Durée (en secondes, toujours 4 sauf éventuellement la dernière)

Usage :
    python song_transcribe.py [--model small] [--window 4] [--output output.csv]

Dépendances :
    pip install openai-whisper
    # whisper nécessite aussi ffmpeg installé sur le système :
    # macOS  : brew install ffmpeg
    # Ubuntu : sudo apt install ffmpeg
    # Windows: https://ffmpeg.org/download.html
"""

import argparse
import csv
import glob
import os
import sys

# ── Vérification de la présence de whisper ───────────────────────────────────
try:
    import whisper
except ImportError:
    sys.exit(
        "❌  Le module 'openai-whisper' est introuvable.\n"
        "   Installez-le avec :  pip install openai-whisper"
    )


# ── Utilitaires ──────────────────────────────────────────────────────────────
def seconds_to_timecode(seconds: float) -> str:
    """Convertit des secondes flottantes en timecode MM:SS.mmm"""
    m = int(seconds) // 60
    s = seconds - m * 60
    return f"{m:02d}:{s:06.3f}"


def find_first_mp3(search_dir: str = ".") -> str | None:
    """Renvoie le chemin du premier fichier .mp3 trouvé dans search_dir."""
    pattern = os.path.join(search_dir, "*.mp3")
    files = sorted(glob.glob(pattern))
    return files[0] if files else None


def transcribe_with_whisper(mp3_path: str, model_name: str) -> list[dict]:
    """
    Transcrit le fichier audio et renvoie la liste des mots avec timestamps.

    Chaque élément : {"word": str, "start": float, "end": float}
    """
    print(f"🔄  Chargement du modèle Whisper « {model_name} »…")
    model = whisper.load_model(model_name)

    print(f"🎵  Transcription de : {mp3_path}")
    result = model.transcribe(
        mp3_path,
        word_timestamps=True,
        verbose=False,
        condition_on_previous_text=False,  # ne saute pas les refrains répétés
        # None = désactive complètement les filtres de rejet de segments.
        # Avec des valeurs numériques même très permissives, Whisper peut encore
        # éliminer silencieusement des passages chantés. None est la seule
        # garantie qu'aucun segment n'est jeté.
        no_speech_threshold=None,
        logprob_threshold=None,
        compression_ratio_threshold=None,
    )

    words = []
    for segment in result.get("segments", []):
        seg_words = segment.get("words", [])

        if seg_words:
            # Cas normal : timestamps disponibles mot par mot
            for w in seg_words:
                word_text = w.get("word", "").strip()
                if word_text:
                    words.append({
                        "word": word_text,
                        "start": float(w["start"]),
                        "end": float(w["end"]),
                    })
        else:
            # Fallback : Whisper n'a pas fourni de timestamps par mot.
            # On distribue les mots uniformément sur la durée du segment.
            # Sans ça, un segment de 3s→9s stocké en un seul bloc avec
            # start=3.0 disparaît complètement de la fenêtre 5-10s.
            seg_text = segment.get("text", "").strip()
            if not seg_text:
                continue
            seg_start = float(segment["start"])
            seg_end = float(segment["end"])
            seg_dur = seg_end - seg_start
            tokens = seg_text.split()
            n = len(tokens)
            for k, token in enumerate(tokens):
                # Répartition linéaire : chaque mot occupe 1/n de la durée
                word_start = seg_start + (k / n) * seg_dur
                word_end = seg_start + ((k + 1) / n) * seg_dur
                words.append({
                    "word": token,
                    "start": round(word_start, 4),
                    "end": round(word_end, 4),
                })

    return words


NO_LYRICS_LABEL = "[no lyrics]"


def build_windows(words: list[dict], window: float, total_duration: float) -> list[dict]:
    """
    Regroupe les mots en fenêtres fixes de `window` secondes.

    Renvoie une liste de dicts :
        {"timecode": str, "content": str, "duration": float}

    Toutes les fenêtres sont présentes, même si aucun mot n'est détecté.
    Dans ce cas, le contenu est mis à NO_LYRICS_LABEL ("[no lyrics]").
    """
    rows = []
    i = 0

    while True:
        # Calcul depuis l'origine pour éviter l'accumulation d'erreurs flottantes
        start = round(i * window, 6)
        if start >= total_duration:
            break
        end = round((i + 1) * window, 6)
        actual_end = min(end, total_duration)
        duration = round(actual_end - start, 3)

        window_words = [
            w["word"]
            for w in words
            if w["start"] >= start and w["start"] < end
        ]

        rows.append({
            "timecode": seconds_to_timecode(start),
            "content": " ".join(window_words) if window_words else NO_LYRICS_LABEL,
            "duration": duration,
        })

        i += 1

    return rows


def write_csv(rows: list[dict], output_path: str) -> None:
    """Écrit les lignes dans un fichier CSV."""
    fieldnames = ["Timecode", "Contenu", "Durée (s)"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "Timecode": row["timecode"],
                "Contenu": row["content"],
                "Durée (s)": row["duration"],
            })
    print(f"✅  CSV généré : {output_path}  ({len(rows)} lignes)")


# ── Obtenir la durée totale de l'audio ───────────────────────────────────────
def get_audio_duration(mp3_path: str) -> float:
    """
    Essaie d'obtenir la durée via mutagen (léger) ou ffprobe,
    et en dernier recours charge l'audio avec whisper.audio.
    """
    # Option 1 : mutagen
    try:
        from mutagen.mp3 import MP3 as MutagenMP3

        audio = MutagenMP3(mp3_path)
        return audio.info.length
    except Exception:
        pass

    # Option 2 : ffprobe
    try:
        import json
        import subprocess

        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            mp3_path,
        ]
        out = subprocess.check_output(cmd)
        info = json.loads(out)
        return float(info["format"]["duration"])
    except Exception:
        pass

    # Option 3 : charger l'audio avec whisper.audio (plus lent)
    try:
        audio = whisper.load_audio(mp3_path)
        return len(audio) / whisper.audio.SAMPLE_RATE
    except Exception:
        pass

    return 0.0


# ── Point d'entrée ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Transcrit un MP3 avec Whisper et génère un CSV toutes les N secondes."
    )
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Modèle Whisper à utiliser (défaut : small). "
        "« medium » ou « large-v3 » pour plus de précision sur les chansons.",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=4.0,
        help="Taille de la fenêtre de paroles en secondes (défaut : 4). "
        "Avec un fondu de 1s entre clips de 5s, le visible net est 4s : "
        "clip_duree(5s) - fondu(1s) = fenetre_paroles(4s).",
    )
    parser.add_argument(
        "--output",
        default="transcription.csv",
        help="Nom du fichier CSV de sortie (défaut : transcription.csv).",
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Répertoire où chercher le premier MP3 (défaut : répertoire courant).",
    )
    args = parser.parse_args()

    # 1. Trouver le MP3
    mp3_path = find_first_mp3(args.dir)
    if not mp3_path:
        sys.exit(f"❌  Aucun fichier .mp3 trouvé dans : {os.path.abspath(args.dir)}")
    print(f"🎧  Fichier MP3 détecté : {mp3_path}")

    # 2. Durée totale
    total_duration = get_audio_duration(mp3_path)
    print(f"⏱️   Durée totale : {seconds_to_timecode(total_duration)}")

    # 3. Transcription Whisper
    words = transcribe_with_whisper(mp3_path, args.model)
    if not words:
        sys.exit("❌  Aucun mot détecté par Whisper. Vérifiez que le fichier contient des paroles.")
    print(f"📝  {len(words)} mots détectés au total.")

    # 4. Découpage en fenêtres de N secondes
    rows = build_windows(words, args.window, total_duration)
    print(f"🗂️   {len(rows)} fenêtres de {args.window}s contenant des paroles.")

    # 5. Export CSV
    write_csv(rows, args.output)

    # 6. Aperçu dans le terminal
    print("\n── Aperçu des 5 premières lignes ──")
    print(f"{'Timecode':<12} {'Durée':>8}  Contenu")
    print("-" * 60)
    for row in rows[:5]:
        preview = row["content"][:50] + ("…" if len(row["content"]) > 50 else "")
        print(f"{row['timecode']:<12} {row['duration']:>6.1f}s  {preview}")


if __name__ == "__main__":
    main()
