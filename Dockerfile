FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install MLflow and dependencies
RUN pip install --no-cache-dir \
    mlflow==2.9.2 \
    boto3 \
    psycopg2-binary

# Expose MLflow default port
EXPOSE 5000

# Set environment variables
ENV MLFLOW_BACKEND_STORE_URI=/mlflow/mlruns
ENV MLFLOW_ARTIFACT_ROOT=/mlflow/artifacts

# Create directories for MLflow data
RUN mkdir -p /mlflow/mlruns /mlflow/artifacts

# Run MLflow server
CMD ["mlflow", "server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--backend-store-uri", "file:///mlflow/mlruns", \
     "--default-artifact-root", "file:///mlflow/artifacts"]
