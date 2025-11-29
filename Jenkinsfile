pipeline {
    agent any

    environment {
        // Set Python path - UPDATE THIS to match your Python installation
        // To find it, run in terminal: where python
        PYTHON_HOME = 'C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python310'
        PYTHON = "${PYTHON_HOME}\\python.exe"
        PIP = "${PYTHON_HOME}\\Scripts\\pip.exe"
    }

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
                bat "${PYTHON} --version"
                bat "${PIP} --version"

                // Install dependencies
                echo 'Installing Python dependencies...'
                bat "${PIP} install -r requirements.txt"

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
                bat "${PYTHON} pipeline.py"

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
                bat "${PYTHON} -m py_compile src/load_data.py"
                bat "${PYTHON} -m py_compile src/preprocess.py"
                bat "${PYTHON} -m py_compile src/train.py"
                bat "${PYTHON} -m py_compile src/evaluate.py"
                bat "${PYTHON} -m py_compile src/main.py"

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
