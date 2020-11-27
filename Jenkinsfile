pipeline {
    agent any

    options {
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        OWNER = 'rantanevich'
        REPOSITORY = 'simple-flask-app'
        REGISTRY = credentials('DOCKER_REGISTRY')
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
    }

    stages {
        stage('Debug') {
            steps {
                sh 'export'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'python:3.8.6-slim-buster'
                    args '-u root:sudo'
                }
            }
            steps {
                sh 'ls -la'
                sh 'pip install --no-cache-dir flake8 pytest'
                sh 'python -m flake8 --exclude=".git,venv"'
                sh 'python -m pytest tests'
                sh 'python -m unittest'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t ${REPOSITORY}:${GIT_COMMIT} -f Dockerfile'
            }
        }
        stage('Push') {
            steps {
                sh 'docker tag ${REPOSITORY}:${GIT_COMMIT} ${REGISTRY}/${REPOSITORY}:${GIT_COMMIT}'
                sh 'docker push ${REGISTRY}/${REPOSITORY}:${GIT_COMMIT}'
            }
        }
        stage('Deploy') {
            steps {
                ansiblePlaybook(
                    playbook: 'provisioning/deploy.yml',
                    inventory: '/etc/ansible/hosts',
                    colorized: true,
                    extraVars: [
                        GIT_COMMIT: '${GIT_COMMIT}'
                    ]
                )
            }
        }
    }

    post {
        success {
            sh '''curl "https://api.github.com/repos/${OWNER}/${REPOSITORY}/statuses/${GIT_COMMIT}" \
                        -H "Authorization: token ${GITHUB_TOKEN}" \
                        -H "Content-Type: application/json" \
                        -X POST \
                        -d "{\\\"state\\\": \\\"success\\\",\\\"context\\\": \\\"continuous-integration/jenkins\\\", \\\"description\\\": \\\"Jenkins\\\", \\\"target_url\\\": \\\"${JOB_URL}/${BUILD_NUMBER}/console\\\"}"
            '''
        }
        failure {
            sh '''curl "https://api.github.com/repos/${OWNER}/${REPOSITORY}/statuses/${GIT_COMMIT}" \
                        -H "Authorization: token ${GITHUB_TOKEN}" \
                        -H "Content-Type: application/json" \
                        -X POST \
                        -d "{\\\"state\\\": \\\"failure\\\",\\\"context\\\": \\\"continuous-integration/jenkins\\\", \\\"description\\\": \\\"Jenkins\\\", \\\"target_url\\\": \\\"${JOB_URL}/${BUILD_NUMBER}/console\\\"}"
            '''
        }
    }
}