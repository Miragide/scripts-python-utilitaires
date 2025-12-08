# PDF → PNG

Script : `script.py`

Convertit chaque page de chaque PDF du dossier en une image PNG (`*_page_1.png`,
`*_page_2.png`, etc.) à 200 DPI.

## Prérequis
- Python 3
- `pymupdf` (importé en tant que `fitz`)
- `Pillow`

Installation :
```bash
pip install pymupdf pillow
```

## Utilisation
```bash
python script.py
```
Les images générées sont enregistrées dans le même dossier que les PDF d'entrée.
