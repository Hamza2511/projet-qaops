// Jenkins local Windows : copier les sources puis exécuter de nouveaux tests.
// Prérequis Jenkins : Pipeline, PowerShell (durable task), JUnit.
pipeline {
  agent any
  options {
    skipDefaultCheckout(true)
    disableConcurrentBuilds()
    timeout(time: 20, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
  }
  parameters {
    string(name: 'SOURCE_DIR', defaultValue: '', description: 'Dossier local du projet extrait ; ne contient aucun secret.')
    string(name: 'PYTHON_BIN', defaultValue: 'python', description: 'Chemin du Python 3.12 installé sur le nœud Jenkins.')
    string(name: 'NODE_DIR', defaultValue: '', description: 'Dossier contenant node.exe et npm.cmd si absents du PATH.')
    string(name: 'CHROME_BINARY', defaultValue: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', description: 'Chrome du nœud Windows.')
    string(name: 'CHROMEDRIVER', defaultValue: '', description: 'Pilote compatible facultatif ; sinon Selenium Manager.')
    string(name: 'NOTIFY_URL', defaultValue: '', description: 'Webhook de notification autorisé, facultatif ; vide = notification Jenkins RSS uniquement.')
  }
  stages {
    stage('Préparation') {
      steps {
        script { env.RUN_DIR = "run-${env.BUILD_NUMBER}" }
        powershell '''
          $ErrorActionPreference = 'Stop'
          if (-not $env:SOURCE_DIR -or -not (Test-Path -LiteralPath $env:SOURCE_DIR)) { throw 'SOURCE_DIR doit désigner le dossier du projet.' }
          $qaTarget = Join-Path $env:WORKSPACE $env:RUN_DIR
          New-Item -ItemType Directory -Path $qaTarget -Force | Out-Null
          foreach ($qaName in @('tests','fixtures','scripts','postman','security','requirements.txt','pytest.ini','package.json','package-lock.json')) {
            Copy-Item -LiteralPath (Join-Path $env:SOURCE_DIR $qaName) -Destination $qaTarget -Recurse -Force
          }
          Set-Location -LiteralPath $qaTarget
          if ($env:NODE_DIR) { $env:PATH = $env:NODE_DIR + ';' + $env:PATH }
          & $env:PYTHON_BIN -m venv .venv
          if ($LASTEXITCODE -ne 0) { throw 'Création venv échouée' }
          & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
          if ($LASTEXITCODE -ne 0) { throw 'Installation Python échouée' }
          & npm.cmd ci --no-audit --no-fund
          if ($LASTEXITCODE -ne 0) { throw 'Installation Node échouée' }
        '''
      }
    }
    stage('Selenium UI') {
      steps {
        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
          dir("${env.RUN_DIR}") {
            powershell '''
              & .\.venv\Scripts\python.exe -m pytest --clean-alluredir --alluredir=reports/allure-results --junitxml=reports/ui/junit.xml
              exit $LASTEXITCODE
            '''
          }
        }
      }
    }
    stage('API CRUD et cas négatifs') {
      steps {
        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
          dir("${env.RUN_DIR}") {
            powershell '''
              if ($env:NODE_DIR) { $env:PATH = $env:NODE_DIR + ';' + $env:PATH }
              & node scripts/run-api.cjs
              $qaCrudCode = $LASTEXITCODE
              & node scripts/run-api.cjs --negative
              if ($LASTEXITCODE -ne 0 -or $qaCrudCode -ne 0) { exit 1 }
            '''
          }
        }
      }
    }
    stage('Rapport Allure') {
      steps {
        dir("${env.RUN_DIR}") {
          powershell '''
            if ($env:NODE_DIR) { $env:PATH = $env:NODE_DIR + ';' + $env:PATH }
            & node scripts/check-allure-results.cjs
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
            & .\node_modules\.bin\allure.cmd generate reports/allure-results --clean -o reports/allure-html
            exit $LASTEXITCODE
          '''
        }
      }
    }
  }
  post {
    always {
      script {
        if (env.RUN_DIR) {
          junit testResults: "${env.RUN_DIR}/reports/**/junit.xml", allowEmptyResults: false
          archiveArtifacts artifacts: "${env.RUN_DIR}/reports/**", allowEmptyArchive: false, fingerprint: true
        }
        // Le flux RSS natif du job contient automatiquement son nouvel état.
        echo "Notification Jenkins : ${env.JOB_NAME} #${env.BUILD_NUMBER} ${currentBuild.currentResult} - ${env.BUILD_URL}"
        if (params.NOTIFY_URL?.trim()) {
          withEnv(["QAOPS_RESULT=${currentBuild.currentResult}"]) {
            powershell '''
              $qaPayload = @{job=$env:JOB_NAME; build=$env:BUILD_NUMBER; result=$env:QAOPS_RESULT; url=$env:BUILD_URL} | ConvertTo-Json
              Invoke-RestMethod -Method Post -Uri $env:NOTIFY_URL -ContentType 'application/json' -Body $qaPayload -TimeoutSec 10 | Out-Null
            '''
          }
        }
      }
    }
  }
}
