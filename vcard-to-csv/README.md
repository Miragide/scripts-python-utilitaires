# vCard → CSV

Script : `vcard to csv.py`

Lit le fichier `data/contacts.vcf`, extrait pour chaque contact les noms,
numéros de téléphone et emails, puis écrit un CSV `data/contacts.csv`.

## Prérequis
- Python 3

## Organisation des fichiers
- Placez vos fichiers `.vcf` dans le sous-dossier `data/` (créé automatiquement
  si absent).

## Utilisation
```bash
python "vcard to csv.py"
```
Le script lit `contacts.vcf` et génère `contacts.csv` dans le même dossier `data/`.
