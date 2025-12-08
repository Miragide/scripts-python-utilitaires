# vCard vers CSV

Script : `vcard to csv.py`

Analyse un fichier vCard `data/contacts.vcf` et exporte les contacts vers un
fichier CSV `data/contacts.csv` en regroupant numéros et emails.

## Prérequis
- Python 3

## Organisation des fichiers
- Placez vos fichiers `.vcf` dans le sous-dossier `data/` (créé automatiquement
  si absent).

## Utilisation
```bash
python "vcard to csv.py"
```
Le script lit `data/contacts.vcf` et écrit `data/contacts.csv` dans le même
répertoire.
