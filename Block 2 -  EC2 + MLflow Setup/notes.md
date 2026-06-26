# Block 2 — EC2 + MLflow Setup

## Summary

This block launches an EC2 instance, installs MLflow, and configures it to use S3 for artifact storage. We prefer EC2 here so you see the full server setup and how MLflow connects to S3.

## Quick Checklist

- [x] Launch EC2 (t3.medium, Ubuntu 22.04)
- [x] Security group: open SSH (22) and MLflow UI (5000) to your IP
- [x] Attach `ec2-mlops-role` to the instance
- [x] Install runtime and dependencies (python3, pip, mlflow, boto3, scikit-learn, xgboost)
- [x] Start MLflow server with S3 artifact store
- [x] Confirm MLflow UI reachable

## Commands & Notes

SSH (example):
```bash
ssh -i "C:/Personal/aws_credentials/mlops-key.pem" ubuntu@<ec2-public-ip>
```

Fix Windows file permissions for .pem if needed:
```powershell
icacls "C:\path\to\mlops-key.pem" /inheritance:r
icacls "C:\path\to\mlops-key.pem" /grant:r "$($env:USERNAME):(R)"
```

Start MLflow on the instance:
```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root s3://mlops-sachin-artifacts/mlruns \
  --host 0.0.0.0 \
  --port 5000 \
  --gunicorn-opts "--workers 1"
```

Verify: open `http://<ec2-public-ip>:5000` in your browser (use your security group's IP restriction).

## Troubleshooting

- If MLflow UI is not reachable: check security group, firewall, and that MLflow is running.
- If MLflow can't write to S3: confirm the instance has the `ec2-mlops-profile` and the role includes S3 permissions.

## Issues Faced

- ML Flow UI was not working due to package version issue. Package was downgraded to 2.x version.
- SSH access failed on Windows until the `.pem` key permissions were fixed. This happened due to corrupt pem file.
- t3 micro was out of memory, after trying swap space and other ways to reduce the cost which did not work, hence instance type was increased to t3 small.
- kept the wrong URL broke the MLflow server.
- PowerShell > redirect corrupts the key file. Fix was Out-File -Encoding ascii
- When I downgraded from MLflow 3.x to 2.14.0, the existing mlflow.db had a schema MLflow 2.x couldn't read. Fix was deleting mlflow.db 


## Key Learnings

- MLflow requires both a valid backend store and a correct default artifact root.
- EC2 security groups must permit your client IP to reach port 5000 for the MLflow UI.
- Attaching the IAM role to EC2 allows MLflow to use AWS resources without manual credentials.




