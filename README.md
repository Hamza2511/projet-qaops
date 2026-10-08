# Projet QAOps - automatisation et assurance qualité

Projet du module M11, Université Hassan II, Faculté des sciences Aïn Chock.
Réalisé par : **Abdouraman Hamza**.
Les résultats effectivement mesurés et les limites figurent dans `reports/etat-executions.md` et le rapport PDF. Aucun résultat attendu n'est présenté comme un succès observé.

## Résultats vérifiés le 6 octobre 2026

- UI : **6 tests réussis**, aucun échec/erreur/test ignoré, en 78,735 s (4 Formy + 2 compléments locaux).
- API : **4 requêtes et 14 assertions réussies** lors de la nouvelle campagne Newman.
- Allure et JUnit régénérés ; les preuves du 5 octobre restent dans `reports/history/2026-10-05/`.
- CI : commandes UI/API/Allure réussies sous Windows. GitLab confirme la syntaxe CI ; le pipeline #2919817204 est bloqué par la vérification d’identité, avec zéro job exécuté.
- Mesures JMeter et ZAP conservées du 5 octobre : p95 8 677 ms et 16 % de HTTP 429 ; 14 catégories d'alertes ZAP, dont 4 moyennes. Les seuils de performance ne sont pas atteints.
- Sources publiées sur [GitLab](https://gitlab.com/abdouraman011/projet-qaops). Notifications personnelles d’échec, de rétablissement et de succès configurées ; réception non testée.

## Compléments de la livraison renforcée

- Laboratoire XSS local exécuté : ZAP détecte la vulnérabilité sur `/vulnerable` et ne la retrouve pas sur `/fixed`. Le navigateur confirme le code exécuté puis neutralisé. Preuves : `reports/security-local/` ; lancement : `python scripts/run-xss-lab.py --zap-jar CHEMIN_ZAP_JAR --work-dir CHEMIN_TRAVAIL`.
- Rapport final : **10 pages**, avec capture Allure, graphique JMeter et deux captures XSS. Plan de tests : **5 pages**, dix scénarios principaux et quatre extensions distinctes.
- API négative : quatre cas et seize assertions prévues ; tentative bloquée par quatre erreurs de transport, sans réponse HTTP. **Aucune réussite ajoutée aux quatorze assertions CRUD déjà validées**. Commande : `npm run test:api:negative`.
- `Jenkinsfile` Windows ajouté. Jenkins est démarré mais exige une connexion à http://127.0.0.1:8080 ; aucun build exécuté. Procédure : `docs/jenkins-local.md`.
- Exigences et preuves rapprochées dans `docs/matrice-conformite.md`. Le pipeline fonctionnel reste à démontrer ; aucune note de 20/20 n'est promise.

## Contenu

- `tests/ui` : 6 scénarios Selenium/Pytest, captures Allure et versions réelles du navigateur/pilote.
- `fixtures` : connexion et iframe locaux, compléments distincts du site Formy.
- `postman` : 4 scénarios CRUD et environnement exportables dans Postman.
- `performance/reqres.jmx` : plan JMeter, 50 utilisateurs, GET et POST.
- `security` : configuration ZAP passive ; aucun test XSS actif sur le site public.
- `.gitlab-ci.yml` : UI/API, JUnit, génération Allure, ZAP sur lancement explicite avec `RUN_SECURITY=1`.
- `docs` : plan de tests, rapport final et sources Markdown modifiables.
- `reports` : traces réelles des exécutions et état de validation.

## Installation et tests UI

Prérequis : Python 3.12, Node.js 22+, Chrome ; Java 17+ pour Allure/JMeter, Java 17+ ou version exigée par votre ZAP. Internet requis pour les sites publics et le téléchargement du pilote Selenium.

Depuis ce dossier, dans PowerShell :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm ci
.\.venv\Scripts\python.exe -m pytest --clean-alluredir --alluredir=reports/allure-results --junitxml=reports/ui/junit.xml
node scripts/check-allure-results.cjs
npx --no-install allure generate reports/allure-results --clean -o reports/allure-html
npx allure open reports/allure-html
```

Sous Linux, utiliser `python3 -m venv .venv`, puis `.venv/bin/python`.
Pour les seuls compléments locaux : ajouter `-m local` à pytest ; pour Formy : `-m formy`.
Un pilote Chrome peut être fourni via `CHROMEDRIVER`, un navigateur via `CHROME_BINARY`, ou un serveur Selenium via `SELENIUM_REMOTE_URL`.
Vérifier que le chemin indiqué par `py -3.12` existe réellement ; sinon utiliser le chemin d'un Python 3.12 installé. L'exécution vérifiée utilise Python 3.12.14, Selenium 4.27.1, Chrome 153.0.8010.50 et ChromeDriver 153.0.8010.52. Node.js 24.13.0 et Java 21.0.11 ont servi à Newman/Allure ; les images CI utilisent Node.js 22 et Python 3.12.

Le plantage historique `tab crashed` n'a pas été reproduit lors de la nouvelle exécution autorisée hors du lancement protégé. Sa cause exacte n'est pas formellement isolée. Les assertions fonctionnelles n'ont pas été assouplies ; la fixture conserve la protection interne de Chrome et ajoute des journaux, captures et versions pour faciliter le diagnostic. Voir `reports/ui/diagnostic.md`.

## API / Postman / Newman

Importer les deux fichiers JSON de `postman` dans Postman, choisir l'environnement, puis exécuter la collection.
La documentation Reqres distingue mal, selon les pages, la démo anonyme et les API avec clé. Le projet conserve les chemins du sujet (`/api/users`) et permet de fournir une clé personnelle si l'accès l'exige.

```powershell
$env:REQRES_API_KEY = 'votre-cle-si-necessaire'
npm run test:api
```

Ne pas committer de clé ; laisser la valeur exportée vide. Les rapports excluent les détails sensibles. Rapports : `reports/api/report.html`, `summary.json`, `junit.xml`. Un HTTP 401/403/429 fait échouer le test et doit être analysé avant toute charge.
Le contrat attendu est celui des endpoints de démonstration historiques : POST/PUT renvoient les champs reçus, DELETE renvoie 204. Ne pas interpréter ces réponses comme une preuve de persistance métier.

## Performance avec JMeter 5.6.3

Vérifier d'abord le succès du test API simple et la compatibilité du quota avec 100 requêtes au minimum. Sur la plateforme publique, convenir de la fenêtre de charge et de la limite de débit avec l'encadrant / l'exploitant. Le plan utilise 50 threads, une montée en charge de 30 secondes, une itération et une pause de 2 secondes avant chaque requête. C'est une première mesure courte, pas un test d'endurance ni la preuve de 50 connexions simultanément actives.

```powershell
New-Item -ItemType Directory -Force reports/performance
jmeter -n -t performance/reqres.jmx -l reports/performance/results.jtl -e -o reports/performance/html -Jusers=50 -Jramp=30 -Jloops=1
.\.venv\Scripts\python.exe scripts/analyze_performance.py reports/performance/results.jtl reports/performance/summary.json
```

Le dossier HTML de destination doit être absent ou vide à chaque nouvelle campagne. Conserver les anciennes campagnes dans un autre dossier, ne pas les écraser. Configurer `-Jhost`, `-Jport`, `-Jprotocol` pour une cible de préproduction compatible. La clé provient de l'environnement `REQRES_API_KEY`. Seuils pédagogiques : p95 < 2 000 ms et erreurs < 1 %. Un 429 est une erreur de quota, pas la preuve d'une régression applicative. Les métriques portent sur l'ensemble et séparément sur GET/POST.

## Sécurité avec ZAP

Option Docker (démarrer Docker Desktop au préalable) :

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-security.ps1
```

Codes du baseline : 0 = aucune alerte, 1 = règle FAIL, 2 = avertissements, 3 = erreur d'exécution. Ne pas masquer les codes avec `|| true`. Dans GitLab, seul le code 2 est toléré avec avertissement. Les fichiers HTML/JSON/Markdown sont conservés.

Alternative sans Docker, utilisée pour le rapport fourni : télécharger ZAP Crossplatform 2.17.0, puis depuis son dossier lancer `java -Xmx512m -jar zap-2.17.0.jar -cmd -port 18091 -dir CHEMIN_DOSSIER_ZAP -autorun CHEMIN_ABSOLU/security/passive.yaml`. Choisir un dossier de travail accessible et un port libre. Le plan passif produit les rapports HTML/JSON dans `reports/security`. Ses codes sont 0 (aucune alerte moyenne/haute), 1 (alerte haute) et 2 (alerte moyenne) ; ces codes ne sont pas ceux du script baseline Docker.
Un scan passif peut relever des en-têtes absents ; il ne démontre pas l'exploitabilité d'une XSS. Une validation active nécessite un environnement contrôlé et un périmètre autorisé. Utiliser les observations du rapport ZAP, vérifier les faux positifs, puis documenter URL, preuve, risque et correction.

## GitLab CI et notifications

Le dépôt privé est publié : [Projet QAOps](https://gitlab.com/abdouraman011/projet-qaops).
Les 27 fichiers sources et documents Markdown ont été transférés via le Web IDE,
commit `8d2e3a7f`. Le ZIP de remise contient en plus les PDF et toutes les preuves locales.

GitLab affiche **Pipeline syntax is correct**. Le [pipeline #2919817204](https://gitlab.com/abdouraman011/projet-qaops/-/pipelines/2919817204)
et la simulation ont été refusés avec **Identity verification is required in order to run CI jobs**.
**Zéro job distant exécuté** : ce blocage de compte ne constitue ni une réussite ni un échec des assertions de tests.
Les captures et l’état exact sont conservés dans `reports/ci/gitlab/`.

Les notifications personnelles GitLab `Pipeline fails`, `Pipeline is fixed` et
`Pipeline is successful` sont activées. Aucun courriel reçu n’a été vérifié.
Pour terminer la validation distante, la vérification personnelle GitLab reste nécessaire,
puis un nouveau pipeline et le contrôle des artefacts et de la réception des notifications.

Les jobs UI/API sont bloquants ; Allure refuse des résultats absents et conserve ses artefacts 30 jours.
Le scan ZAP est optionnel (`RUN_SECURITY=1`) ; seul son code 2 est toléré.
Une clé `REQRES_API_KEY` masquée peut être nécessaire selon l’accès Reqres depuis le runner.
Aucun secret n’est livré. Les contrôles locaux et les versions Windows ne valident pas les images Docker CI.

## Limites de périmètre

Formy et Reqres sont deux démonstrateurs indépendants. Ils ne constituent pas une application de gestion d'étudiants connectée de bout en bout. Le formulaire Formy démontre une soumission UI ; le CRUD démontre le contrat API. La fixture de connexion expose volontairement ses identifiants dans le code et n'est pas une implémentation d'authentification de production.

## Références officielles

- https://formy-project.herokuapp.com/
- https://reqres.in/docs
- https://www.selenium.dev/documentation/webdriver/
- https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/
- https://jmeter.apache.org/usermanual/get-started.html
- https://www.zaproxy.org/docs/docker/baseline-scan/
- https://docs.gitlab.com/ci/testing/unit_test_reports/
- https://docs.gitlab.com/user/project/integrations/pipelines_email/

Préparation initiale : 5 octobre 2026. Reprise et vérifications locales : 6 octobre 2026.
