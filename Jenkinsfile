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

        // ===============================
        // Checkout Source
        // ===============================
        stage('Checkout') {
            steps {
                cleanWs()
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: "${GITHUB_URL}"]]
                ])
            }
        }

        // ===============================
        // Static Code Review
        // ===============================
        stage('Static Tests') {
            steps {
                sh 'python3 -m py_compile $(find . -name "*.py")'
            }
        }

        // ===============================
        // Build Docker Image
        // ===============================
        stage('Build Docker') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIALS_ID}") {
                        def app = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                        app.push()
                    }
                }
            }
        }

        // ===============================
        // Deploy to Dev
        // ===============================
        stage('Deploy to Dev') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        // ===============================
        // Init Database
        // ===============================
        stage('Initialize DB') {
            steps {
                script {
                    def appPod = sh(
                        script: "kubectl get pods -l app=flask -o jsonpath='{.items[0].metadata.name}'",
                        returnStdout: true
                    ).trim()

                    sh "kubectl exec ${appPod} -- python3 /app/data-gen.py"
                }
            }
        }

        // ===============================
        // Run Selenium Tests (outside)
        // ===============================
        stage('Selenium Tests') {
            steps {
                sh 'python3 tests/test_selenium.py'
            }
        }
    }

    post {
        success {
            echo "✔ Build completed successfully!"
        }
        failure {
            echo "❌ Build failed!"
        }
    }
}
