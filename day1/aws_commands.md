### 1. Block - 1 commands

aws s3api create-bucket  --bucket mlops-sachin-artifacts  --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2

aws iam create-policy --policy-name mlops-learner-iam-policy --policy-document day1/mlops-learner-iam-policy.json --profile admin

aws iam create-role --role-name ec2-mlops-role  --assume-role-policy-document file://C:/Users/sachi/Projects/PythonProjects/Learn_MLOps_Application/day1/trust-policy.json

aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess

aws iam attach-role-policy --role-name ec2-mlops-role  --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess

aws iam create-instance-profile --instance-profile-name ec2-mlops-profile

aws iam add-role-to-instance-profile --instance-profile-name ec2-mlops-profile --role-name ec2-mlops-role


## Block - 2 Commands

- Step 1 — Find the Ubuntu 22.04 AMI for ap-south-1:
aws ec2 describe-images --owners 099720109477 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" --query "Images | sort_by(@, &CreationDate) | [-1].ImageId" --region us-west-2 --output text

- output : ami-0370d56c6f7906c70

- Step 2 — Create Security Group:
aws ec2 create-security-group --group-name mlops-mlflow-sg --description "Security group for MLflow server" --region us-west-2

- Step 3 — Get your public IP:
curl https://checkip.amazonaws.com


- Step 4a — Add SSH rule:
aws ec2 authorize-security-group-ingress --group-id sg-0a931b0771876e8bc --protocol tcp --port 22 --cidr <your-ip>/32 --region us-west-2

- Step 4b — Add MLflow port rule:
aws ec2 authorize-security-group-ingress --group-id sg-0a931b0771876e8bc --protocol tcp --port 5000 --cidr <your-ip>/32 --region us-west-2

- Step 5 — Create key pair:
aws ec2 create-key-pair --key-name mlops-key --query "KeyMaterial" --output text --region us-west-2 > mlops-key.pem

- Step 6 — Launch the instance:
aws ec2 run-instances --image-id ami-0370d56c6f7906c70 --instance-type t3.medium --key-name mlops-key --security-group-ids sg-0a931b0771876e8bc --iam-instance-profile Name=ec2-mlops-profile --region us-west-2 --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=mlops-mlflow-server}]" --count 1

- Step 7 — Get public IP:
aws ec2 describe-instances --filters "Name=tag:Name,Values=mlops-mlflow-server" --query "Reservations[0].Instances[0].PublicIpAddress" --region us-west-2 --output text

## Block - 3 Commands

- `python prepare_data.py`
- `python train.py`

- `aws s3 ls s3://mlops-sachin-artifacts/data/`

- `aws ec2 stop-instances --instance-ids <your-instance-id> --region us-west-2`
- `aws ec2 start-instances --instance-ids <your-instance-id> --region us-west-2`

- `aws ec2 describe-instances --instance-ids <your-instance-id> --query "Reservations[0].Instances[0].State.Name" --region us-west-2 --output text`

- `aws s3 ls s3://mlops-sachin-artifacts/mlruns/ --recursive`


## Block - 4 Commands

- `python registry.py`

## Infra setup commands

- First time — creates everything
    `python infra.py --action setup`

- Coming back after a break — starts instance, updates SG with your new IP
    `python infra.py --action start`

- Taking a break — stops instance
    `python infra.py --action stop`

- Done with everything — deletes all resources
    `python infra.py --action teardown`