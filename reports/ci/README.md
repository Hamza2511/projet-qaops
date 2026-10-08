# Validation CI locale - 6 octobre 2026

La configuration GitLab a été revue et corrigée. Aucune exécution distante n'est revendiquée.

## Exécutions réelles

- Commande UI : 6 tests réussis, JUnit et résultats Allure renouvelés.
- Commande API : 4 requêtes et 14 assertions réussies, JUnit/HTML/JSON renouvelés.
- Commande Allure : génération réussie ; HTML servi localement en HTTP et contrôlé dans Chrome, 6 cas et 100 % de réussite.
- 13 contrôles comportementaux des scripts auxiliaires réussis, 0 échec : 8 contrôles d'attente Selenium avec un petit serveur HTTP de test et 5 contrôles d'entrées Allure valides/absentes/invalides. Ce sont des tests des scripts, pas 13 scénarios UI supplémentaires.

Voir `local-validation.json` pour chaque contrôle et le SHA-256 de la configuration concernée. Les fichiers synthétiques des contrôles ont été isolés dans un dossier temporaire ; ils ne sont pas mélangés aux six résultats Selenium réels.

## Limites vérifiées

- La validation automatique YAML et la vérification des commandes shell restent non exécutées : PyYAML n'était pas accessible correctement au processus protégé. La configuration a fait l'objet d'une revue de son contenu, pas d'une certification CI Lint.
- Le moteur Docker n'était pas actif ; les images, le service Grid, le réseau interconteneurs et l'ordonnancement GitLab ne sont pas validés.
- Aucun identifiant GitLab stocké n'était disponible via Git Credential Manager. La vérification du compte vue sur la capture utilisateur reste une action utilisateur.
- Aucun pipeline GitLab, téléversement d'artefacts GitLab ou envoi de notifications n'a été vérifié.

Les tests de composants ont utilisé Windows, Python 3.12.14, Node 24.13.0 et Java 21.0.11. Les images prévues par le pipeline utilisent Python 3.12, Node 22 et Selenium Standalone Chrome ; une exécution sur runner reste nécessaire.

## Modifications

Artefacts ciblés par job et suppression des anciennes sorties ; disponibilité Selenium fondée sur `value.ready=true`, délai borné et erreur explicite ; garde Allure contre les résultats absents/invalides ; ZAP activé seulement par `RUN_SECURITY=1`, avec conservation des codes et rapports. Le code ZAP 2 est toléré, les codes 1/3 restent bloquants.
