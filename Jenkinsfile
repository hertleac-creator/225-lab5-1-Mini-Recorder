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

        // ===========================================
        // Checkout
        // ===========================================
        stage('⚙️ Data-Vault Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        // ===========================================
        // Static analysis
        // ===========================================
        stage('📜 HTML Litany Inspection') {
            steps {
                sh 'npm install htmlhint --save-dev'
                sh 'npx htmlhint *.html'
            }
        }

        stage('📜 Static Purity Tests') {
            steps {
                sh 'python3 -m py_compile $(find . -name "*.py")'

                sh '''
                python3 - <<EOF
import yaml, glob, sys
for f in glob.glob("*.yaml"):
    try:
        list(yaml.safe_load_all(open(f)))
    except Exception as e:
        print(f"YAML ERROR in {f}: {e}")
        sys.exit(1)
EOF
                '''
            }
        }

        // ===========================================
        // Docker build & push
        // ===========================================
        stage('🏭 Forge Docker War Machine') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIALS_ID}") {
                        def app = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile .")
                        app.push()
                    }
                }
            }
        }

        // ===========================================
        // Deploy to Dev
        // ===========================================
        stage('⚔️ Deploy to Dev Engagement Zone') {
            steps {
                script {
                    sh "kubectl delete --all deployments --namespace=default || true"
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        // ===========================================
        // Wait for Flask pod readiness
        // ===========================================
        stage('🟢 Wait for Flask Pod Ready') {
            steps {
                script {
                    sh "kubectl wait --for=condition=ready pod -l app=flask --timeout=120s"
                }
            }
        }

        // ===========================================
        // Purge old DB data
        // ===========================================
        stage('🧹 Dev Database Purification') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh """
                        kubectl exec ${appPod} -- python3 - <<'PY'
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

        // ===========================================
        // Generate Selenium-friendly test data
        // ===========================================
        stage('📦 Test Data Resupply') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- python3 /app/data-gen.py"
                    echo "✅ Test data inserted successfully"
                }
            }
        }

        // ===========================================
        // Selenium QA
        // ===========================================
        stage('⚙️ Selenium QA Verification') {
            steps {
                script {
                    def appPodIP = sh(script: "kubectl get pod -l app=flask -o jsonpath='{.items[0].status.podIP}'", returnStdout: true).trim()
                    echo "🌐 Running Selenium tests against Flask pod at ${appPodIP}"
                    sh "python3 tests/test_selenium.py --base-url=http://${appPodIP}:5000"
                }
            }
        }

        // ===========================================
        // DAST testing
        // ===========================================
        stage('🔮 DAST Inquisitorial Ordeal') {
            steps {
                sh 'docker pull public.ecr.aws/portswigger/dastardly:latest'
                sh '''
                    docker run --user $(id -u) -v ${WORKSPACE}:${WORKSPACE}:rw \
                    -e HOME=${WORKSPACE} \
                    -e BURP_START_URL=http://10.48.229.148 \
                    -e BURP_REPORT_FILE_PATH=${WORKSPACE}/dastardly-report.xml \
                    public.ecr.aws/portswigger/dastardly:latest
                '''
            }
        }

        // ===========================================
        // QA Docker tests
        // ===========================================
        stage('⚙️ Adeptus QA Trial Protocols') {
            steps {
                script {
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                    sh 'docker build -t qa-tests -f Dockerfile.test .'
                    sh 'docker run qa-tests'
                }
            }
        }

        // ===========================================
        // Cleanup test data
        // ===========================================
        stage('🧽 Purge Test Data') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "kubectl exec ${appPod} -- python3 data-clear.py"
                }
            }
        }

        // ===========================================
        // Deploy to Production
        // ===========================================
        stage('🚀 Deploy to Holy Production Server') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                    sh "cd .."
                    sh "kubectl apply -f deployment-prod.yaml"
                }
            }
        }

        // ===========================================
        // Verify deployment
        // ===========================================
        stage('📡 Vox Confirmations') {
            steps {
                script {
                    sh "kubectl get all"
                }
            }
        }
    }

    post {
        success {
            slackSend color: "good", message: "🟢 Deployment successful: ${env.JOB_NAME} #${env.BUILD_NUMBER} — Glory to the Omnissiah!"
        }
        unstable {
            slackSend color: "warning", message: "🟡 Deployment unstable: ${env.JOB_NAME} #${env.BUILD_NUMBER} — Statistical variance detected."
        }
        failure {
            slackSend color: "danger", message: "🔴 Deployment FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} — Tech-Priests must report immediately!"
        }
    }
}
