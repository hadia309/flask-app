pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Cloning the Flask app repository
                git branch: 'main', url: 'https://github.com/your-username/your-flask-app-repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installing Python dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Running unit tests with pytest
                sh 'pytest'
            }
        }

        stage('Build Application') {
            steps {
                // Building or preparing the application for deployment
                sh 'zip -r app.zip .'
            }
        }

        stage('Deploy Application') {
            steps {
                // Simulating deployment
                sh 'cp -r * /path/to/deployment/directory'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline executed successfully.'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}
