// A generated but empty Allure report is not evidence that tests ran.
const fs = require('node:fs');
const path = require('node:path');
const folder = process.argv[2] || 'reports/allure-results';
try {
  const results = fs.readdirSync(folder).filter(name => name.endsWith('-result.json'));
  if (!results.length) throw new Error('Aucun resultat de test Allure disponible');
  const statuses = new Set(['passed', 'failed', 'broken', 'skipped', 'unknown']);
  const counts = {};
  for (const name of results) {
    const result = JSON.parse(fs.readFileSync(path.join(folder, name), 'utf8'));
    if (!result.uuid || !result.name || !statuses.has(result.status)) {
      throw new Error(`Resultat Allure incomplet : ${name}`);
    }
    counts[result.status] = (counts[result.status] || 0) + 1;
  }
  console.log(JSON.stringify({testResults: results.length, statuses: counts}));
} catch (error) {
  console.error(`Generation Allure impossible : ${error.message}`);
  process.exitCode = 1;
}
