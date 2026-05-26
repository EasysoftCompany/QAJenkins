pipeline {
    agent {
        any {
            image 'python:3.11-slim'
            args '--shm-size=2g'  // Evita crashes de Chrome por falta de memoria compartida
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))  // Conserva solo los últimos 10 builds
        timeout(time: 30, unit: 'MINUTES')              // Cancela si tarda más de 30 min
        timestamps()                                     // Agrega timestamps a los logs
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
        BASE_URL    = 'https://demoqa.com'
        HEADLESS    = 'true'   // Siempre headless en CI
        BROWSER     = "${params.BROWSER}"
        PIP_NO_CACHE_DIR = 'off'
    }

    stages {

        stage('Setup') {
            steps {
                echo "🔧 Instalando dependencias del sistema..."
                sh '''
                    apt-get update -qq
                    apt-get install -y -qq \
                        chromium \
                        chromium-driver \
                        libglib2.0-0 \
                        libnss3 \
                        libgconf-2-4 \
                        libfontconfig1 \
                        wget \
                        curl
                '''
                echo "🐍 Instalando dependencias de Python..."
                sh '''
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
                        python -m pytest ${markers} \
                            --alluredir=reports/allure-results \
                            --tb=short \
                            -v
                    """
                }
            }
            post {
                always {
                    // Guarda los resultados aunque los tests fallen
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
            cleanWs()  // Limpia el workspace al terminar
        }
    }
}
