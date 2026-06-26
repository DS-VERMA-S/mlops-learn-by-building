import mlflow
from mlflow.tracking import MlflowClient

TRACKING_URI = "http://35.165.175.72:5000/"
MODEL_NAME = "IrisClassifier"
RUN_ID = "9ad4b29b449842a4937657b1746968a3"

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