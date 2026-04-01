# WP Heavy Files Finder

Script PHP autonome pour diagnostiquer rapidement les fichiers lourds sur un site WordPress.

## Capture d'écran

![Capture d'écran de WP Heavy Files Finder](https://user-images.githubusercontent.com/placeholder/wp-heavy-files-finder.png)

## Installation (usage ponctuel)

1. Renomme le fichier en `wp-diagnostic.php` si besoin.
2. Uploade `wp-diagnostic.php` à la racine de ton WordPress via FTP.
3. Modifie le mot de passe dans le script (constante `PASSWORD`) avant exécution.
4. Ouvre : `https://tonsite.com/wp-diagnostic.php`

## Fonctionnalités

- Affiche les poids des sous-dossiers du répertoire courant (navigation cliquable).
- Affiche le top N des fichiers les plus lourds avec barre de poids relatif.
- Filtre par taille minimum (par défaut 1 MB).
- Permet la navigation dossier par dossier.
- Protection par mot de passe (`PASSWORD`).

## Paramètres URL

- `?min=1` : taille minimum en MB.
- `?top=50` : nombre max de fichiers affichés.
- `?dir=/chemin/absolu` : dossier à scanner (restreint à la racine du script).

## Sécurité

- Ce script expose une partie de la structure du serveur.
- **Supprime impérativement `wp-diagnostic.php` après diagnostic.**
