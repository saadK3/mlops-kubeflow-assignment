# MLOps Pipeline with MLflow and Kubernetes

## Project Overview

This project demonstrates a complete MLOps pipeline for training and evaluating a machine learning model on the **Diabetes dataset**. The pipeline implements best practices for:

- **Data versioning** using DVC (Data Version Control)
- **Experiment tracking** using MLflow
- **Container orchestration** using Kubernetes (Minikube)
- **Continuous Integration** using Jenkins
- **Pipeline orchestration** using MLflow Projects

### ML Problem

The project uses the **Diabetes dataset** from scikit-learn to predict disease progression based on patient features. The model is a **Random Forest Regressor** that predicts a quantitative measure of disease progression one year after baseline.

**Note:** This project was originally designed for Kubeflow Pipelines, but due to technical issues with KFP deployment on Windows, we were advised to use **MLflow** as an alternative orchestration tool. MLflow provides similar experiment tracking and pipeline management capabilities with simpler deployment requirements.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Minikube Cluster                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              MLflow Tracking Server                  │   │
│  │         (Deployed as Kubernetes Pod)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                    MLflow Tracking API
                            │
┌─────────────────────────────────────────────────────────────┐
│                   ML Pipeline (Local)                       │
│  ┌────────────┐  ┌────────────┐  ┌────────┐  ┌──────────┐  │
│  │ Load Data  │→ │ Preprocess │→ │ Train  │→ │ Evaluate │  │
│  │   (DVC)    │  │  (Split)   │  │ (RF)   │  │ (Metrics)│  │
│  └────────────┘  └────────────┘  └────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                    Jenkins CI/CD
                            │
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Repository                      │
│         (Code, DVC metadata, Jenkinsfile)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- **Windows 10/11** with WSL2 or **Linux/macOS**
- **Docker Desktop** (for Minikube)
- **Python 3.9+**
- **Git**
- **Minikube**
- **kubectl**
- **Jenkins** (optional, for CI/CD)

---

## Setup Instructions

### 1. Install Minikube

**Windows (using Chocolatey):**
```bash
choco install minikube
```

### 2. Start Minikube

```bash
minikube start --driver=docker
```

Verify Minikube is running:
```bash
minikube status
```

Expected output:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
```

### 3. Deploy MLflow Server on Kubernetes

Apply the MLflow deployment:
```bash
kubectl apply -f mlflow-k8s.yaml
```

Verify the MLflow pod is running:
```bash
kubectl get pods
```

You should see:
```
NAME                             READY   STATUS    RESTARTS   AGE
mlflow-server-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
```

### 4. Access MLflow UI

Start port forwarding to access MLflow:
```bash
minikube service mlflow-service --url
```

This will output a URL like `http://127.0.0.1:xxxxx`. Keep this terminal open and access the MLflow UI in your browser.

### 5. Setup DVC Remote Storage

This project uses DVC for data versioning. The data is tracked locally, but you can configure remote storage:

**Initialize DVC (already done):**
```bash
dvc init
```

**Add data to DVC:**
```bash
dvc add data/raw_data.csv
git add data/raw_data.csv.dvc data/.gitignore
git commit -m "Track data with DVC"
```

**Configure remote storage (optional):**
```bash
# Example: Using Google Drive
dvc remote add -d myremote gdrive://your-folder-id

# Or using S3
dvc remote add -d myremote s3://mybucket/path
```

**Push data to remote:**
```bash
dvc push
```

### 6. Install Python Dependencies

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Pipeline Walkthrough

### Understanding the Pipeline

The ML pipeline consists of 4 stages:

1. **Load Data** (`src/load_data.py`)
   - Loads data from DVC-tracked CSV file
   - Outputs: `data/extracted.csv`

2. **Preprocess** (`src/preprocess.py`)
   - Splits data into train/test sets (80/20)
   - Outputs: `data/train.csv`, `data/test.csv`

3. **Train** (`src/train.py`)
   - Trains Random Forest Regressor
   - Logs parameters and metrics to MLflow
   - Outputs: `data/model.pkl`

4. **Evaluate** (`src/evaluate.py`)
   - Evaluates model on test set
   - Logs MSE and R² metrics to MLflow
   - Outputs: Metrics in MLflow UI

### Running the Pipeline

#### Option 1: Run Complete Pipeline

Execute the main pipeline script:
```bash
python src/main.py
```

Expected output:
```
Starting Pipeline...

--- Step 1: Load Data ---
Data loaded to C:\...\data\extracted.csv

--- Step 2: Preprocess ---
Preprocessing done. Train shape: (353, 11), Test shape: (89, 11)

--- Step 3: Train ---
Model trained and saved to C:\...\data\model.pkl

--- Step 4: Evaluate ---
Evaluation Results - MSE: X.XX, R2: X.XX

Pipeline Completed Successfully!
```

#### Option 2: Run Individual Steps

You can run each step independently:

```bash
# Step 1: Load Data
python src/load_data.py data/raw_data.csv data/extracted.csv

# Step 2: Preprocess
python src/preprocess.py data/extracted.csv data/train.csv data/test.csv

# Step 3: Train
python src/train.py data/train.csv data/model.pkl

# Step 4: Evaluate
python src/evaluate.py data/model.pkl data/test.csv
```

### Viewing Results in MLflow UI

1. Open the MLflow UI (from the port-forwarding URL)
2. Navigate to the **"diabetes_pipeline"** experiment
3. Click on a run to view:
   - **Parameters**: `n_estimators`, `random_state`, etc.
   - **Metrics**: `mse`, `r2_score`
   - **Artifacts**: Saved model files

---

## Continuous Integration with Jenkins

### Setup Jenkins Pipeline

1. **Access Jenkins**: `http://localhost:8080`

2. **Create New Pipeline Job**:
   - Click "New Item"
   - Name: `MLOps-Pipeline-CI`
   - Type: "Pipeline"
   - Click "OK"

3. **Configure Pipeline**:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your GitHub repo URL
   - **Branch**: `*/main`
   - **Script Path**: `Jenkinsfile`

4. **Update Python Path** in `Jenkinsfile`:
   - Edit line 7 to match your Python installation
   - Find path using: `where python` (Windows) or `which python` (Linux/macOS)

5. **Run Build**:
   - Click "Build Now"
   - View console output to see all 3 stages execute

### Jenkins Pipeline Stages

The Jenkinsfile defines 3 stages:

1. **Environment Setup**
   - Checkout code from GitHub
   - Install Python dependencies

2. **Pipeline Validation**
   - Validate MLflow project structure
   - Check all component scripts exist
   - Verify Python syntax

3. **Syntax Check**
   - Compile all Python files
   - Ensure no syntax errors

---

## Project Structure

```
mlops-kubeflow-assignment/
├── .dvc/                      # DVC configuration
├── .git/                      # Git repository
├── components/                # Legacy KFP component YAMLs (not used)
├── data/
│   ├── raw_data.csv          # Original dataset
│   ├── raw_data.csv.dvc      # DVC tracking file
│   ├── extracted.csv         # Loaded data
│   ├── train.csv             # Training set
│   ├── test.csv              # Test set
│   └── model.pkl             # Trained model
├── src/
│   ├── load_data.py          # Data loading component
│   ├── preprocess.py         # Preprocessing component
│   ├── train.py              # Training component
│   ├── evaluate.py           # Evaluation component
│   └── main.py               # Pipeline orchestration
├── Dockerfile                # MLflow server Docker image
├── Jenkinsfile               # Jenkins CI/CD pipeline
├── MLProject.yaml            # MLflow project configuration
├── mlflow-k8s.yaml           # Kubernetes deployment for MLflow
├── pipeline.py               # Pipeline validation script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## Key Technologies

| Technology | Purpose |
|------------|---------|
| **MLflow** | Experiment tracking and pipeline orchestration |
| **DVC** | Data version control |
| **Kubernetes (Minikube)** | Container orchestration |
| **Docker** | Containerization |
| **Jenkins** | Continuous Integration/Deployment |
| **scikit-learn** | Machine learning framework |
| **Python** | Programming language |

---

## Why MLflow Instead of Kubeflow?

**Original Plan**: Use Kubeflow Pipelines (KFP) for pipeline orchestration.

**Challenge**: Kubeflow Pipelines has complex deployment requirements and encountered technical issues on Windows environments, including:
- Large resource requirements (multiple pods, databases, etc.)
- Compatibility issues with Windows Docker Desktop
- Complex networking configuration

**Solution**: MLflow was recommended as a simpler, more lightweight alternative that provides:
- ✅ Experiment tracking (similar to KFP)
- ✅ Pipeline orchestration via MLflow Projects
- ✅ Model registry
- ✅ Easy deployment (single pod on Kubernetes)
- ✅ Better Windows compatibility
- ✅ Simpler setup and maintenance

Both tools serve the MLOps purpose, but MLflow is more suitable for this assignment's scope and environment constraints.

---

## Troubleshooting

### Minikube Issues

**Problem**: Minikube won't start
```bash
minikube delete
minikube start --driver=docker
```

**Problem**: Can't access MLflow UI
```bash
# Check pod status
kubectl get pods

# Restart port forwarding
minikube service mlflow-service --url
```

### Pipeline Issues

**Problem**: Module not found errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem**: DVC data not found
```bash
# Pull data from remote
dvc pull

# Or regenerate data
python generate_data.py
```

### Jenkins Issues

**Problem**: Python not found in Jenkins
- Update `PYTHON_HOME` in Jenkinsfile (line 7)
- Use full path to Python executable

**Problem**: Build fails at validation
```bash
# Test validation locally
python pipeline.py
```

## Contributors

- **Saad Ahmad Khan** - 22i-0499

---

## License

This project is for educational purposes as part of an MLOps assignment.

---

## Acknowledgments

- **Diabetes Dataset**: scikit-learn datasets
- **MLflow**: Databricks
- **Kubeflow**: Google/Kubeflow Community
- **Course Instructors**: For guidance on using MLflow as KFP alternative
