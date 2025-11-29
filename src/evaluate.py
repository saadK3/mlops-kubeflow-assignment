import sys
import pandas as pd
import pickle
import mlflow
from sklearn.metrics import mean_squared_error, r2_score

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage: python evaluate.py <model_path> <test_path>\n")
    sys.exit(1)

model_path = sys.argv[1]
test_path = sys.argv[2]

# Start a new MLflow run for evaluation
with mlflow.start_run():
    test_df = pd.read_csv(test_path)
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Log metrics to MLflow
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2_score", r2)

    print(f"✅ Evaluation Results - MSE: {mse:.4f}, R2: {r2:.4f}")
