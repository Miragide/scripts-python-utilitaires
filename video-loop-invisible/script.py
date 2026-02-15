#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path


# --- GUI minimaliste (Tkinter) ---
def pick_files_gui():
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as e:
        raise RuntimeError(
            "Tkinter indisponible. Sur Linux installe souvent 'python3-tk'. "
            f"Détail: {e}"
        )

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    inp = filedialog.askopenfilename(
        title="Sélectionner la vidéo source",
        filetypes=[
            ("Vidéos", "*.mp4 *.mov *.mkv *.avi *.webm *.m4v"),
            ("Tous les fichiers", "*.*"),
        ],
    )
    if not inp:
        raise SystemExit("Annulé (aucun fichier source).")

    default_out = str(Path(inp).with_name(Path(inp).stem + "_loop.mp4"))
    out = filedialog.asksaveasfilename(
        title="Enregistrer la vidéo loopable",
        defaultextension=".mp4",
        initialfile=Path(default_out).name,
        initialdir=str(Path(default_out).parent),
        filetypes=[("MP4", "*.mp4"), ("Tous les fichiers", "*.*")],
    )
    if not out:
        raise SystemExit("Annulé (aucun fichier de sortie).")

    return inp, out


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            "Commande échouée:\n"
            + " ".join(cmd)
            + "\n\nSTDERR:\n"
            + p.stderr.strip()
        )
    return p.stdout


def ffprobe_json(input_path: str) -> dict:
    out = run([
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        input_path,
    ])
    return json.loads(out)


def get_duration_seconds(info: dict) -> float:
    dur = info.get("format", {}).get("duration")
    if dur is None:
        raise RuntimeError("Impossible de lire la durée via ffprobe.")
    return float(dur)


def has_audio_stream(info: dict) -> bool:
    return any(s.get("codec_type") == "audio" for s in info.get("streams", []))


def build_filter_complex(T: float, d: float, keep_audio: bool, audio_present: bool):
    # Vidéo : overlay du head (fade alpha 0->1) sur les d dernières secondes, puis trim [d..T]
    vf = f"""
    [0:v]trim=0:{T:.6f},setpts=PTS-STARTPTS,format=yuva420p[base];
    [0:v]trim=0:{d:.6f},setpts=PTS-STARTPTS,format=yuva420p,
         fade=t=in:st=0:d={d:.6f}:alpha=1[head];
    [head]setpts=PTS+({T:.6f}-{d:.6f})/TB[head_del];
    [base][head_del]overlay=shortest=1:eof_action=pass:format=auto[vcomp];
    [vcomp]trim=start={d:.6f}:end={T:.6f},setpts=PTS-STARTPTS,format=yuv420p[vout]
    """.strip().replace("\n", "")

    maps = ["-map", "[vout]"]

    if keep_audio and audio_present:
        delay_ms = int(round((T - d) * 1000.0))
        af = f"""
        [0:a]atrim=0:{T:.6f},asetpts=PTS-STARTPTS[abase];
        [abase]afade=t=out:st={T - d:.6f}:d={d:.6f}[atail];
        [0:a]atrim=0:{d:.6f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d={d:.6f}[ahead];
        [ahead]adelay=delays={delay_ms}:all=1[ahead_del];
        [atail][ahead_del]amix=inputs=2:duration=longest:dropout_transition=0[amix];
        [amix]atrim=start={d:.6f}:end={T:.6f},asetpts=PTS-STARTPTS[aout]
        """.strip().replace("\n", "")
        fc = vf + ";" + af
        maps += ["-map", "[aout]"]
    else:
        fc = vf

    return fc, maps


def main():
    ap = argparse.ArgumentParser(
        description="Rendre une vidéo loopable via superposition du début sur la fin."
    )
    ap.add_argument("input", nargs="?", help="Vidéo source")
    ap.add_argument("output", nargs="?", help="Vidéo loopable (mp4)")
    ap.add_argument(
        "--fade",
        type=float,
        default=4.0,
        help="Durée du fondu/superposition en secondes (défaut 4.0)",
    )
    ap.add_argument(
        "--no-audio", action="store_true", help="Désactive l'audio même si présent"
    )
    ap.add_argument("--crf", type=int, default=18, help="CRF H.264 (défaut 18)")
    ap.add_argument("--preset", default="medium", help="Preset x264 (défaut medium)")
    args = ap.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise SystemExit(
            "ffmpeg/ffprobe introuvables. Installe FFmpeg et assure-toi qu'il est dans le PATH."
        )

    # Si input/output manquants -> GUI
    if not args.input or not args.output:
        inp, out = pick_files_gui()
    else:
        inp, out = args.input, args.output

    inp = str(Path(inp))
    out = str(Path(out))

    info = ffprobe_json(inp)
    T = get_duration_seconds(info)
    audio_present = has_audio_stream(info)

    d = float(args.fade)
    if d <= 0:
        raise SystemExit("--fade doit être > 0")

    # Sécurité : d < T et d <= T/2
    if d >= T:
        d = max(0.1, T / 2.0)
    if d > T / 2.0:
        d = T / 2.0

    keep_audio = not args.no_audio
    filter_complex, maps = build_filter_complex(
        T=T, d=d, keep_audio=keep_audio, audio_present=audio_present
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        inp,
        "-filter_complex",
        filter_complex,
        *maps,
        "-c:v",
        "libx264",
        "-crf",
        str(args.crf),
        "-preset",
        args.preset,
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
    ]

    if keep_audio and audio_present:
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]

    cmd += [out]

    subprocess.run(cmd, check=True)
    print(f"OK: {out}")
    print(
        f"Durée source: {T:.3f}s | fondu: {d:.3f}s | audio: {'oui' if (keep_audio and audio_present) else 'non'}"
    )
    print("Test loop: ffplay -loop 0 -i output.mp4")


if __name__ == "__main__":
    main()
