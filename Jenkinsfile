pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Navegador a usar'
        )
        choice(
            name: 'MARKERS',
            choices: ['', 'smoke', 'regression', 'elements'],
            description: 'Marcador de pytest (vacío = todos los tests)'
        )
    }

    environment {
        BASE_URL = 'https://demoqa.com'
        HEADLESS = 'true'
        BROWSER  = "${params.BROWSER}"
    }

    stages {

        stage('Setup') {
            steps {
                echo "🐍 Instalando dependencias de Python..."
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip -q
                    pip install -r requirements.txt -q
                '''
            }
        }

        stage('Tests') {
            steps {
                echo "🧪 Corriendo tests..."
                script {
                    def markers = params.MARKERS ? "-m ${params.MARKERS}" : ""
                    sh """
                        . venv/bin/activate
                        python3 -m pytest ${markers} \
                            --alluredir=reports/allure-results \
                            --tb=short \
                            -v
                    """
                }
            }
            post {
                always {
                    allure([
                        includeProperties: true,
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completado — todos los tests pasaron"
        }
        failure {
            echo "❌ Pipeline falló — revisa el reporte Allure"
        }
        unstable {
            echo "⚠️ Pipeline inestable — algunos tests fallaron"
        }
        always {
            cleanWs()
        }
    }
}