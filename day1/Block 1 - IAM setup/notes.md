# Block 1 — IAM + AWS Setup

## Checklist
- [x] Created IAM user `mlops-learner` with programmatic access
- [x] Downloaded and stored access key CSV safely (not in repo)
- [x] Attached policies: S3FullAccess, EC2FullAccess, ECRFullAccess, CloudWatchFullAccess
- [x] Configured AWS CLI locally (`aws configure`)
- [x] Verified CLI works: `aws s3 ls` returns without error
- [x] Created S3 bucket `mlops-<yourname>-artifacts` with public access blocked
- [x] Created IAM Role `ec2-mlops-role` with same 4 policies
- [x] Verified role has EC2 as trusted entity (not a user, not Lambda — EC2)

## Screenshots
- [x] IAM user created (console screenshot)
- [x] Policies attached to user
- [x] S3 bucket created
- [x] IAM Role trust relationship showing EC2

## Key Concepts — Answer These Before Moving On
1. What is the difference between an IAM User and an IAM Role?
2. Why does the EC2 role have EC2 as the trusted entity?
3. Where are your AWS credentials stored locally after `aws configure`?
4. What happens if you put your access keys in a Python file and push to GitHub?

## Notes

### 1. What Were We Doing?

In Day 1, Block 1, we set up the **foundational security and infrastructure** for our MLOps project on AWS. Instead of using root AWS account credentials (which is dangerous), we created a proper **IAM role** that EC2 machines can use. This follows the principle of least privilege—each service only gets the permissions it actually needs.

Think of it like this:
- **IAM Role** = A job title or badge for an EC2 machine
- **Instance Profile** = The holder that carries the badge
- **Policies** = The specific permissions written on the badge (S3 access, EC2 access, etc.)

When we launch an EC2 instance and attach this badge to it, the instance automatically knows how to talk to AWS services like S3 (for storing models/data), ECR (for Docker images), and CloudWatch (for monitoring)—without us having to hardcode any credentials on the machine.

We also created an S3 bucket as a central storage hub for all our MLOps artifacts (datasets, trained models, logs, configs).

### 2. Commands Executed

#### 1.1 S3 Bucket Creation
```bash
aws s3api create-bucket \
  --bucket mlops-sachin-artifacts \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2
```
**Purpose:** Created a private S3 bucket to store MLOps artifacts (models, datasets, logs)

#### 1.2 IAM Policy Creation
```bash
aws iam create-policy \
  --policy-name mlops-learner-iam-policy \
  --policy-document day1/mlops-learner-iam-policy.json \
  --profile admin
```
**Purpose:** Created a custom IAM policy with specific permissions for MLOps work

#### 1.3 IAM Role Creation (for EC2)
```bash
aws iam create-role \
  --role-name ec2-mlops-role \
  --assume-role-policy-document file://C:/Users/sachi/Projects/PythonProjects/Learn_MLOps_Application/day1/trust-policy.json
```
**Purpose:** Created an IAM role that EC2 instances can assume. Trust policy allows EC2 service to use this role.

#### 1.4 Attached Policies to Role
```bash
# S3 Full Access
aws iam attach-role-policy \
  --role-name ec2-mlops-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# EC2 Full Access
aws iam attach-role-policy \
  --role-name ec2-mlops-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

# ECR Full Access (for Docker image management)
aws iam attach-role-policy \
  --role-name ec2-mlops-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess

# CloudWatch Full Access (for monitoring & logs)
aws iam attach-role-policy \
  --role-name ec2-mlops-role \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess
```
**Purpose:** Granted necessary AWS service permissions to the EC2 role

#### 1.5 Created Instance Profile
```bash
aws iam create-instance-profile --instance-profile-name ec2-mlops-profile
```
**Purpose:** Created a container that holds the IAM role. This is what gets attached to EC2 instances.

#### 1.6 Added Role to Instance Profile
```bash
aws iam add-role-to-instance-profile \
  --instance-profile-name ec2-mlops-profile \
  --role-name ec2-mlops-role
```
**Purpose:** Linked the role to the instance profile. Now any EC2 instance using this profile will have these permissions.

### 2. Architecture Summary
```
EC2 Instance
    ↓
Instance Profile (ec2-mlops-profile)
    ↓
IAM Role (ec2-mlops-role)
    ↓
Policies Attached:
  • AmazonS3FullAccess
  • AmazonEC2FullAccess
  • AmazonEC2ContainerRegistryFullAccess
  • CloudWatchFullAccess
```

When you launch an EC2 instance with this instance profile, the instance will automatically have access to these AWS services without needing to store credentials on the instance.

### 3. Configure AWS CLI
- `aws configure` for setting up the CLI in local windows
```
AWS Access Key ID:      ← from the CSV you downloaded
AWS Secret Access Key:  ← from the CSV you downloaded
Default region name:    ← use us-west-2 (Always choose the closest)
Default output format:  ← json
```