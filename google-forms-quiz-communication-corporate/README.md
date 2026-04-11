# QCM Google Forms – Communication Corporate (exemple 5 questions)

Script : `script.gs`

Ce script Google Apps Script configure automatiquement un Google Form en mode
quiz avec 5 questions à choix multiple (1 point par question), toutes
obligatoires, avec feedback correct/incorrect.

## Pourquoi cette version évite le blocage Google
- Le script est prévu pour être collé **dans le formulaire lui-même**
  (Extensions > Apps Script).
- Il utilise `@OnlyCurrentDoc` + `FormApp.getActiveForm()`.
- Résultat : portée d'accès limitée au formulaire actif (`forms.currentonly`).

## Déploiement (4 étapes)
1. Aller sur `forms.new` et créer un formulaire vide.
2. Ouvrir **Extensions > Apps Script**.
3. Remplacer le contenu par `script.gs`.
4. Exécuter `remplirQuiz` puis autoriser l'accès au formulaire actif.

L'URL de partage du formulaire est affichée dans les journaux d'exécution.

## Ce que le script configure automatiquement
- Mode quiz activé (`setIsQuiz(true)`).
- Collecte des e-mails.
- 5 questions obligatoires (`setRequired(true)`).
- 1 point par question (5 points au total).
- Feedback ✅ correct et ❌ incorrect sur chaque question.
- Nettoyage des anciennes questions avant régénération.

## Réglages manuels à faire dans Google Forms
Ces options ne sont pas exposées par `FormApp` :
- Publication des notes (immédiate ou différée).
- Affichage des réponses incorrectes.
- Affichage des bonnes réponses.
- Affichage du nombre de points.
