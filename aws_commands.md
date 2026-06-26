# AWS Commands — Day 1 (Summary)

Purpose

- Record the key AWS CLI commands run during Day 1 (IAM, S3, instance profile) and how to verify them.

Commands Executed

```bash
# 1. Create S3 bucket
aws s3api create-bucket \
  --bucket mlops-sachin-artifacts \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# 2. Create a custom IAM policy (JSON file in day1/)
aws iam create-policy \
  --policy-name mlops-learner-iam-policy \
  --policy-document day1/mlops-learner-iam-policy.json \
  --profile admin

# 3. Create IAM role with EC2 trust
aws iam create-role \
  --role-name ec2-mlops-role \
  --assume-role-policy-document file://day1/trust-policy.json

# 4. Attach managed policies to the role
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess

# 5. Create instance profile and add role
aws iam create-instance-profile --instance-profile-name ec2-mlops-profile
aws iam add-role-to-instance-profile --instance-profile-name ec2-mlops-profile --role-name ec2-mlops-role
```

Verification

```bash
# Check S3 bucket exists and is listable
aws s3 ls s3://mlops-sachin-artifacts

# Check role exists
aws iam get-role --role-name ec2-mlops-role

# List attached policies
aws iam list-attached-role-policies --role-name ec2-mlops-role

# Check instance profile
aws iam get-instance-profile --instance-profile-name ec2-mlops-profile
```

Notes & Tips

- Use least privilege: replace managed policies with a tailored JSON policy when possible.
- The trust policy file is `day1/trust-policy.json` and should specify `ec2.amazonaws.com` as the principal.
- To attach the instance profile to an EC2 instance, do so at launch or via the EC2 console/`associate-iam-instance-profile`.
- Avoid committing credentials to the repo; use IAM roles for EC2 instead.

Troubleshooting

- If `aws s3 ls` fails on an EC2 instance, confirm the instance has an attached instance profile and the role has S3 permissions.
- If `add-role-to-instance-profile` fails with a "Limit exceeded" error, check for existing roles attached or delete unused instance profiles.

References

- AWS CLI: https://docs.aws.amazon.com/cli/latest/reference/
- IAM Roles for EC2: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html
