# Block 6 - Serving Layer

- [x] Write FastAPI app that loads Production model from MLflow on startup
- [x] Add /predict endpoint with Pydantic validation
- [x] Add /health endpoint
- [x] Test locally against live MLflow server
- [x] Verify predictions are correct

## Summary 
Model serving is the step where we expose trained model to external clients. In this block, we implement a FastAPI application that loads the Production model from MLflow on startup and provides endpoints for prediction and health checks.


## Learning
- Model should always be loaded from MLflow on startup, not per request.
- Add try catch for model loading and prediction to handle errors gracefully.
- Use Pydantic for request validation to ensure input data is in the correct format.
- 

## Key Challenges
- If Mflow server is not running, the FastAPI app will fail to start. We need to handle this scenario.
- With validator it is important to ensure that the input data matches the expected schema, otherwise the request will be rejected.