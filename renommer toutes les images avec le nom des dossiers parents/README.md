# Renommer toutes les images avec le nom des dossiers parents

Ce script Python renomme automatiquement les fichiers image en préfixant chaque nom par la chaîne des dossiers parents. Les noms sont convertis en *slugs* (minuscules, accents supprimés et caractères spéciaux remplacés par des tirets) pour éviter les caractères problématiques.

## Fonctionnement
- Le script repère le premier dossier présent à la racine du répertoire courant et l'utilise comme dossier principal.
- Il parcourt récursivement tous les sous-dossiers du dossier principal.
- Pour chaque image trouvée (JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP), il construit un préfixe à partir des noms de dossiers rencontrés, séparés par des underscores.
- Le nom d'origine du fichier est également *slugifié* puis concaténé au préfixe, avec l'extension en minuscules.
- Si un fichier portant déjà le nouveau nom existe, il n'est pas écrasé et un avertissement est affiché.

## Prérequis
- Python 3.7 ou version ultérieure.

## Utilisation
1. Placez le script `image-renamer.py` dans un répertoire contenant un seul dossier racine qui contient vos images dans ses sous-dossiers.
2. Ouvrez un terminal dans ce répertoire.
3. Exécutez :
   ```bash
   python image-renamer.py
   ```
4. Surveillez la console pour vérifier les fichiers renommés ou les avertissements d'écrasement.

## Exemple
Si la structure est :
```
photos/
├─ vacances 2023/
│  ├─ jour 1/
│  │  └─ plage.JPG
│  └─ jour 2/
│     └─ montagne.png
```
Le script renomme :
- `plage.JPG` → `photos_vacances-2023_jour-1_plage.jpg`
- `montagne.png` → `photos_vacances-2023_jour-2_montagne.png`

## Limites et conseils
- Seul le premier dossier rencontré dans le répertoire courant est traité. Assurez-vous qu'il contient l'ensemble des images à renommer.
- Faites une sauvegarde avant exécution si vous avez des doutes.
- Les noms générés sont adaptés au web grâce à la *slugification* et aux extensions en minuscules.
