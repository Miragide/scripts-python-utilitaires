# PDF → Markdown via OpenAI

Script : `script.py`

Lit `input.pdf` placé dans ce dossier, envoie chaque page au modèle OpenAI
(`gpt-4o-mini` par défaut) pour produire du Markdown structuré, puis concatène
l'ensemble dans `output.md` avec un séparateur `---` entre les pages.

## Prérequis
- Python 3
- `openai`
- `pdfplumber`

Installation :
```bash
pip install openai pdfplumber
```

## Configuration
1. Ouvrez `script.py` et renseignez votre clé API dans `OPENAI_API_KEY`.
2. Facultatif : ajustez le modèle (`MODEL_NAME`), le nombre de tentatives ou
   le prompt `PROMPT_INSTRUCTIONS` pour adapter la mise en forme.

## Utilisation
```bash
python script.py
```
Le script journalise chaque page traitée. `output.md` est écrasé puis rempli au
fil des pages.
