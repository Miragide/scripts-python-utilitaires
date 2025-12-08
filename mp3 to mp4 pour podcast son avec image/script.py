#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path
import sys

# Extensions supportées
AUDIO_EXTS = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.wma'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}

def check_ffmpeg():
    """Vérifie que FFmpeg est installé"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg n'est pas installé ou pas dans le PATH")
        print("   Téléchargez-le sur : https://ffmpeg.org/download.html")
        return False

def get_duration(file):
    """Obtient la durée d'un fichier média"""
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 
               'format=duration', '-of', 'json', str(file)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"⚠️  Impossible de lire la durée de {file.name}: {e}")
        return None

def validate_file(file, file_type):
    """Valide qu'un fichier existe et n'est pas corrompu"""
    if not file.exists():
        print(f"❌ Le fichier {file_type} n'existe plus: {file.name}")
        return False
    
    if file.stat().st_size == 0:
        print(f"❌ Le fichier {file_type} est vide: {file.name}")
        return False
    
    return True

def main():
    # Vérifier FFmpeg
    if not check_ffmpeg():
        sys.exit(1)
    
    # Récupérer les fichiers dans le répertoire courant uniquement
    current_dir = Path('.')
    
    audio_file = next((f for f in current_dir.iterdir() 
                       if f.is_file() and f.suffix.lower() in AUDIO_EXTS), None)
    
    image_file = next((f for f in current_dir.iterdir() 
                       if f.is_file() and f.suffix.lower() in IMAGE_EXTS), None)
    
    # Vérifications
    if not audio_file:
        print(f"❌ Aucun fichier audio trouvé")
        print(f"   Formats supportés: {', '.join(AUDIO_EXTS)}")
        sys.exit(1)
    
    if not image_file:
        print(f"❌ Aucune image trouvée")
        print(f"   Formats supportés: {', '.join(IMAGE_EXTS)}")
        sys.exit(1)
    
    # Valider les fichiers
    if not validate_file(audio_file, "audio"):
        sys.exit(1)
    
    if not validate_file(image_file, "image"):
        sys.exit(1)
    
    print(f"🎵 Audio: {audio_file.name}")
    print(f"🖼️  Image: {image_file.name}")
    
    # Obtenir la durée de l'audio
    duration = get_duration(audio_file)
    if duration:
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        print(f"⏱️  Durée audio: {minutes}min {seconds}s ({duration:.2f}s)")
    else:
        print("⚠️  Impossible de déterminer la durée, mais on continue...")
    
    # Nom du fichier de sortie (éviter les caractères spéciaux)
    output_name = "".join(c for c in audio_file.stem if c.isalnum() or c in (' ', '-', '_'))
    output = f"output_{output_name}.mp4"
    
    # Vérifier si le fichier existe déjà
    if Path(output).exists():
        print(f"⚠️  Le fichier {output} existe déjà")
        try:
            response = input("   Voulez-vous l'écraser ? (o/n): ").lower()
            if response != 'o':
                print("❌ Opération annulée")
                sys.exit(0)
        except:
            pass  # Si input ne fonctionne pas, on continue
    
    # Commande FFmpeg CORRIGÉE
    cmd = [
        'ffmpeg',
        '-y',  # Écraser sans demander
        '-loop', '1',
        '-framerate', '1',  # 1 fps pour image fixe
        '-i', str(image_file),
        '-i', str(audio_file),
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'copy',  # Copie l'audio sans ré-encoder
        '-pix_fmt', 'yuv420p',
        '-movflags', 'faststart',  # SANS le +
        '-shortest',  # Option globale, pas dans -fflags
        '-max_muxing_queue_size', '9999',
        output
    ]
    
    print(f"\n⏳ Création de la vidéo en cours...")
    print(f"   (Cela peut prendre quelques instants pour {minutes}min d'audio)\n")
    
    try:
        # Exécuter FFmpeg
        result = subprocess.run(
            cmd, 
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes max pour 2h30 d'audio
        )
        
        if result.returncode != 0:
            print("\n❌ Erreur lors de la création de la vidéo")
            print(result.stderr)
            sys.exit(1)
        
        # Vérifier le fichier de sortie
        output_path = Path(output)
        if not output_path.exists():
            print("❌ Le fichier de sortie n'a pas été créé")
            sys.exit(1)
        
        output_size = output_path.stat().st_size / (1024 * 1024)  # Mo
        output_duration = get_duration(output_path)
        
        print(f"\n✅ Vidéo créée avec succès : {output}")
        print(f"   Taille: {output_size:.2f} Mo")
        
        if output_duration and duration:
            diff = abs(output_duration - duration)
            minutes_out = int(output_duration // 60)
            seconds_out = int(output_duration % 60)
            
            if diff > 1:  # Plus d'1 seconde de différence
                print(f"⚠️  Différence de durée détectée: {diff:.2f}s")
                print(f"   Audio original: {minutes}min {seconds}s")
                print(f"   Vidéo créée: {minutes_out}min {seconds_out}s")
            else:
                print(f"   Durée: {minutes_out}min {seconds_out}s ✓")
    
    except subprocess.TimeoutExpired:
        print("\n❌ Timeout : l'opération a pris trop de temps (>30min)")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
