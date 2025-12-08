# Vérification des numéros de sécurité sociale

Script : `script.py`

Calcule le NIR attendu pour chaque salarié listé dans `salariés.csv`, compare la
valeur saisie et indique les correspondances ou divergences. Un rapport détaillé
est écrit dans `salariés_verifiés.csv`.

## Prérequis
- Python 3
- `pandas`

## Préparation du fichier source
`salariés.csv` doit contenir les colonnes : `sexe`, `annee_naissance`,
`mois_naissance`, `departement`, `commune`, `num_ordre`, `nir_saisi`.

## Utilisation
```bash
python script.py
```
Un résumé du nombre de lignes conformes/erronées est affiché dans la console.
