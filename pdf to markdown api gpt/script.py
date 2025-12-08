#!/usr/bin/env python3
"""
pdf2md_gpt.py
-------------
Lit un PDF « input.pdf » à la racine, envoie chaque page au modèle GPT
pour conversion en Markdown, puis écrit le résultat concaténé dans
« output.md ».

Dépendances :
    pip install openai pdfplumber
"""

from pathlib import Path
import time
import pdfplumber
import openai


# ----------------------- Clé API -------------------------
# REMPLACEZ la valeur ci-dessous par votre vraie clé.
OPENAI_API_KEY = "..."    # <-- ICI
# --------------------------------------------------------

# ----------------------- Paramètres ----------------------
PDF_NAME      = "input.pdf"
OUTPUT_MD     = "output.md"
MODEL_NAME    = "gpt-4o-mini"
MAX_RETRIES   = 3
DELAY_BETWEEN = 1.5
# ---------------------------------------------------------

PROMPT_INSTRUCTIONS = """Transforme ce texte normatif en Markdown bien structuré :

Identifie les titres hiérarchiques (ex. 7.3.2.1.4) et convertis-les en titres Markdown (#, ##, etc.).

Détecte les tableaux implicites (repérés par "Tableau X") et mets-les en forme Markdown avec en-têtes et colonnes.

Formate les listes (repérées par des puces ou énumérations) en listes à puces Markdown.

Corrige la casse excessive (ex. MAJUSCULES non nécessaires).

Ne change pas les mots, respecte le texte initial.

N’ajoute aucun commentaire comme "Voici le texte en Markdown", ni des "```markdown" : met seulement le contenu.
"""


def gpt_markdownify(page_text: str) -> str:
    """
    Envoie le texte d’une page au modèle GPT et renvoie la version Markdown.
    Réessaie jusqu’à MAX_RETRIES fois en cas d’échec.
    """
    client = openai.Client(api_key=OPENAI_API_KEY)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": f"{PROMPT_INSTRUCTIONS}\n\n---\n\n{page_text}"
                    }
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as err:
            print(f"[WARN] Échec appel GPT (tentative {attempt}/{MAX_RETRIES}) : {err}")
            if attempt == MAX_RETRIES:
                raise
            time.sleep(2 * attempt)  # back-off exponentiel


def extract_pages(pdf_path: Path) -> list[str]:
    """Extrait le texte de chaque page du PDF dans une liste."""
    with pdfplumber.open(pdf_path) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def main() -> None:
    pdf_path = Path(__file__).with_name(PDF_NAME)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf_path}")

    output_path = Path(__file__).with_name(OUTPUT_MD)
    output_path.write_text("")  # réinitialise

    print(f"[INFO] Conversion de « {pdf_path.name} » → « {output_path.name} »")

    for idx, page_text in enumerate(extract_pages(pdf_path), start=1):
        print(f"[INFO] Page {idx}…")
        markdown = gpt_markdownify(page_text)
        with output_path.open("a", encoding="utf-8") as md_file:
            md_file.write(markdown + "\n\n---\n\n")
        time.sleep(DELAY_BETWEEN)

    print(f"[OK] Terminé ! Markdown généré : {output_path.resolve()}")


if __name__ == "__main__":
    # Simple garde-fou : on s’assure qu’on n’a pas laissé la clé vide
    if OPENAI_API_KEY.startswith("sk-XXXX"):
        raise ValueError("Remplacez OPENAI_API_KEY par votre vraie clé avant d’exécuter le script.")
    main()
