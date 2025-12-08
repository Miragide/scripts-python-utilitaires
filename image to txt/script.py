import os
import easyocr
import pandas as pd
from PIL import Image

# Initialisation du lecteur avec le français
reader = easyocr.Reader(['fr'])

dossier = os.getcwd()
extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')

data = []

for fichier in os.listdir(dossier):
    if fichier.lower().endswith(extensions):
        chemin_image = os.path.join(dossier, fichier)
        print(f"Traitement de : {fichier}")

        try:
            resultats = reader.readtext(chemin_image, detail=0, paragraph=True)

            # Tous les textes concaténés avec virgules
            texte_concatene = ', '.join([txt.strip() for txt in resultats if txt.strip()])

            data.append({
                'nom_image': fichier,
                'texte': texte_concatene
            })

        except Exception as e:
            print(f"Erreur avec {fichier} : {e}")

# Export en CSV
df = pd.DataFrame(data)
df.to_csv('resultats_textes_easyocr.csv', index=False, encoding='utf-8-sig')

print("Extraction terminée. Résultats dans 'resultats_textes_easyocr.csv'")
