# Diagnostic Selenium/Chrome

Le 5 octobre, les six scénarios échouaient avec `tab crashed` avant leurs assertions. Cette trace d'origine est conservée dans `../history/2026-10-05/ui/`.

Le 6 octobre, un lancement protégé n'a pas pu charger correctement les dépendances Python installées sous le compte Windows utilisateur. L'installation réseau avait aussi rencontré un refus de socket WinError 10013. Après autorisation de lancer les outils hors de cet environnement protégé, le test de connexion locale a réussi sans modifier ses assertions : 1 passed en 6,57 s (`diagnostic-local.log`).

La suite complète a ensuite réussi : 6 passed en 78,735 s. Les versions réelles figurent dans `environment.json`, et chaque test possède son journal ChromeDriver ainsi que des pièces jointes Allure. Le site Formy a été visité en ligne ; les deux scénarios locaux restent identifiés comme tels.

La cause exacte du plantage historique n'a pas été isolée par une expérience comparant tous les paramètres à l'identique. La conclusion établie est la réussite sur la configuration actuelle et l'absence de reproduction du plantage hors du lancement protégé. Aucun argument `--no-sandbox` n'a été nécessaire. La fixture ajoute des preuves techniques et garantit la fermeture du navigateur après exécution.

Reproduction depuis la racine du projet, après installation des dépendances et vérification des chemins Python/Chrome :

```powershell
$env:CHROME_BINARY = 'CHEMIN_REEL_VERS_CHROME.exe'
$env:CHROMEDRIVER = 'CHEMIN_REEL_VERS_CHROMEDRIVER.exe'
.\.venv\Scripts\python.exe -m pytest --clean-alluredir --alluredir=reports/allure-results --junitxml=reports/ui/junit.xml
node scripts/check-allure-results.cjs
npx --no-install allure generate reports/allure-results --clean -o reports/allure-html
```

Ces variables sont facultatives si Selenium Manager peut trouver/télécharger le navigateur et son pilote. Ne pas ignorer un refus d'autorisation : utiliser un environnement d'exécution autorisé. Référence : [diagnostic officiel ChromeDriver](https://developer.chrome.com/docs/chromedriver/help/chrome-doesnt-start).
