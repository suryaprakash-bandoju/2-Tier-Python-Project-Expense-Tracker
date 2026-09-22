pipeline  {

    agent any

    stages {

        stage("Git Checkout") {
            steps {

                git branch: "main",
                    url: 'https://github.com/suryaprakash-bandoju/2-Tier-Python-Project-Expense-Tracker.git'

            }
        }
        
        stage("Installing Dependencies") {
            steps {

                sh 'pip3 install -r requirements.txt'
                
            }
        }

        stage("Syntax Check") {
            steps {

                sh 'python3 -m py_compile app.py'
                
            }
        }
    }
}
