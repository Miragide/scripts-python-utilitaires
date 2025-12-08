# Fusion de PDF

Script : `script.py`

Parcourt le dossier courant, trie tous les fichiers `.pdf` puis les fusionne dans
un fichier `fusion.pdf` unique.

## Prérequis
- Python 3
- `PyPDF2`

Installez la dépendance :
```bash
pip install PyPDF2
```

## Utilisation
```bash
python script.py
```
Le script affiche chaque fichier ajouté puis crée `fusion.pdf` dans le dossier.
Assurez-vous de placer uniquement les PDF à fusionner dans le répertoire.
