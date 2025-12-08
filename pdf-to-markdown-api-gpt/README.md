# PDF → Markdown avec GPT

Script : `script.py`

Lit `input.pdf` placé dans le même dossier, envoie chaque page à l'API OpenAI
pour convertir le contenu en Markdown structuré, puis concatène le tout dans
`output.md`.

## Prérequis
- Python 3
- `openai`
- `pdfplumber`

Installez les dépendances :
```bash
pip install openai pdfplumber
```

## Configuration
1. Renseignez votre clé API dans la variable `OPENAI_API_KEY` du script.
2. Ajustez éventuellement `MODEL_NAME`, `MAX_RETRIES` ou les instructions du
   prompt pour adapter la mise en forme.

## Utilisation
```bash
python script.py
```
Le script parcourt chaque page du PDF et écrit le Markdown généré dans
`output.md` en insérant un séparateur `---` entre les pages.
