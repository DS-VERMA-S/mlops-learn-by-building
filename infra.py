import boto3
import argparse
import json
import time
import requests
import subprocess
import sys

# ── Config ──────────────────────────────────────────────
REGION = "us-west-2"
INSTANCE_NAME = "mlops-mlflow-server"
SG_NAME = "mlops-mlflow-sg"
BUCKET_NAME = "mlops-sachin-artifacts"
KEY_NAME = "mlops-key"
AMI_ID = "ami-0370d56c6f7906c70"
INSTANCE_TYPE = "t3.small"
INSTANCE_PROFILE = "ec2-mlops-profile"
PORTS = [22, 5000]

ec2 = boto3.client("ec2", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)


# ── Helpers ──────────────────────────────────────────────
def get_my_ip():
    ip = requests.get("https://checkip.amazonaws.com").text.strip()
    print(f"Your current IP: {ip}")
    return ip


def get_instance():
    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name", "Values": [INSTANCE_NAME]},
            {"Name": "instance-state-name", "Values": ["running", "stopped", "pending"]}
        ]
    )
    reservations = response["Reservations"]
    if not reservations:
        return None
    return reservations[0]["Instances"][0]


def get_sg_id():
    response = ec2.describe_security_groups(
        Filters=[{"Name": "group-name", "Values": [SG_NAME]}]
    )
    groups = response["SecurityGroups"]
    if not groups:
        return None
    return groups[0]["GroupId"]


def update_sg_rules(sg_id, my_ip):
    print(f"Updating security group {sg_id} with IP {my_ip}...")

    # Remove all existing ingress rules
    sg = ec2.describe_security_groups(GroupIds=[sg_id])["SecurityGroups"][0]
    existing = sg.get("IpPermissions", [])
    if existing:
        ec2.revoke_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=existing
        )

    # Add fresh rules for current IP
    for port in PORTS:
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[{
                "IpProtocol": "tcp",
                "FromPort": port,
                "ToPort": port,
                "IpRanges": [{"CidrIp": f"{my_ip}/32", "Description": f"Port {port} for MLOps learner"}]
            }]
        )
    print(f"Security group updated — ports {PORTS} open for {my_ip}/32")


# ── Actions ──────────────────────────────────────────────
def setup():
    my_ip = get_my_ip()

    # Create S3 bucket
    print(f"Creating S3 bucket {BUCKET_NAME}...")
    try:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": REGION}
        )
        s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True
            }
        )
        print(f"S3 bucket {BUCKET_NAME} created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"S3 bucket {BUCKET_NAME} already exists.")

    # Create security group
    sg_id = get_sg_id()
    if not sg_id:
        print("Creating security group...")
        response = ec2.create_security_group(
            GroupName=SG_NAME,
            Description="Security group for MLflow server"
        )
        sg_id = response["GroupId"]
        print(f"Security group created: {sg_id}")
    else:
        print(f"Security group already exists: {sg_id}")

    update_sg_rules(sg_id, my_ip)

    # Launch EC2 instance
    instance = get_instance()
    if instance:
        print(f"Instance already exists: {instance['InstanceId']} ({instance['State']['Name']})")
        return

    print("Launching EC2 instance...")
    response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SecurityGroupIds=[sg_id],
        IamInstanceProfile={"Name": INSTANCE_PROFILE},
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": INSTANCE_NAME}]
        }]
    )
    instance_id = response["Instances"][0]["InstanceId"]
    print(f"Instance launched: {instance_id}")
    print("Waiting for instance to be running...")
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])

    instance = get_instance()
    print(f"Instance is running. Public IP: {instance['PublicIpAddress']}")
    print(f"\nSSH command:\nssh -i C:\\Personal\\aws_credentials\\mlops-key.pem ubuntu@{instance['PublicIpAddress']}")


def start():
    my_ip = get_my_ip()
    instance = get_instance()

    if not instance:
        print("No instance found. Run: python infra.py --action setup")
        return

    instance_id = instance["InstanceId"]
    state = instance["State"]["Name"]

    if state == "running":
        print(f"Instance already running: {instance['PublicIpAddress']}")
    elif state == "stopped":
        print(f"Starting instance {instance_id}...")
        ec2.start_instances(InstanceIds=[instance_id])
        print("Waiting for instance to be running...")
        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceIds=[instance_id])
        instance = get_instance()
        print(f"Instance started. Public IP: {instance['PublicIpAddress']}")
    else:
        print(f"Instance is in state: {state}. Wait and retry.")
        return

    # Update SG with new IP
    sg_id = get_sg_id()
    update_sg_rules(sg_id, my_ip)

    instance = get_instance()
    print(f"\nMLflow UI: http://{instance['PublicIpAddress']}:5000")
    print(f"SSH command:\nssh -i C:\\Personal\\aws_credentials\\mlops-key.pem ubuntu@{instance['PublicIpAddress']}")


def stop():
    instance = get_instance()
    if not instance:
        print("No running instance found.")
        return

    instance_id = instance["InstanceId"]
    print(f"Stopping instance {instance_id}...")
    ec2.stop_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter("instance_stopped")
    waiter.wait(InstanceIds=[instance_id])
    print("Instance stopped. No EC2 compute charges until you start it again.")
    print("Note: EBS storage charges still apply (~$0.10/GB/month).")


def teardown():
    confirm = input("This will TERMINATE the instance and DELETE the S3 bucket. Type 'yes' to confirm: ")
    if confirm != "yes":
        print("Aborted.")
        return

    # Terminate instance
    instance = get_instance()
    if instance:
        instance_id = instance["InstanceId"]
        print(f"Terminating instance {instance_id}...")
        ec2.terminate_instances(InstanceIds=[instance_id])
        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=[instance_id])
        print("Instance terminated.")
    else:
        print("No instance found to terminate.")

    # Delete S3 bucket contents then bucket
    print(f"Deleting S3 bucket {BUCKET_NAME}...")
    try:
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=BUCKET_NAME):
            objects = page.get("Contents", [])
            if objects:
                s3.delete_objects(
                    Bucket=BUCKET_NAME,
                    Delete={"Objects": [{"Key": o["Key"]} for o in objects]}
                )
        s3.delete_bucket(Bucket=BUCKET_NAME)
        print("S3 bucket deleted.")
    except Exception as e:
        print(f"S3 deletion error: {e}")

    # Delete security group
    sg_id = get_sg_id()
    if sg_id:
        print(f"Deleting security group {sg_id}...")
        try:
            ec2.delete_security_group(GroupId=sg_id)
            print("Security group deleted.")
        except Exception as e:
            print(f"SG deletion error (may still have dependencies): {e}")


# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MLOps Infrastructure Manager")
    parser.add_argument("--action", required=True, choices=["setup", "start", "stop", "teardown"])
    args = parser.parse_args()

    actions = {
        "setup": setup,
        "start": start,
        "stop": stop,
        "teardown": teardown
    }
    actions[args.action]()