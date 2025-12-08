import moviepy.editor as mp
import numpy as np

# ----------- CONFIGURATION -------------
SILENCE_THRESHOLD = 0.02   # niveau sonore max considéré comme silence (0 à 1)
MIN_SILENCE_DURATION = 1.5  # durée min d'un silence à couper (sec) -> met 1 ou 2
SAFE_MARGIN = 1.0           # respiration laissée avant/après les coupes
# ---------------------------------------

INPUT_VIDEO = "input.mp4"
OUTPUT_VIDEO = "output_cut.mp4"

def detect_silences(audio, threshold, min_duration, fps):
    sound = audio.to_soundarray(fps=fps)
    amplitude = np.max(np.abs(sound), axis=1)

    silences = []
    start = None

    for i, amp in enumerate(amplitude):
        if amp < threshold:
            if start is None:
                start = i
        else:
            if start is not None:
                duration = (i - start) / fps
                if duration >= min_duration:
                    silences.append((start/fps, i/fps))
                start = None

    if start is not None:
        duration = (len(amplitude) - start) / fps
        if duration >= min_duration:
            silences.append((start/fps, len(amplitude)/fps))

    return silences

def cut_video(video, silences, margin):
    cuts = []
    start = 0

    for (s, e) in silences:
        # on laisse une marge avant/après
        safe_start = max(start, s - margin)
        safe_end = min(video.duration, e + margin)

        if safe_start > start:
            cuts.append(video.subclip(start, safe_start))
        
        start = safe_end

    if start < video.duration:
        cuts.append(video.subclip(start, video.duration))

    return mp.concatenate_videoclips(cuts)

# --- MAIN ---
print("Chargement de la vidéo…")
video = mp.VideoFileClip(INPUT_VIDEO)
audio = video.audio

print("Détection des silences…")
silences = detect_silences(audio, SILENCE_THRESHOLD, MIN_SILENCE_DURATION, fps=audio.fps)

print("Coupes détectées :", silences)

print("Création de la vidéo finale…")
final = cut_video(video, silences, SAFE_MARGIN)

final.write_videofile(
    OUTPUT_VIDEO,
    codec="libx264",
    audio_codec="aac",
    threads=4
)

print("Terminé ! Fichier exporté sous :", OUTPUT_VIDEO)
