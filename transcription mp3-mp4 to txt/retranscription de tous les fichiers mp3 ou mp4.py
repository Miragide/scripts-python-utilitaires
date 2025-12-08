import whisper
import os
import glob

# 🔍 Rechercher tous les fichiers MP4 et MP3 dans le dossier courant
audio_files = glob.glob("*.mp4") + glob.glob("*.mp3") + glob.glob("*.m4a")  # Liste tous les fichiers .mp4 et .mp3

if not audio_files:
    print("❌ Aucun fichier MP4 ou MP3 trouvé dans le dossier du script.")
    exit()

# 🚀 Charger le modèle Whisper (small pour un bon équilibre vitesse/précision sinon tiny ou base)
model = whisper.load_model("small")

for audio_file in audio_files:
    print(f"🎵 Fichier trouvé : {audio_file}")
    
    # 🎙️ Transcrire l'audio
    print("⏳ Transcription en cours...")
    result = model.transcribe(audio_file)
    
    # 📝 Générer un nom de fichier pour la transcription
    output_file = os.path.splitext(audio_file)[0] + "_transcription.txt"
    
    # 💾 Sauvegarde de la transcription dans un fichier texte
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"✅ Transcription terminée et enregistrée dans : {output_file}")