pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'amansahu743/task-management:1.0.0'
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Aman-S-07/Task-Management.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh './venv/bin/python manage.py test'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to DockerHub') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials-id', usernameVariable: 'Aman-S-07', passwordVariable: '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')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f task-management-app || true
                    docker run -d --name task-management-app -p 8080:8000 $DOCKER_IMAGE
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
    }
}

