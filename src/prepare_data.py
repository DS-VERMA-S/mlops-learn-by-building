import pandas as pd
import boto3
from sklearn.datasets import load_iris

# Load iris dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target

# Save locally first
df.to_csv('iris.csv', index=False)

# Upload to S3
s3 = boto3.client('s3', region_name='us-west-2')
s3.upload_file('iris.csv', 'mlops-sachin-artifacts', 'data/iris.csv')
print("Uploaded iris.csv to s3://mlops-sachin-artifacts/data/iris.csv")