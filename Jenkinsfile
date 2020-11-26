pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME = 'flask-app'
        REGISTRY = credentials('DOCKER_REGISTRY')
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${GIT_COMMIT} .'
            }
        }
        stage('Push') {
            steps {
                sh 'docker tag ${IMAGE_NAME}:${GIT_COMMIT} ${REGISTRY}/${IMAGE_NAME}:${GIT_COMMIT}'
                sh 'docker push ${REGISTRY}/${IMAGE_NAME}:${GIT_COMMIT}'
            }
        }
        stage('Deploy') {
            steps {
                ansiColor('xterm') {
                    ansiblePlaybook('provisioning/deploy.yml') {
                        inventoryPath('/etc/ansible/hosts')
                        colorizedOutput(true)
                        extraVars {
                            extraVar('GIT_COMMIT', '${GIT_COMMIT}', false)
                        }
                    }
                }
            }
        }
    }
}