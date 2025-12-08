import os
import ffmpeg

def convert_all_mp4_to_mp3():
    # Lister tous les fichiers MP4 dans le dossier actuel
    mp4_files = [f for f in os.listdir() if f.lower().endswith('.mp4')]

    if not mp4_files:
        print("Aucun fichier MP4 trouvé dans le dossier.")
        return

    for file in mp4_files:
        mp3_filename = os.path.splitext(file)[0] + '.mp3'
        try:
            print(f"Conversion de : {file} → {mp3_filename}")
            ffmpeg.input(file).output(mp3_filename, **{'q:a': 0, 'vn': None}).run(quiet=True)
            print(f"✔ Conversion terminée : {mp3_filename}")
        except ffmpeg.Error as e:
            print(f"❌ Erreur lors de la conversion de {file} :", e)

if __name__ == "__main__":
    convert_all_mp4_to_mp3()
