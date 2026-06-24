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