"""
Pipeline Validation Script
This script validates the MLflow pipeline structure and components.
Adapted for MLflow instead of Kubeflow Pipelines.
"""

import os
import sys
import py_compile
from pathlib import Path

def validate_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"{description} NOT FOUND: {filepath}")
        return False

def validate_python_syntax(filepath):
    """Validate Python file syntax"""
    try:
        py_compile.compile(filepath, doraise=True)
        print(f"✅ Syntax valid: {filepath}")
        return True
    except py_compile.PyCompileError as e:
        print(f"Syntax error in {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("MLflow Pipeline Validation")
    print("=" * 60)

    all_valid = True

    # Check component scripts
    print("\n[*] Validating Component Scripts...")
    components = [
        ("src/load_data.py", "Load Data Component"),
        ("src/preprocess.py", "Preprocess Component"),
        ("src/train.py", "Train Component"),
        ("src/evaluate.py", "Evaluate Component"),
        ("src/main.py", "Main Pipeline Script")
    ]

    for filepath, description in components:
        if validate_file_exists(filepath, description):
            if not validate_python_syntax(filepath):
                all_valid = False
        else:
            all_valid = False

    # Check MLProject configuration
    print("\n[*] Validating MLflow Project Configuration...")
    if not validate_file_exists("MLProject.yaml", "MLProject Configuration"):
        all_valid = False

    # Check requirements file
    print("\n[*] Validating Dependencies...")
    if not validate_file_exists("requirements.txt", "Requirements File"):
        all_valid = False

    # Check data directory
    print("\n[*] Validating Data Directory...")
    if not os.path.exists("data"):
        print("Data directory NOT FOUND")
        all_valid = False
    else:
        print("✅ Data directory exists")

    # Try importing MLflow
    print("\n[*] Validating MLflow Installation...")
    try:
        import mlflow
        print(f"✅ MLflow installed (version {mlflow.__version__})")
    except ImportError:
        print("MLflow NOT installed")
        all_valid = False

    # Final result
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ VALIDATION PASSED - Pipeline is ready!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("VALIDATION FAILED - Please fix the errors above")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
