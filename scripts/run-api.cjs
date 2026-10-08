const newman = require('newman');
const fs = require('fs');
const negative = process.argv.includes('--negative');
const reportDir = negative ? 'reports/api-negative' : 'reports/api';
fs.mkdirSync(reportDir, {recursive:true});
newman.run({
 collection: require(negative ? '../postman/qaops-negative.collection.json' : '../postman/qaops.collection.json'),
 environment: require('../postman/reqres.environment.json'),
 envVar: [{key:'base_url', value:process.env.API_BASE_URL || 'https://reqres.in/api'}, {key:'api_key', value:process.env.REQRES_API_KEY || ''}],
 reporters: ['cli','junit','htmlextra'],
 reporter: {junit:{export:reportDir+'/junit.xml'}, htmlextra:{export:reportDir+'/report.html',skipSensitiveData:true}},
 timeoutRequest: 15000, timeout: 120000, delayRequest: 500
}, (err, summary) => {
 if (err) {console.error(err.message);process.exitCode=1;return;}
 // Ne jamais exporter la collection résolue : elle peut contenir la clé API.
 const result={date:new Date().toISOString(),target:process.env.API_BASE_URL || 'https://reqres.in/api',stats:summary.run.stats,failures:summary.run.failures.map(f=>({source:f.source.name,error:f.error.message}))};
 result.campaign = negative ? 'negative-and-boundary' : 'CRUD';
 result.outcome = summary.run.stats.requests.failed ? 'blocked_transport' : summary.run.failures.length ? 'failed_assertions' : 'passed';
 result.executions = summary.run.executions.map(e=>({name:e.item.name,method:e.request.method,status:e.response?.code,response_ms:e.response?.responseTime,assertions:(e.assertions||[]).map(a=>({name:a.assertion,passed:!a.error}))}));
 fs.writeFileSync(reportDir+'/summary.json',JSON.stringify(result,null,2));
 process.exitCode=summary.run.failures.length?1:0;
});
