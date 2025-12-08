# Scripts Python utilitaires

Ce dépôt regroupe de petits outils autonomes. Chaque dossier contient au moins
un script prêt à être exécuté depuis son propre répertoire. Référez-vous aux
README de chaque dossier pour les commandes détaillées et les dépendances.

## Aperçu rapide
- `arborescence-maker/` : affiche l'arborescence d'un dossier avec Tkinter.
- `fusion-pdf/` : fusionne tous les PDF du dossier en un seul fichier.
- `image-to-pdf/` : assemble toutes les images en un PDF unique.
- `image-to-txt/` : effectue de l'OCR (EasyOCR) sur chaque image et exporte en CSV.
- `mp4-to-mp3/` : extrait la piste audio de chaque MP4 en MP3 avec FFmpeg.
- `optimize-images-2000px-compress/` : redimensionne et compresse des JPEG, ou renomme des lots d'images.
- `pdf-to-img/` : exporte chaque page PDF en PNG.
- `pdf-to-markdown-api-gpt/` : convertit un PDF en Markdown via l'API OpenAI.
- `remove-image-backgrounds/` : supprime le fond des images via `rembg`.
- `transcription-mp3-mp4-to-txt/` : transcrit audios/vidéos en texte avec Whisper.
- `vcard-to-csv/` : convertit un fichier `.vcf` en CSV.
- `verification-numero-secu/` : contrôle des numéros de sécu dans un CSV et génération d'un rapport.
- `video-montage-photos-to-video/` : recadre plusieurs vidéos en carré puis les concatène.

## Conseils généraux
- Exécutez les scripts depuis **leur propre dossier** pour qu'ils trouvent les
  fichiers attendus.
- Installez les dépendances mentionnées dans chaque README (`pip install ...`).
- Sauvegardez vos fichiers sources avant d'exécuter un script qui modifie les
  images/vidéos de manière destructive.

## Pourquoi je vois des doublons ou des conflits ?
- Les dossiers ont été renommés en kebab-case (ex. `aborescence maker` →
  `arborescence-maker`). Si votre branche locale part d'un commit plus ancien
  avec les anciens noms, GitHub affiche alors **l'ancien dossier et le nouveau**
  au lieu de les fusionner, d'où les doublons.
- Pour éviter les conflits, mettez votre branche à jour avant de pousser
  (`git pull --rebase origin <branche>`), puis supprimez les anciens dossiers
  locaux résiduels s'il y en a encore avant de relancer le commit.
