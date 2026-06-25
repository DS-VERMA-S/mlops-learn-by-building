sudo apt update && sudo apt upgrade -y
# Block 3 — Training Pipeline

## Summary

This block implements the local training script that logs experiments to the MLflow server and stores artifacts in S3. The goal is to produce reproducible runs that can be inspected and promoted via the Model Registry.

## Quick Checklist

- [x] Upload dataset to S3
- [x] Write training script that logs to remote MLflow
- [x] Log params, metrics, and model artifact
- [x] Confirm run shows in MLflow UI
- [x] Confirm model artifact exists in S3

## Development Steps (local/EC2)

```bash
sudo apt update && sudo apt upgrade -y
python3 -m venv ~/mlops-env
source ~/mlops-env/bin/activate
pip install mlflow==2.14.0 boto3 scikit-learn xgboost pandas
```

Run data prep (example):
```bash
python day1/Block\ 3\ -\ Training\ Pipeline/prepare_data.py
```

Run training (example):
```bash
python day1/Block\ 3\ -\ Training\ Pipeline/train.py
```

## Verification

- Check MLflow UI: new run appears with params/metrics
- Check S3: artifacts under `s3://mlops-sachin-artifacts/mlruns/<run-id>`

## Troubleshooting

- If training can't reach MLflow: confirm `MLFLOW_TRACKING_URI` and network/security group rules.
- If artifacts don't appear in S3: verify role permissions and `--default-artifact-root` used by MLflow.
