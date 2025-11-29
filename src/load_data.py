import sys
import pandas as pd
import dvc.api

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage: python load_data.py <data_path> <output_path>\n")
    sys.exit(1)

data_path = sys.argv[1]
output_path = sys.argv[2]

# Pull data using DVC
# Note: Ensure you are running this from the repo root or adjust repo= path
try:
    with dvc.api.open(
        path=data_path,
        mode='r'
    ) as fd:
        df = pd.read_csv(fd)
        df.to_csv(output_path, index=False)
        print(f"✅ Data loaded to {output_path}")
except Exception as e:
    print(f"Error loading data: {e}")
    sys.exit(1)
