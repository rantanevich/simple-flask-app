pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '1'))
    }

    stages {
        stage('Display ENV') {
            steps {
                sh 'export'
            }
        }
    }
}