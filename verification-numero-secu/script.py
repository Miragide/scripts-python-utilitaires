#!/usr/bin/env python3
"""
verifier_nir.py – Génère le NIR attendu pour chaque salarié,
le compare au NIR saisi et écrit le résultat dans un nouveau CSV.

Colonnes requises dans salariés.csv :
  sexe (M/F), annee_naissance, mois_naissance (01‑12),
  departement (75, 99, 2A …), commune (code INSEE ou pays),
  num_ordre (3 chiffres), nir_saisi (15 caractères)

© 2025 – Adapté pour exécution locale (Thonny)
"""

import pandas as pd
import re
from pathlib import Path
import sys

FICHIER_ENTREE = Path("salariés.csv")          # nom du fichier source
FICHIER_SORTIE = Path("salariés_verifiés.csv")  # nom du fichier de sortie

# ───────────────────────────────────────── Fonctions utilitaires ──
def sexe_code(s: str) -> str:
    """Convertit 'M'/'F' en 1/2 (code sexe NIR)"""
    return "2" if s.upper() == "F" else "1"

def base_nir(row) -> str:
    """Construit les 13 premiers caractères du NIR (hors clé)"""
    sexe = sexe_code(row["sexe"])
    aa   = str(row["annee_naissance"])[-2:]
    mm   = str(row["mois_naissance"]).zfill(2)
    dep  = str(row["departement"])
    com  = str(row["commune"]).zfill(3)
    ord_ = str(row["num_ordre"]).zfill(3)

    base = f"{sexe}{aa}{mm}{dep}{com}{ord_}"

    # Cas particuliers Corse
    if dep == "2A":
        base = f"{sexe}{aa}{mm}19{com}{ord_}"
    elif dep == "2B":
        base = f"{sexe}{aa}{mm}18{com}{ord_}"

    return base

def cle97(base13: str) -> int:
    """Calcule la clé : 97 - (nombre mod 97) (ou 97 si reste 0)"""
    reste = int(base13) % 97
    return (97 - reste) if reste else 97

def nir_attendu(row) -> str:
    base = base_nir(row)
    return base + str(cle97(base)).zfill(2)

def comparer(row) -> str:
    exp = nir_attendu(row)
    act = re.sub(r"\s+", "", str(row["nir_saisi"]))  # suppr. espaces

    # Cas correspondance exacte
    if exp == act:
        return "Correspondance ✅"

    # Anomalie de longueur / type
    if len(act) != 15 or not act.isdigit():
        return "Différence ❌ : format invalide"

    # Détails des divergences
    labels = ["Sexe", "Année", "Mois", "Département/pays",
              "Commune/pays", "Num. ordre", "Clé"]
    exp_parts = [exp[0], exp[1:3], exp[3:5], exp[5:7],
                 exp[7:10], exp[10:13], exp[13:15]]
    act_parts = [act[0], act[1:3], act[3:5], act[5:7],
                 act[7:10], act[10:13], act[13:15]]

    diffs = [f"{lab} ({a}≠{e})"
             for lab, a, e in zip(labels, act_parts, exp_parts) if a != e]

    return "Différence ❌ : " + ", ".join(diffs)

# ───────────────────────────────────────── Exécution principale ──
def main():
    if not FICHIER_ENTREE.exists():
        sys.exit(f"❌ Fichier {FICHIER_ENTREE} introuvable.")

    # Lecture CSV
    df = pd.read_csv(FICHIER_ENTREE, dtype=str).fillna("")

    # Calculs
    df["nir_attendu"] = df.apply(nir_attendu, axis=1)
    df["résultat"]    = df.apply(comparer, axis=1)

    # Sauvegarde
    df.to_csv(FICHIER_SORTIE, index=False, encoding="utf-8-sig")
    print(f"✅ Vérification terminée – résultat écrit dans {FICHIER_SORTIE}")

    # Compte‑rendu synthétique
    nb_ok  = df["résultat"].str.startswith("Correspondance").sum()
    nb_ko  = len(df) - nb_ok
    print(f"   Lignes OK : {nb_ok}")
    print(f"   Lignes KO : {nb_ko}")

if __name__ == "__main__":
    main()
