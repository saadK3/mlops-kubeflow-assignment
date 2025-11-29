import sys
import pandas as pd
from sklearn.model_selection import train_test_split

if len(sys.argv) != 4:
    sys.stderr.write("Arguments error. Usage: python preprocess.py <input_path> <train_out> <test_out>\n")
    sys.exit(1)

input_path = sys.argv[1]
train_path = sys.argv[2]
test_path = sys.argv[3]

df = pd.read_csv(input_path)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)
print(f"✅ Preprocessing done. Train shape: {train_df.shape}, Test shape: {test_df.shape}")
