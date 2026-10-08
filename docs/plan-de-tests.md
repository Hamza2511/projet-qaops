# Plan de tests

Automatisation des tests et assurance qualité d’une application web
Projet de fin de module M11
Faculté des sciences Aïn Chock - Casablanca
Version du 6 octobre 2026

## Réalisé par : Abdouraman Hamza

## Périmètre et approche

Dix scénarios : six UI et quatre API. Quatre UI portent sur Formy ; deux compléments locaux couvrent la connexion et les iframes absents du catalogue Formy. Les plateformes UI et API sont indépendantes : cette campagne ne valide pas un système étudiant intégré.

| Campagne | Objectif et livrable |
| --- | --- |
| UI / Selenium | Interactions, attentes explicites, contexte navigateur. JUnit et Allure. |
| API / Newman | Contrat CRUD, HTTP, JSON, schémas. JUnit, HTML, synthèse JSON. |
| Performance | 50 utilisateurs JMeter ; GET/POST ; JTL, HTML et métriques. |
| Sécurité | ZAP passif ; qualification des alertes et recommandations. |

## Conditions d’entrée et de sortie

Entrée : réseau accessible, navigateur/pilote compatibles, outils installés et accès API vérifié. Sortie fonctionnelle : tous les scénarios applicables passent ; aucun incident technique n’est compté comme une réussite. Les limites connues sont consignées. Les données sont fictives et reproductibles.

Priorité haute : UI-01, UI-05 et CRUD API. Les cas sont indépendants. Campagne du 6 octobre 2026 : 6/6 UI réussis et 14/14 assertions API réussies. Les verdicts détaillés figurent avec chaque scénario ; sources : reports/ui/junit.xml et reports/api. La couverture négative se limite au refus de connexion locale.




# Scénarios UI / Formy

## UI-01 - Inscription Formy

Données et préconditions : /form ; Sara / Bennani / QA Engineer ; radio 2, checkbox 2, expérience 2, date 10/05/2026.

Procédure : Saisir les trois champs, sélectionner radio, case et expérience, saisir la date, cliquer Submit.

Critère de validation : Les sélections sont conservées avant envoi et le bandeau de succès contient « successfully submitted ». Cela ne prouve pas un enregistrement en base.
Résultat observé le 6 octobre 2026 : PASS - 21,114 s.

## UI-02 - Boutons et menu Formy

Données et préconditions : /buttons ; bouton Primary, menu Dropdown, premier lien.

Procédure : Cliquer Primary, ouvrir le menu, vérifier un lien visible, le sélectionner.

Critère de validation : Primary est cliquable ; le menu révèle un libellé non vide et se ferme après sélection. Aucun effet métier supplémentaire attendu.
Résultat observé le 6 octobre 2026 : PASS - 19,304 s.

## UI-03 - Fenêtre modale Formy

Données et préconditions : /modal ; bouton Open modal, fermeture Close.

Procédure : Ouvrir la modale, vérifier son titre, fermer avec le bouton dédié.

Critère de validation : La modale est visible, contient « Modal title », puis devient invisible. Attentes explicites de 15 secondes maximum.
Résultat observé le 6 octobre 2026 : PASS - 8,578 s.

## UI-04 - Alerte et nouvelle fenêtre

Données et préconditions : /switch-window ; texte attendu « This is a test alert! ».

Procédure : Déclencher l’alerte, vérifier son texte, accepter ; ouvrir la nouvelle fenêtre, basculer, vérifier le domaine, fermer et revenir.

Critère de validation : Alerte absente après acceptation ; exactement deux fenêtres pendant le test ; contenu visible dans la nouvelle fenêtre et retour au handle initial.
Résultat observé le 6 octobre 2026 : PASS - 7,120 s.




# Scénarios locaux et exploitation

## UI-05 - Connexion locale positive et négative

Données et préconditions : fixtures/index.html ; sara@example.test ; incorrect puis QaOps-demo-2026.

Procédure : Soumettre le mot de passe incorrect, vérifier le refus ; corriger le mot de passe et soumettre à nouveau.

Critère de validation : « Identifiants invalides », puis « Bienvenue Sara ». Fixture pédagogique uniquement : aucune authentification serveur ni couverture de sécurité de session.
Résultat observé le 6 octobre 2026 : PASS - 15,765 s.

## UI-06 - Gestion d’un iframe local

Données et préconditions : fixtures/index.html ; student-frame ; Sara Bennani.

Procédure : Entrer dans l’iframe, saisir et enregistrer le nom ; vérifier le résultat ; revenir au document principal.

Critère de validation : « Étudiant : Sara Bennani » dans le cadre ; titre principal accessible après default_content. Le contenu est embarqué en data URL pour Selenium distant.
Résultat observé le 6 octobre 2026 : PASS - 6,622 s.

## Performance : protocole de mesure

Plan JMeter : 50 threads, montée sur 30 secondes, une boucle GET/POST, pause de 2 secondes avant chaque requête. Total nominal : 100 requêtes. Mesurer moyenne, p95, débit et erreurs ; ventiler GET/POST. Objectifs proposés : p95 < 2 s, erreurs < 1 %. Répéter ensuite sur une cible maîtrisée pour une conclusion robuste.

## Sécurité : critères et preuves

Pour chaque alerte : conserver l’URL, la règle, le niveau de risque, la confiance et l’élément observé. La revue humaine confirme la pertinence. Un scan non exécuté ne vaut pas absence de vulnérabilité ; une politique CSP absente ne prouve pas une XSS.




# Scénarios API / Reqres

## API-01 - Liste des utilisateurs

Données et préconditions : GET /api/users?page=2 ; clé optionnelle via environnement.

Procédure : Envoyer GET avec le paramètre page=2 et analyser la réponse JSON.

Critère de validation : HTTP 200 ; Content-Type JSON ; page=2 ; liste non vide, taille ≤ per_page ; id entier, email valide, noms et avatar conformes au schéma.
Résultat observé le 6 octobre 2026 : PASS - HTTP 200, 450 ms.

## API-02 - Création d’un utilisateur

Données et préconditions : POST /api/users ; name=Sara Bennani, job=student.

Procédure : Envoyer le corps JSON et contrôler les champs retournés.

Critère de validation : HTTP 201 ; Content-Type JSON ; champs name/job identiques ; id chaîne non vide ; createdAt valide et schéma conforme.
Résultat observé le 6 octobre 2026 : PASS - HTTP 201, 245 ms.

## API-03 - Mise à jour d’un utilisateur

Données et préconditions : PUT /api/users/2 ; name=Sara Bennani, job=QA engineer.

Procédure : Envoyer les nouvelles valeurs et contrôler la réponse.

Critère de validation : HTTP 200 ; Content-Type JSON ; champs retournés identiques ; updatedAt est une date valide ; schéma conforme. Pas d’hypothèse de persistance.
Résultat observé le 6 octobre 2026 : PASS - HTTP 200, 166 ms.

## API-04 - Suppression d’un utilisateur

Données et préconditions : DELETE /api/users/2.

Procédure : Envoyer DELETE et examiner statut et taille du corps.

Critère de validation : HTTP 204 et corps vide. L’identifiant 2 est celui de la démo publique ; ne pas appliquer cette collection à des données réelles sans adaptation.
Résultat observé le 6 octobre 2026 : PASS - HTTP 204, 107 ms.




# Extensions et traçabilité

Les dix scénarios principaux UI-01 à UI-06 et API-01 à API-04 répondent au périmètre initial de 5 à 10 scénarios. Les quatre cas ci-dessous sont des extensions séparées, fournies dans postman/qaops-negative.collection.json.

| Extension | Données, contrôle et résultat réel |
| --- | --- |
| API-N01 | GET /users/23 : attendu 404, JSON vide, aucune donnée utilisateur. |
| API-N02 | GET /users?page=999 : attendu 200, page 999 et tableau data vide. |
| API-N03 | POST /login avec email seul : attendu 400, erreur JSON et aucun token. |
| API-N04 | POST /register avec email seul : attendu 400, erreur JSON, aucun id/token. |

## Résultat des extensions API

Tentative du 6 octobre à 23:26:16 UTC : quatre erreurs de transport, aucune réponse HTTP et aucune validation fonctionnelle acquise. Newman a exécuté huit assertions qui ont échoué, puis quatre scripts ont interrompu leurs contrôles faute de JSON. Les seize assertions prévues ne sont donc pas toutes atteintes. Conserver ce verdict BLOQUÉ ; relancer dans Jenkins après connexion et accès réseau.

## SEC-L01 : XSS local et correction

Lancer scripts/run-xss-lab.py avec le chemin de ZAP. Le serveur se lie uniquement à 127.0.0.1:18094. ZAP active uniquement la règle 40012. Critères : XSS trouvée sur /vulnerable, aucune alerte XSS sur /fixed. Le navigateur doit exécuter le marqueur sur la première page et afficher le code comme texte sur la seconde. Résultat : critères observés, code de sortie ZAP 0. Preuves : reports/security-local.

## Exécution CI

GitLab : sources publiées, syntaxe correcte, jobs bloqués par vérification d’identité. Alternative prévue par le sujet : Jenkinsfile Windows fourni. Jenkins local est démarré mais l’interface requiert une connexion ; aucun build Jenkins n’est déclaré exécuté. Collecter JUnit, Allure, console, URL de build et notification après exécution.


