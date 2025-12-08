import os
import tkinter as tk
from tkinter import filedialog

def afficher_arborescence(dossier, prefix=""):
    """Affiche récursivement la structure du dossier"""
    fichiers_et_dossiers = sorted(os.listdir(dossier))
    for i, element in enumerate(fichiers_et_dossiers):
        chemin_complet = os.path.join(dossier, element)
        # Déterminer le préfixe pour l'arborescence
        is_last = (i == len(fichiers_et_dossiers) - 1)
        branche = "└── " if is_last else "├── "
        print(prefix + branche + element)
        # Si c’est un dossier, descendre récursivement
        if os.path.isdir(chemin_complet):
            nouveau_prefix = prefix + ("    " if is_last else "│   ")
            afficher_arborescence(chemin_complet, nouveau_prefix)

def choisir_dossier():
    """Ouvre une boîte de dialogue pour choisir un dossier"""
    root = tk.Tk()
    root.withdraw()  # cache la fenêtre principale
    dossier = filedialog.askdirectory(title="Choisir un dossier")
    return dossier

if __name__ == "__main__":
    dossier = choisir_dossier()
    if dossier:
        print(f"\nStructure du dossier : {dossier}\n")
        afficher_arborescence(dossier)
    else:
        print("Aucun dossier sélectionné.")
