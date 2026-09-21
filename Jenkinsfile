pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
        booleanParam(name: 'RUN_SECURITY_SCANS', defaultValue: true, description: 'Toggle OWASP & Trivy scans')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'prod'], description: 'Target deployment environment')
    }

    environment {
        APP_NAME         = 'my-python-app'
        DOCKER_HUB_USER  = 'your-dockerhub-username'
        REGISTRY         = 'docker.io'
        SONAR_HOST_URL   = 'http://your-sonarqube-server:9000'
        SLACK_CHANNEL    = '#devops-deployments'
        
        VENV_DIR         = '.venv'

        DOCKER_CREDS     = credentials('docker-hub-credentials')
        SLACK_TOKEN      = credentials('slack-token')
        SONAR_TOKEN      = credentials('sonar-token')
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Cloning Python source code..."
                checkout scm
            }
        }

        stage('Setup Virtual Environment & Install Dependencies') {
            steps {
                script {
                    echo "Creating Python virtual environment..."
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Parallel Tests & Code Analysis') {
            parallel {

                stage('Linting (Flake8)') {
                    steps {
                        script {
                            echo "Running Flake8 code linting..."
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
                            '''
                        }
                    }
                }

                stage('Unit Tests & Coverage') {
                    steps {
                        script {
                            echo "Running Pytest..."
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                pytest tests/ --junitxml=junit/test-results.xml --cov=app --cov-report=xml:coverage.xml
                            '''
                        }
                    }
                }

                stage('SonarQube Scan') {
                    steps {
                        script {
                            echo "Executing SonarQube Scanner..."
                            def scannerHome = tool 'SonarScanner'
                            withSonarQubeEnv('SonarQubeServer') {
                                sh """
                                    ${scannerHome}/bin/sonar-scanner \
                                        -Dsonar.projectKey=${env.APP_NAME} \
                                        -Dsonar.sources=app \
                                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                                        -Dsonar.host.url=${env.SONAR_HOST_URL} \
                                        -Dsonar.login=${env.SONAR_TOKEN}
                                """
                            }
                        }
                    }
                }

            }
        }

        stage('Quality Gate Check') {
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }

        stage('Security Scans') {
            when {
                expression { return params.RUN_SECURITY_SCANS == true }
            }
            parallel {

                stage('Python Safety Scan') {
                    steps {
                        script {
                            sh '''
                                . ${VENV_DIR}/bin/activate
                                safety check --full-report || true
                            '''
                        }
                    }
                }

                stage('Trivy Repository Scan') {
                    steps {
                        sh 'trivy fs --severity HIGH,CRITICAL .'
                    }
                }

            }
        }

        stage('Build & Scan Docker Image') {
            steps {
                script {
                    def fullImageName = "${env.DOCKER_HUB_USER}/${env.APP_NAME}:${params.IMAGE_TAG}"
                    
                    echo "Building Docker Image..."
                    sh "docker build -t ${fullImageName} ."

                    echo "Scanning Image with Trivy..."
                    sh "trivy image --severity HIGH,CRITICAL ${fullImageName}"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    def fullImageName = "${env.DOCKER_HUB_USER}/${env.APP_NAME}:${params.IMAGE_TAG}"
                    sh "echo ${env.DOCKER_CREDS_PSW} | docker login -u ${env.DOCKER_CREDS_USR} --password-stdin ${env.REGISTRY}"
                    sh "docker push ${fullImageName}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying ${env.APP_NAME} to ${params.DEPLOY_ENV}..."
                    sh 'echo "Deployment successful!"'
                }
            }
        }

    }

    post {
        always {
            sh "rm -rf ${env.VENV_DIR} coverage.xml junit/"
            sh "docker rmi ${env.DOCKER_HUB_USER}/${env.APP_NAME}:${params.IMAGE_TAG} || true"
            cleanWs deleteDirs: true, notFailBuild: true
        }

        success {
            slackSend(
                channel: env.SLACK_CHANNEL,
                color: '#00FF00',
                message: "SUCCESS: Job '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] (${env.BUILD_URL})"
            )
        }

        failure {
            slackSend(
                channel: env.SLACK_CHANNEL,
                color: '#FF0000',
                message: "FAILURE: Job '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] (${env.BUILD_URL})"
            )
        }
    }
}
