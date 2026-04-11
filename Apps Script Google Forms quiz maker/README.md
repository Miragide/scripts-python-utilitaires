# Apps Script Google Forms quiz maker

Script : `script.gs`

Ce dossier contient un **modèle prêt à copier-coller** pour Google Apps Script
(permettant de remplir automatiquement un Google Form en mode quiz).

Objectif principal : fournir une base de code à donner à une IA afin qu'elle
génère automatiquement un script pour **n'importe quel QCM décrit en langage
naturel** (questions, choix, bonnes réponses, feedback).

## Positionnement du modèle
- Le script actuel contient un exemple concret de **5 questions**.
- La structure `questions` est le bloc à remplacer/générer par l'IA.
- Le reste (création des items, points, feedback, paramètres quiz) est
  générique et réutilisable.

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
- Questions obligatoires (`setRequired(true)`).
- 1 point par question (`setPoints(1)`).
- Feedback ✅ correct et ❌ incorrect sur chaque question.
- Nettoyage des anciennes questions avant régénération.

## Réglages manuels à faire dans Google Forms
Ces options ne sont pas exposées par `FormApp` :
- Publication des notes (immédiate ou différée).
- Affichage des réponses incorrectes.
- Affichage des bonnes réponses.
- Affichage du nombre de points.

## Exemple de prompt IA (recommandé)
> Voici mon modèle `script.gs` Google Forms.
> Garde la logique du script intacte.
> Remplace uniquement le tableau `questions` pour créer un QCM sur :
> [ton sujet].
> Je veux [N] questions, 4 choix par question, une seule bonne réponse,
> feedback pédagogique pour bonne/mauvaise réponse, niveau [débutant/intermédiaire/avancé].
