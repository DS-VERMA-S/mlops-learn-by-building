# Block 1 — IAM + AWS Setup

## Summary

This block sets up the IAM and basic AWS infrastructure used by later MLOps blocks. Key outcomes:
- An S3 bucket for artifacts
- A role (`ec2-mlops-role`) that EC2 instances can assume
- An instance profile (`ec2-mlops-profile`) that bundles the role for EC2

Purpose: allow EC2 instances to interact with AWS services (S3, ECR, CloudWatch) without embedding credentials on the host.

## Quick Checklist

- [x] S3 bucket created: `mlops-sachin-artifacts`
- [x] IAM policy created: `mlops-learner-iam-policy`
- [x] IAM role created: `ec2-mlops-role`
- [x] Instance profile created: `ec2-mlops-profile`
- [x] Policies attached: S3, EC2, ECR, CloudWatch

## High-level Notes (plain English)

- We avoid using long-lived access keys on servers. Instead, EC2 instances get a role (temporary credentials provided by AWS).
- The role is attached to an instance profile; the EC2 instance uses that profile to obtain short-lived credentials from the metadata service.
- S3 is our artifact store for models, datasets, and MLflow artifacts.

## Commands (what we ran)

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

# 3. Create role and trust policy for EC2
aws iam create-role \
  --role-name ec2-mlops-role \
  --assume-role-policy-document file://day1/trust-policy.json

# 4. Attach managed policies
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
aws iam attach-role-policy --role-name ec2-mlops-role --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess

# 5. Create instance profile and add role
aws iam create-instance-profile --instance-profile-name ec2-mlops-profile
aws iam add-role-to-instance-profile --instance-profile-name ec2-mlops-profile --role-name ec2-mlops-role
```

## How to Verify

- From a machine with the instance profile attached: `aws s3 ls` should work without manual credentials.
- In the EC2 console, check the instance's IAM role and the attached instance profile.

## Common Troubleshooting

- If `aws s3 ls` fails on the instance: confirm the instance has the instance profile attached and the role has S3 permissions.
- If the role isn't visible in EC2: ensure the instance profile was created and the role was added to it.

## Next Steps

- Launch EC2 (Block 2) and attach `ec2-mlops-profile`.
- Start MLflow server and configure S3 as artifact store.

## Issues Faced

- EC2 could not access S3 because the instance profile was not attached.
- IAM policy permissions were missing for one or more AWS services.
- S3 bucket creation failed when the bucket region did not match the command parameters.

## Key Learnings

- EC2 instances should use IAM roles instead of embedded credentials.
- An instance profile is required for EC2 to assume the IAM role.
- Verify IAM permissions with simple AWS CLI calls from the instance.
