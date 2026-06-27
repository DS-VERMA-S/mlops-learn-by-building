import sys
import os
import time
import numpy as np
import mlflow.sklearn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List

# Add src to path for feature_pipeline import

from .feature_pipeline import load_reference_stats, apply_reference_stats as preprocess
import pandas as pd

# ── Config ──────────────────────────────────────────────
TRACKING_URI = "http://localhost:5000"
MODEL_NAME = "IrisClassifier"
MODEL_STAGE = "Production"
FEATURE_NAMES = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)"
]

# ── App Setup ────────────────────────────────────────────
app = FastAPI(title="Iris Classifier API", version="1.0.0")
model = None
reference_stats = None


@app.on_event("startup")
def load_model():
    global model, reference_stats
    mlflow.set_tracking_uri(TRACKING_URI)
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
    reference_stats = load_reference_stats()
    print(f"Model loaded: {MODEL_NAME}/{MODEL_STAGE}")
    print(f"Reference stats loaded from S3")


class PredictRequest(BaseModel):
    features: List[float]

    @validator("features")
    def check_feature_length(cls, v):
        if len(v) != 4:
            raise ValueError(f"Expected 4 features, got {len(v)}")
        return v


class PredictResponse(BaseModel):
    prediction: int
    confidence: float
    label: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_name": MODEL_NAME,
        "model_stage": MODEL_STAGE
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Build dataframe with correct feature names
    input_df = pd.DataFrame([req.features], columns=FEATURE_NAMES)

    # Apply same preprocessing as training
    processed = preprocess(input_df, reference_stats)

    # Predict
    pred = model.predict(processed)
    proba = model.predict_proba(processed)

    labels = {0: "setosa", 1: "versicolor", 2: "virginica"}

    return PredictResponse(
        prediction=int(pred[0]),
        confidence=round(float(proba[0].max()), 4),
        label=labels[int(pred[0])]
    )


@app.get("/")
def root():
    return {"message": "Iris Classifier API is running"}