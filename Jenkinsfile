pipeline {

    agent any

    stages {

        stage('Creating Virtual Environment') {
            steps {
                sh 'python3 -m venv .venv'
            }
        }

        stage('Installing Dependencies') {
            steps {
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Checking Python Environment') {
            steps {
                sh '.venv/bin/python --version'
                sh '.venv/bin/pip --version'
            }
        }

        stage('Syntax Check') {
            steps {
                sh '.venv/bin/python -m py_compile app.py'
            }
        }

    }
}
