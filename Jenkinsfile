pipeline {
    agent any

    stages {
        stage('Environment Setup') {
            steps {
                echo '========================================='
                echo 'Stage 1: Environment Setup'
                echo '========================================='

                // Checkout code
                echo 'Checking out code from repository...'
                checkout scm

                // Verify Python installation
                bat 'python --version'
                bat 'pip --version'

                // Install dependencies
                echo 'Installing Python dependencies...'
                bat 'pip install -r requirements.txt'

                echo '✅ Environment setup complete!'
            }
        }

        stage('Pipeline Validation') {
            steps {
                echo '========================================='
                echo 'Stage 2: Pipeline Validation'
                echo '========================================='

                // Run pipeline validation script
                echo 'Validating MLflow pipeline structure...'
                bat 'python pipeline.py'

                echo '✅ Pipeline validation complete!'
            }
        }

        stage('Syntax Check') {
            steps {
                echo '========================================='
                echo 'Stage 3: Syntax Check'
                echo '========================================='

                // Check syntax of all Python files
                echo 'Checking Python syntax for all components...'
                bat 'python -m py_compile src/load_data.py'
                bat 'python -m py_compile src/preprocess.py'
                bat 'python -m py_compile src/train.py'
                bat 'python -m py_compile src/evaluate.py'
                bat 'python -m py_compile src/main.py'

                echo '✅ Syntax check complete!'
            }
        }
    }

    post {
        success {
            echo '========================================='
            echo '✅ BUILD SUCCESSFUL!'
            echo 'All stages completed successfully.'
            echo '========================================='
        }
        failure {
            echo '========================================='
            echo '❌ BUILD FAILED!'
            echo 'Please check the console output above.'
            echo '========================================='
        }
    }
}
