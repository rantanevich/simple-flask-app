pipeline {
    agent any

    options {
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        REPOSITORY = 'rantanevich'
        PROJECT = 'simple-flask-app'
        IMAGE_NAME = 'flask-app'
        WEBHOOK_URL = credentials('JENKINS_WEBHOOK_URL')
        REGISTRY = credentials('DOCKER_REGISTRY')
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
    }

    stages {
        stage('Debug') {
            steps {
                sh 'export'
            }
        }
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

    post {
        success {
            sh '''curl "https://api.github.com/repos/${REPOSITORY}/${PROJECT}/statuses/${GIT_COMMIT}?access_token=${GITHUB_TOKEN}" \
                        -H "Content-Type: application/json" \
                        -X POST \
                        -d "{\\\"state\\\": \\\"success\\\",\\\"context\\\": \\\"continuous-integration/jenkins\\\", \\\"description\\\": \\\"Jenkins\\\", \\\"target_url\\\": \\\"${WEBHOOK_URL}/job/${PROJECT}/${BUILD_NUMBER}/console\\\"}"
            '''
        }
        failure {
            sh '''curl "https://api.github.com/repos/${REPOSITORY}/${PROJECT}/statuses/${GIT_COMMIT}?access_token=${GITHUB_TOKEN}" \
                        -H "Content-Type: application/json" \
                        -X POST \
                        -d "{\\\"state\\\": \\\"failure\\\",\\\"context\\\": \\\"continuous-integration/jenkins\\\", \\\"description\\\": \\\"Jenkins\\\", \\\"target_url\\\": \\\"${WEBHOOK_URL}/job/${PROJECT}/${BUILD_NUMBER}/console\\\"}"
            '''
        }
    }
}