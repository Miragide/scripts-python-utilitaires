# PDF vers images

Script : `script.py`

Convertit chaque page de tous les PDF présents dans le dossier en images PNG
(`nom_page_#.png`) avec une résolution de 200 DPI.

## Prérequis
- Python 3
- `pymupdf` (package `fitz`)
- `Pillow`

Installation :
```bash
pip install pymupdf pillow
```

## Utilisation
```bash
python script.py
```
Les images générées sont enregistrées dans le même dossier que les PDF source.
