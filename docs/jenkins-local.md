# Jenkins local : procédure reproductible

Le sujet autorise Jenkins local ou GitLab CI. Le `Jenkinsfile` Windows constitue
une alternative à la vérification GitLab. **État de cette livraison : script
préparé, Jenkins local démarré, connexion demandée ; aucun build Jenkins exécuté
ni validation de sa syntaxe par Jenkins obtenue.**

1. Se connecter à l'installation Jenkins locale, puis créer un job de type Pipeline.
2. Copier le contenu du `Jenkinsfile` dans Pipeline script. Conserver le sandbox Groovy.
3. Renseigner les paramètres : `SOURCE_DIR` = dossier extrait du projet ;
   `PYTHON_BIN` = Python 3.12 ; `NODE_DIR` si Node/npm sont absents du PATH ;
   `CHROME_BINARY` et éventuellement `CHROMEDRIVER` compatibles.
4. Vérifier que le compte exécutant le nœud Jenkins peut lire les sources et
   accéder aux registres Python/npm, à Formy et à Reqres. Une clé Reqres éventuelle
   doit venir des credentials Jenkins, jamais des fichiers publiés.
5. Lancer le build et conserver la console complète. Les anciennes preuves du
   dossier source ne sont jamais copiées : un dossier `run-N` reçoit les sources
   et produit de nouveaux rapports UI, API, API négatifs et Allure.
6. Consulter Tests/JUnit et les artefacts archivés. Télécharger le dossier Allure
   et le servir via HTTP. Vérifier les nombres, erreurs, dates et captures.
7. Le flux RSS natif du job expose les nouveaux états ; abonner un lecteur pour
   recevoir une notification. `NOTIFY_URL` permet en complément d'envoyer un POST
   JSON à un webhook préalablement autorisé. Vide, aucun webhook n'est contacté.
   Une ligne de console ou un fichier de notification ne prouve pas une réception :
   conserver la preuve côté lecteur ou destinataire.

Plugins requis : Pipeline (dont Declarative et Durable Task/PowerShell), JUnit.
Java doit être disponible pour Allure. Aucune installation de plugins ni
modification de la sécurité Jenkins n'a été effectuée par cette livraison.

## Critères de clôture

- Nouveau build contenant six vrais tests UI et les quatre requêtes CRUD.
- Extensions : quatre requêtes et seize assertions prévues, statut réel à vérifier.
- Un échec métier ou technique doit rendre le build non vert.
- JUnit, captures, résultats Allure et HTML produits pendant ce build.
- URL/numéro du build, version des sources et preuve de notification reçue.

Référence : https://www.jenkins.io/doc/book/pipeline/syntax/
