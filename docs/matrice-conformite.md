# Matrice de conformité au sujet M11

Auteur : **Abdouraman Hamza**. Les pondérations viennent du sujet ; aucune note
n'est prédite. Le respect des délais dépend de la date réelle de remise.

| Exigence | Preuve | État et limite |
|---|---|---|
| 5 à 10 scénarios, données et critères | plan-de-tests.pdf, UI-01 à UI-06 et API-01 à API-04 | 10 scénarios principaux documentés |
| Selenium : formulaire, boutons, fenêtres, alertes, listes et radios | tests/ui/test_formy.py, reports/ui/junit.xml | 4 scénarios Formy réussis |
| Login et iframe | tests/ui/test_local.py, fixtures/ | 2 scénarios locaux réussis ; compléments pédagogiques, pas des pages Formy |
| Rapports Allure | reports/allure-results, reports/allure-html, reports/ui/allure-overview.png | 6/6 réussis, HTML ouvert et vérifié |
| Reqres CRUD : HTTP, JSON, schémas | postman/qaops.collection.json, reports/api/ | 4 requêtes et 14 assertions réussies, campagne datée |
| Extensions de couverture API | postman/qaops-negative.collection.json, reports/api-negative/ | 4 cas fournis ; tentative bloquée au transport, aucun PASS |
| Au moins 50 utilisateurs GET/POST | performance/reqres.jmx, reports/performance/results.jtl | 50 utilisateurs configurés, 100 requêtes réellement mesurées |
| Analyse temps, débit, erreurs | summary.json, reports/figures/performance.pdf | p95 8 677 ms, 3,36 req/s, 16 % HTTP 429 ; seuils non atteints |
| Scan Formy avec ZAP | reports/security/zap.json et zap.html | 14 catégories dont 4 moyennes ; scan passif |
| Identification et correction XSS | security/xss_lab.py, reports/security-local/ | XSS locale détectée puis corrigée ; recontrôle ZAP et navigateur, aucune attribution à Formy |
| Recommandations de sécurité | rapport-final.pdf, page 6 et page 10 | Priorités, confiance, encodage de sortie et CSP ; propriétaire de Formy requis pour corriger le service |
| Pipeline UI + API fonctionnel | .gitlab-ci.yml, Jenkinsfile, reports/ci/gitlab/ | **Partiel** : GitLab bloque les jobs ; Jenkins préparé mais connexion requise |
| Rapports automatiques en CI | définitions GitLab/Jenkins | Prévus, non démontrés sur un build CI exécuté |
| Notifications automatiques | capture GitLab notifications.png, Jenkinsfile | GitLab configuré, réception non testée ; Jenkins RSS/webhook non testés |
| Scripts dans un dépôt Git | https://gitlab.com/abdouraman011/projet-qaops | Sources initiales publiées ; archive ZIP = livraison complète avec preuves |
| Collection exportable et plan PDF | postman/, docs/plan-de-tests.pdf | Fournis |
| Rapport final de 5 à 10 pages | docs/rapport-final.pdf | 10 pages, résultats réels et figures |

Pondération : UI/API 30 %, performance/sécurité 20 %, CI/CD 20 %, rapport 20 %,
délais 10 %. **Le manque de preuve CI empêche de déclarer une conformité complète.**
