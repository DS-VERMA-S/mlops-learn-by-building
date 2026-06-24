# Notes for Block 02

**Why EC2 and not SageMaker**: SageMaker hides too much. You need to know what a tracking server actually is before you use a managed one.

**What you will do:**

 - Launch an EC2 instance — t3.medium, Ubuntu 22.04, 20GB storage
- Security group: open port 22 (SSH), port 5000 (MLflow UI) — restrict to your IP only
- Attach the ec2-mlops-role you created above
- SSH in, install: python3, pip, mlflow, boto3, scikit-learn, xgboost
- Start MLflow with S3 as artifact store:

## Checklist

- [x] Launch EC2 instance (t3.medium, Ubuntu 22.04)
- [x] Configure Security Group (SSH port 22, MLflow port 5000)
- [x] Attach ec2-mlops-role to the instance
- [x] SSH into instance
- [x] Install dependencies (python3, pip, mlflow, boto3, scikit-learn, xgboost)
- [x] Start MLflow server with S3 as artifact store
- [x] Verify MLflow UI opens in browser


## Learning Notes


- .pem file is open for all users to read, lets fix it.

- commands for reading and entering in EC2 instance
icacls "C:\xxxx\xxxx\mlops-key.pem" /inheritance:r
icacls "C:\xxxx\xxxx\mlops-key.pem" /grant:r "$($env:USERNAME):(R)"

ssh -i "C:\xxxx\xxxx\mlops-key.pem" ubuntu@34.221.xx.xx






