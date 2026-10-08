# État des exécutions - 6 octobre 2026

Réalisé par : **Abdouraman Hamza**.

| Domaine | Résultat réellement observé | Preuve |
|---|---|---|
| UI | 6 tests réussis, 0 échec, 0 erreur, 0 ignoré ; durée Pytest 78,735 s | ui/execution.log, ui/junit.xml, ui/environment.json |
| Allure | 6 résultats PASS ; HTML généré et chargé dans Chrome ; tableau de bord 100 % | allure-results/, allure-html/, ui/allure-overview.png, ci/allure-render-validation.json |
| API | Nouvelle campagne : 4 requêtes, 14 assertions réussies, moyenne affichée 242 ms | api/summary.json, api/execution.log, api/report.html, api/junit.xml |
| Performance | Campagne du 5 octobre conservée : 50 utilisateurs configurés, 100 requêtes, p95 8 677 ms, 16 % d'erreurs HTTP 429 | performance/results.jtl, performance/summary.json, performance/html/ |
| Sécurité | Scan ZAP passif du 5 octobre conservé : 14 catégories, 4 moyennes, 6 faibles, 4 informatives, aucune haute | security/zap.json, security/zap.html, security/execution.log |
| CI/CD | Syntaxe CI acceptée par GitLab ; pipeline #2919817204 créé puis bloqué par la vérification d’identité, zéro job exécuté | .gitlab-ci.yml, ci/ |
| Publication/notifications | Sources publiées ; notifications personnelles CI configurées, réception non testée | ci/gitlab/status.json et captures |

## UI : preuve de reprise et périmètre

Début JUnit : 2026-10-06T08:09:27.313528+00:00. Python 3.12.14, Selenium 4.27.1, Chrome 153.0.8010.50, ChromeDriver 153.0.8010.52, Windows 11. Quatre scénarios visitent le vrai site Formy ; deux utilisent les fixtures pédagogiques de connexion et d'iframe. Aucun scénario n'a été ignoré. Les assertions fonctionnelles sont inchangées.

Le diagnostic préalable de connexion locale a réussi (1 test en 6,57 s) lors d'un lancement autorisé hors de l'environnement protégé. Le plantage historique « tab crashed » n'a pas été reproduit ; sa cause précise n'est pas isolée formellement. La nouvelle fixture enregistre versions, journaux ChromeDriver et captures Allure, puis ferme le navigateur après exécution. Elle ne désactive plus implicitement la protection interne de Chrome lorsque CI est défini.

Les anciens échecs UI restent dans history/2026-10-05/ui/. Les résultats actuels remplacent ceux de la campagne initiale dans les dossiers principaux. Allure doit être servi en HTTP : npx --no-install allure open reports/allure-html.

## API : campagne actualisée

Synthèse horodatée 2026-10-06T08:10:52.344Z. GET 200 (450 ms), POST 201 (245 ms), PUT 200 (166 ms), DELETE 204 (107 ms), aucune assertion échouée. Les durées affichées par Newman sur une seule itération ne constituent pas une mesure de charge. L'ancienne campagne reste dans history/2026-10-05/api/.

## Performance : mesures conservées

Campagne initiale UTC du 5 octobre : premier départ à 16:44:52.888, dernière fin à 16:45:22.634. 50 GET HTTP 200 (p95 9 719 ms). Sur 50 POST, 34 HTTP 201 et 16 HTTP 429 (32 % d'échecs POST, p95 434 ms). Moyenne globale 1 328,81 ms ; débit 3,36 requêtes/s.

Les objectifs pédagogiques p95 < 2 s et erreurs < 1 % ne sont pas atteints. Les 429 indiquent une limitation du service et ne prouvent pas une régression fonctionnelle. Aucune nouvelle campagne de charge le 6 octobre.

## Sécurité : résultats conservés

Le spider ZAP a trouvé 103 URL. Les quatre catégories moyennes sont l'absence de jeton anti-CSRF sur /fileupload (confiance faible), CSP absente, SRI absent et jQuery 3.2.1 signalée vulnérable. Ce sont des alertes à qualifier, pas des exploitations démontrées. Aucun test XSS actif ni nouveau scan le 6 octobre. Le paramètre non reconnu numberOfThreads a été retiré du plan livré après le scan initial ; le journal conserve fidèlement l'avertissement.

## CI et actions restantes

Les commandes de test UI, API et génération Allure ont réellement réussi sous Windows. Contrôles locaux de configuration et de scripts : ci/. Node local 24.13.0, Java 21.0.11 ; les images GitLab Node 22/Python 3.12 et le service Selenium Grid n'ont pas été lancés. Docker n'avait pas de moteur actif. Les tests simulés du contrôle de disponibilité Selenium ne sont pas des tests UI supplémentaires.

Publication effectuée : https://gitlab.com/abdouraman011/projet-qaops. Commit 8d2e3a7f, 27 fichiers sources/documentation. GitLab confirme la syntaxe CI. Pipeline : https://gitlab.com/abdouraman011/projet-qaops/-/pipelines/2919817204. La simulation et les jobs sont bloqués par « Identity verification is required in order to run CI jobs ». Zéro job exécuté. Notifications personnelles échec/rétablissement/succès activées ; réception non testée. La vérification personnelle n’a pas été poursuivie. Elle reste nécessaire pour une exécution distante. Les PDF et preuves complètes sont inclus dans le ZIP de remise.

Le projet est validé localement pour les six scénarios UI et le contrat API testé. Les objectifs de performance ne sont pas atteints ; les alertes de sécurité restent à qualifier et la validation distante CI reste à réaliser.



## Compléments du 6 octobre en fin de journée UTC

XSS local : scan actif ZAP terminé avec code 0, règle 40012 positive sur /vulnerable et absente sur /fixed. Le navigateur a réellement exécuté le marqueur avant correction et l’a affiché comme texte après correction. Ce résultat ne concerne pas Formy. Preuves : security-local/.

API négative : quatre erreurs de transport, aucune réponse HTTP ; huit assertions atteintes ont échoué et les scripts JSON ont été interrompus. Les seize assertions prévues ne sont donc pas toutes exécutées. Verdict BLOQUÉ. Preuves : api-negative/.

Jenkinsfile préparé, service local démarré, connexion utilisateur requise ; aucun build exécuté ni syntaxe Jenkins validée. La conformité CI/CD reste partielle.
