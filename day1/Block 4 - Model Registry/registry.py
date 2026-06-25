import mlflow
from mlflow.tracking import MlflowClient

TRACKING_URI = "http://44.247.73.2:5000/"
MODEL_NAME = "IrisClassifier"
RUN_ID = "2d087958dd1d4d6a8c408dd8250faa24"

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