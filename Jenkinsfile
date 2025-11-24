pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/hertleac'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/hertleac-creator/225-lab5-1-Mini-Recorder.git'
        KUBECONFIG = credentials('hertleac-225')
    }

    stages {

        // ==============================================================
        // PHASE I – Retrieve sacred data from the Mechanicus vault
        // ==============================================================
        stage('⚙️ Data-Vault Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: "${GITHUB_URL}"]]
                ])
            }
        }

        // ==============================================================
        // PHASE II – Code Canticle Litanies
        // ==============================================================
        stage('📜 Static Purity Tests') {
            steps {
                sh 'python3 -m py_compile $(find . -name "*.py")'
            }
        }

        // ==============================================================
        // PHASE III – Forge Docker War Machine
        // ==============================================================
        stage('🏭 Forge Docker War Machine') {
            steps {
                script {
                    docker.withRegistry(
                        'https://registry.hub.docker.com',
                        "${DOCKER_CREDENTIALS_ID}"
                    ) {
                        def app = docker.build(
                            "${DOCKER_IMAGE}:${IMAGE_TAG}",
                            "-f Dockerfile.build ."
                        )
                        app.push()
                    }
                }
            }
        }

        // ==============================================================
        // PHASE IV – Deploy to Dev Engagement Zone
        // ==============================================================
        stage('⚔️ Deploy to Dev Engagement Zone') {
            steps {
                script {
                    sh "kubectl delete --all deployments --namespace=default || true"
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        // ==============================================================
        // PHASE V – Await pod readiness
        // ==============================================================
        stage('🟢 Await Pod Readiness') {
            steps {
                sh "kubectl wait --for=condition=ready pod -l app=flask --timeout=120s"
            }
        }

        // ==============================================================
        // PHASE VI – Purge stale heresy from the database
        // ==============================================================
        stage('🧹 Dev Database Purification') {
            steps {
                script {
                    def pod = sh(
                        script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    sh """
                    kubectl exec ${pod} -- python3 - << 'PY'
import sqlite3
conn = sqlite3.connect('/nfs/demo.db')
cur = conn.cursor()
cur.execute('DELETE FROM warhammer')
conn.commit()
conn.close()
PY
                    """
                }
            }
        }

        // ==============================================================
        // PHASE VII – Generate Warhammer test data
        // ==============================================================
        stage('📦 Test Data Resupply') {
            steps {
                script {
                    def pod = sh(
                        script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    sh "kubectl exec ${pod} -- python3 /app/data-gen.py"
                }
            }
        }

        // ==============================================================
        // PHASE VIII – Selenium Field Trial
        // ==============================================================
        stage('🔍 Selenium Field Trial') {
            steps {
                script {
                    def pod = sh(
                        script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    def podIP = sh(
                        script: "kubectl get pod ${pod} -o jsonpath='{.status.podIP}'",
                        returnStdout: true
                    ).trim()

                    sh "kubectl exec ${pod} -- python3 /app/tests/test_selenium.py --base-url=http://${podIP}:5000"
                }
            }
        }

        // ==============================================================
        // PHASE IX – Clean up the holy records again
        // ==============================================================
        stage('🧽 Purge Test Data') {
            steps {
                script {
                    def pod = sh(
                        script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    sh "kubectl exec ${pod} -- python3 /app/data-clear.py"
                }
            }
        }

        // ==============================================================
        // PHASE X – Deploy to Holy Production Server
        // ==============================================================
        stage('🚀 Deploy to Production') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                    sh "kubectl apply -f deployment-prod.yaml"
                }
            }
        }
    }

    post {
        success {
            slackSend color: "good",
                message: "🟢 Deployment successful — The Omnissiah approves!"
        }
        failure {
            slackSend color: "danger",
                message: "🔴 Deployment FAILED — Tech-Priests to the manufactorum!"
        }
    }
}
