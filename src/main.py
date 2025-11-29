import mlflow
import os
import subprocess
import sys

# Configure MLflow tracking to use the server running on Minikube
# Get the URL using: minikube service mlflow-service --url
mlflow.set_tracking_uri("http://127.0.0.1:62686")
mlflow.set_experiment("diabetes_pipeline")


def run_pipeline():
    # Define local paths for artifacts
    root = os.getcwd()
    raw_data = "data/raw_data.csv"

    data_out = os.path.join(root, "data", "extracted.csv")
    train_data = os.path.join(root, "data", "train.csv")
    test_data = os.path.join(root, "data", "test.csv")
    model_path = os.path.join(root, "data", "model.pkl")

    print("🚀 Starting Pipeline...")

    # Step 1: Load Data
    print("\n--- Step 1: Load Data ---")
    result = subprocess.run([sys.executable, "src/load_data.py", raw_data, data_out], check=True)

    # Step 2: Preprocess
    print("\n--- Step 2: Preprocess ---")
    result = subprocess.run([sys.executable, "src/preprocess.py", data_out, train_data, test_data], check=True)

    # Step 3: Train
    print("\n--- Step 3: Train ---")
    result = subprocess.run([sys.executable, "src/train.py", train_data, model_path], check=True)

    # Step 4: Evaluate
    print("\n--- Step 4: Evaluate ---")
    result = subprocess.run([sys.executable, "src/evaluate.py", model_path, test_data], check=True)

    print("\n✅ Pipeline Completed Successfully!")

if __name__ == "__main__":
    run_pipeline()
