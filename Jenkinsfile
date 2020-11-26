pipeline {
    agent any

    options {
        ansiColor('xterm')
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
}