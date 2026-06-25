# Block 3 - Training Pipeline

- [x] Create training dataset and upload to S3
- [x] Write training script that logs to remote MLflow
- [x] Log params, metrics, and model as MLflow artifact
- [x] Verify run appears in MLflow UI
- [x] Verify model files appear in S3 bucket


sudo apt update && sudo apt upgrade -y
python3 -m venv ~/mlops-env
source ~/mlops-env/bin/activate
pip install mlflow==2.14.0 boto3 scikit-learn xgboost pandas



python '.\day1\Block 3 - Training Pipeline\prepare_data.py'                

python '.\day1\Block 3 - Training Pipeline\train.py'