import io
import os
import sys
import boto3
import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from feature_pipeline import compute_reference_stats, save_reference_stats

# ── Config ──────────────────────────────────────────────
TRACKING_URI = "http://35.165.175.72:5000"
EXPERIMENT_NAME = "iris-classifier-v1"
BUCKET = "mlops-sachin-artifacts"
DATA_KEY = "data/iris.csv"
REGION = "us-west-2"

# ── AWS S3 Data Ingestion ────────────────────────────────
s3 = boto3.client("s3", region_name=REGION)
obj = s3.get_object(Bucket=BUCKET, Key=DATA_KEY)
df = pd.read_csv(io.BytesIO(obj["Body"].read()))

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Save reference stats to S3 after splitting
stats = compute_reference_stats(X_train)
save_reference_stats(stats)

# ── MLflow Setup ─────────────────────────────────────────
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

params = {
    "n_estimators": 100,
    "max_depth": 3,
    "learning_rate": 0.1,
    "random_state": 42
}

# ── Training & Tracking Pipeline ─────────────────────────
with mlflow.start_run() as run:
    model = GradientBoostingClassifier(**params)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="weighted")

    # Log hyperparameters
    mlflow.log_params(params)

    # Log metrics
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("f1_score", f1)

    # Log model artifact safely 
    # Specifying artifact_path explicitly as a keyword argument preserves backward 
    # compatibility with older backend REST endpoints handling tracking stores.
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model"
    )

    print(f"Run ID: {run.info.run_id}")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Artifact URI: {mlflow.get_artifact_uri()}")