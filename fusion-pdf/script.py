import os
from PyPDF2 import PdfMerger

# Initialiser le fusionneur de PDF
merger = PdfMerger()

# Lister et trier les fichiers PDF dans le répertoire courant
pdf_files = sorted([f for f in os.listdir('.') if f.lower().endswith('.pdf')])

# Ajouter chaque fichier PDF au fusionneur
for pdf in pdf_files:
    print(f"Ajout de {pdf}...")
    merger.append(pdf)

# Écrire le fichier fusionné
output_filename = "fusion.pdf"
merger.write(output_filename)
merger.close()

print(f"Fichier fusionné créé : {output_filename}")