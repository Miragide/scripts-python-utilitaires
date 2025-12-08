# Convertisseur WordPress XML vers Markdown

Cet utilitaire transforme les articles issus d'un export WordPress (fichier XML) en un document Markdown unique. Il propose à la fois une interface graphique simple ainsi qu'un mode ligne de commande pour automatiser les conversions.

## Fonctionnalités
- Convertit les balises HTML courantes en Markdown (titres, emphase, liens, sauts de ligne).
- Nettoie les shortcodes WordPress, notamment ceux générés par Divi (`[et_pb_*]`).
- Ignore les images pour produire un contenu texte épuré.
- Ajoute le titre et l'URL de chaque article et sépare les articles par une ligne `...`.
- Journalise la progression dans l'interface graphique et propose une barre de progression.

## Prérequis
- Python 3.10 ou plus récent.
- `tkinter` est requis pour l'interface graphique (installé par défaut sur la plupart des distributions Python de bureau).

## Utilisation en ligne de commande
```bash
python script.py chemin/vers/export_wordpress.xml sortie.md
```
- `export_wordpress.xml` : fichier exporté depuis WordPress via **Outils > Exporter**.
- `sortie.md` : chemin du fichier Markdown généré.

Le script affiche le nombre d'articles détectés et signale les erreurs de lecture ou d'écriture.

## Utilisation avec l'interface graphique
Lancer simplement :
```bash
python script.py
```
1. Cliquez sur **Parcourir...** pour sélectionner l'export XML WordPress.
2. Choisissez le fichier Markdown de sortie (un nom est proposé automatiquement à partir du XML sélectionné).
3. Cliquez sur **Convertir** pour démarrer la transformation.
4. Suivez l'avancement dans la zone « Journal des opérations » ; une notification confirme la réussite.

## Notes
- Les images sont ignorées et les shortcodes sont retirés pour obtenir un Markdown propre.
- Si aucun article n'est trouvé dans le fichier XML, une alerte est affichée et aucun fichier n'est créé.
- Les articles sont concaténés dans un seul fichier Markdown. Vous pouvez ensuite découper le contenu si nécessaire.
