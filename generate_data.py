import pandas as pd
from sklearn.datasets import load_diabetes
import os

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load Diabetes dataset
diabetes = load_diabetes()
df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
df['target'] = diabetes.target

# Save to CSV
df.to_csv('data/raw_data.csv', index=False)
print("✅ Success: data/raw_data.csv created using the Diabetes dataset.")
