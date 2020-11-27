pipeline {
    agent any

    options {
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        OWNER = 'rantanevich'
        REPO = 'simple-flask-app'
        IMAGE_NAME = 'flask-app'
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
            sh '''curl "https://api.github.com/repos/${OWNER}/${REPO}/statuses/${GIT_COMMIT}" \
                        -H "Authorization: token ${GITHUB_TOKEN}" \
                        -H "Content-Type: application/json" \
                        -X POST \
                        -d "{\\\"state\\\": \\\"success\\\",\\\"context\\\": \\\"continuous-integration/jenkins\\\", \\\"description\\\": \\\"Jenkins\\\", \\\"target_url\\\": \\\"${JOB_URL}/${BUILD_NUMBER}/console\\\"}"
            '''
        }
        failure {
            sh '''curl "https://api.github.com/repos/${OWNER}/${REPO}/statuses/${GIT_COMMIT}" \
                        -H "Authorization: token ${GITHUB_TOKEN}" \
                        -H "Content-Type: application/json" \
                        -X POST \
                        -d "{\\\"state\\\": \\\"failure\\\",\\\"context\\\": \\\"continuous-integration/jenkins\\\", \\\"description\\\": \\\"Jenkins\\\", \\\"target_url\\\": \\\"${JOB_URL}/${BUILD_NUMBER}/console\\\"}"
            '''
        }
    }
}