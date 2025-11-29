import sys
import pandas as pd
import pickle
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage: python train.py <train_path> <model_path>\n")
    sys.exit(1)

train_path = sys.argv[1]
model_path = sys.argv[2]
n_estimators = 100

# Enable Auto-Logging to capture params and metrics automatically
mlflow.sklearn.autolog()

with mlflow.start_run():
    train_df = pd.read_csv(train_path)
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']

    model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)

    # Save manually for the next step (artifact passing)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"Model trained and saved to {model_path}")
