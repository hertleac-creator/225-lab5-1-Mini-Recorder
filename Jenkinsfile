pipeline {
    agent any

    environment {
        // Sacred credentials and identifiers
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/hertleac'  //<<-- Replace with your MiamiID–blessed image name
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/hertleac-creator/225-lab5-1-Mini-Recorder.git'
        KUBECONFIG = credentials('hertleac-225') 
    }

    stages {

        // ===========================================
        // PHASE I: Retrieve STC fragments from the archives
        // ===========================================
        stage('⚙️ Data-Vault Checkout') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        // ===========================================
        // PHASE II: Scan sacred scripts for impurity
        // ===========================================
        stage('📜 HTML Litany Inspection') {
            steps {
                sh 'npm install htmlhint --save-dev'
                sh 'npx htmlhint *.html'
            }
        }

        stage('📜 Static Purity Tests') {
            steps {

                // Python syntax validation
                sh 'python3 -m py_compile $(find . -name "*.py")'

                // YAML purity inspections
                sh '''
                python3 - <<EOF
import yaml, glob, sys
for f in glob.glob("*.yaml"):
    try:
        with open(f) as file:
            list(yaml.safe_load_all(file))
    except Exception as e:
        print(f"YAML ERROR in {f}: {e}")
        sys.exit(1)
EOF
                '''
            }
        }

        // ===========================================
        // PHASE III: Forge the Docker combat frame
        // ===========================================
        stage('🏭 Forge Docker War Machine') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIALS_ID}") {
                        def app = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                        app.push()
                    }
                }
            }
        }

        // ===========================================
        // PHASE IV: Deploy to the Dev Theatre of War
        // ===========================================
        stage('⚔️ Deploy to Dev Engagement Zone') {
            steps {
                script {
                    // Load sacred kube config
                    def kubeConfig = readFile(KUBECONFIG)

                    // Purge old constructs
                    sh "kubectl delete --all deployments --namespace=default"

                    // Update deployment image tag
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"

                    // Deploy battle assets
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        // ===========================================
        // PHASE V: Expose to hostile penetration testing
        // ===========================================
        stage('🔮 DAST Inquisitorial Ordeal') {
            steps {
                // IMPORTANT: Update cluster IP
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
        // PHASE VI: Purge corrupted data after trial
        // ===========================================
        stage('🧹 Dev Database Purification') {
            steps {
                script {
                    def appPod = sh(
                        script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    sh """
                        kubectl exec ${appPod} -- python3 - <<'PY'
                        import sqlite3
                        conn = sqlite3.connect('/nfs/demo.db')
                        cur = conn.cursor()
                        cur.execute('DELETE FROM parts')
                        conn.commit()
                        conn.close()
                        PY
                    """
                }
            }
        }

        // ===========================================
        // PHASE VII: Generate test data for compliance
        // ===========================================
        stage('📦 Test Data Resupply') {
            steps {
                script {
                    def appPod = sh(script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'", returnStdout: true).trim()
                    sh "sleep 15"
                    sh "kubectl get pods"
                    sh "kubectl exec ${appPod} -- python3 data-gen.py"
                }
            }
        }

        // ===========================================
        // PHASE VIII: Perform Mechanicus Trials (Acceptance Tests)
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
        // PHASE IX: Cleanup combat logs and residues
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
        // PHASE X: Send war asset to final production front
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
        // PHASE XI: Verify battle readiness
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
