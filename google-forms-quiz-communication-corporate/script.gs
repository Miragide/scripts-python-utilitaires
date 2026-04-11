/**
 * QCM – Communication Corporate (exemple 5 questions)
 *
 * ═══════════════════════════════════════════════════════════════
 * PROCÉDURE (évite le blocage de permissions) :
 *  1. Créer un Google Form VIDE à l'adresse : forms.new
 *  2. Dans le formulaire : Extensions > Apps Script
 *  3. Remplacer tout le code par ce fichier
 *  4. Cliquer sur ▶ Exécuter > remplirQuiz
 *  5. Autoriser uniquement l'accès au formulaire actif
 * ═══════════════════════════════════════════════════════════════
 *
 * @OnlyCurrentDoc  ← annotation clé : limite les permissions
 *                    au seul formulaire ouvert (forms.currentonly)
 */

/** @OnlyCurrentDoc */
function remplirQuiz() {
  // Récupère le formulaire dans lequel le script est intégré
  const form = FormApp.getActiveForm();

  // ── Paramètres globaux ────────────────────────────────────────────────────
  form.setTitle("QCM – Communication Corporate");
  form.setDescription(
    "5 questions sur la communication corporate, l'image de marque, " +
    "la gestion de crise et la stratégie digitale.\n" +
    "Toutes les réponses sont obligatoires."
  );
  form.setIsQuiz(true);
  form.setCollectEmail(true);

  // Supprime les items existants si le script est relancé
  form.getItems().forEach(item => form.deleteItem(item));

  // ── Helper feedback ───────────────────────────────────────────────────────
  function fb(text) {
    return FormApp.createFeedback().setText(text).build();
  }

  // ── Données des 5 questions ───────────────────────────────────────────────
  // Format : { t: titre, c: [[texte, estCorrect], …], ok: feedback ✅, ko: feedback ❌ }
  const questions = [
    {
      t: "1. Quelle est la principale distinction entre la communication corporate et la communication marketing ?",
      c: [
        ["A. La communication corporate valorise l'entreprise comme entité globale plutôt que ses produits.", true],
        ["B. La communication corporate s'adresse uniquement aux salariés internes.", false],
        ["C. La communication corporate n'utilise jamais les médias digitaux.", false],
        ["D. La communication corporate a pour seul objectif de générer des ventes immédiates.", false],
      ],
      ok: "✅ La communication corporate se concentre sur l'identité, les valeurs et la réputation de l'organisation dans son ensemble.",
      ko: "❌ La communication corporate valorise l'entreprise comme entité globale — elle ne se limite ni aux salariés, ni aux ventes, et utilise tous les médias disponibles."
    },
    {
      t: "2. Quel document est considéré comme la référence pour synthétiser les données financières et stratégiques d'une organisation ?",
      c: [
        ["A. La charte graphique.", false],
        ["B. Le communiqué de presse.", false],
        ["C. Le registre du commerce.", false],
        ["D. Le rapport annuel (ou rapport intégré).", true],
      ],
      ok: "✅ Ce document est la pièce maîtresse pour comprendre la santé globale et la vision d'une entreprise.",
      ko: "❌ La charte régit l'identité visuelle, le communiqué est ponctuel, et le registre contient uniquement des données légales de base. Seul le rapport annuel synthétise données financières ET stratégiques."
    },
    {
      t: "3. Dans le modèle du 'Golden Circle' de Simon Sinek, par quoi une organisation devrait-elle commencer son discours pour générer de l'adhésion ?",
      c: [
        ["A. Le What (Quoi).", false],
        ["B. Le Budget (Combien).", false],
        ["C. Le Why (Pourquoi).", true],
        ["D. Le How (Comment).", false],
      ],
      ok: "✅ Commencer par la raison d'être profonde permet de créer un lien émotionnel et de l'engagement.",
      ko: "❌ Sinek démontre que les organisations inspirantes commencent par le WHY (raison d'être), et non par ce qu'elles font ou comment elles le font."
    },
    {
      t: "4. Depuis la loi PACTE de 2019, que peuvent inscrire les sociétés françaises dans leurs statuts ?",
      c: [
        ["A. La liste complète de leurs clients.", false],
        ["B. Une raison d'être (purpose).", true],
        ["C. Un nouveau logo.", false],
        ["D. Leur chiffre d'affaires prévisionnel.", false],
      ],
      ok: "✅ Cette loi permet de formaliser la contribution de l'entreprise à la société au-delà du profit.",
      ko: "❌ La loi PACTE permet d'inscrire une raison d'être dans les statuts — pas des données clients, visuelles ou financières prévisionnelles."
    },
    {
      t: "5. Selon Edgar Schein, quel niveau de la culture d'entreprise comprend les éléments visibles comme les locaux ou le code vestimentaire ?",
      c: [
        ["A. Le prisme d'identité.", false],
        ["B. Les valeurs affichées.", false],
        ["C. Les artefacts.", true],
        ["D. Les hypothèses de base.", false],
      ],
      ok: "✅ Les artefacts sont les manifestations physiques et tangibles de la culture au quotidien.",
      ko: "❌ Le prisme est un outil de Kapferer. Les valeurs affichées sont dans les chartes. Les hypothèses de base sont inconscientes. Seuls les artefacts sont visibles physiquement."
    }
  ];

  // ── Génération des questions dans le formulaire ───────────────────────────
  questions.forEach(q => {
    const item = form.addMultipleChoiceItem();
    item
      .setTitle(q.t)
      .setRequired(true)
      .setPoints(1)
      .setChoices(
        q.c.map(([text, isCorrect]) => item.createChoice(text, isCorrect))
      );
    item.setFeedbackForCorrect(fb(q.ok));
    item.setFeedbackForIncorrect(fb(q.ko));
  });

  Logger.log("✅ 5 questions ajoutées avec succès !");
  Logger.log("🔗 URL de partage : " + form.getPublishedUrl());
}

/**
 * ═══════════════════════════════════════════════════════════════
 * PARAMÈTRES À ACTIVER MANUELLEMENT (Forms > ⚙️ Paramètres)
 * ═══════════════════════════════════════════════════════════════
 * Onglet "Questionnaire" :
 *   • Publication des notes : "Immédiatement après chaque envoi"
 *                          ou "Plus tard, après examen manuel"
 *
 * Onglet "Questionnaire" > Paramètres des personnes interrogées :
 *   ☑ Questions avec réponses incorrectes
 *   ☑ Bonnes réponses (visibles après communication des notes)
 *   ☑ Nombre de points (total et par question)
 * ═══════════════════════════════════════════════════════════════
 */
