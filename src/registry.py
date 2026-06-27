import mlflow
from mlflow.tracking import MlflowClient

TRACKING_URI = "http://localhost:5000/"
MODEL_NAME = "IrisClassifier"
RUN_ID = "1e5730eca3cb4b4a8c31d79e8efbf6d0"

mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient()

# Register the model
model_uri = f"runs:/{RUN_ID}/model"
registered = mlflow.register_model(model_uri, MODEL_NAME)
print(f"Model registered: {registered.name}, version: {registered.version}")

# Transition to Staging
client.transition_model_version_stage(
    name=MODEL_NAME,
    version=registered.version,
    stage="Staging"
)
print(f"Model transitioned to Staging")

# Transition to Production
client.transition_model_version_stage(
    name=MODEL_NAME,
    version=registered.version,
    stage="Production"
)
print(f"Model transitioned to Production")