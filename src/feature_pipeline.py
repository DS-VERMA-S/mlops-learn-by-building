import os
import io
import json
import boto3
import pandas as pd
import numpy as np

BUCKET = "mlops-sachin-artifacts"
REGION = "us-west-2"

s3 = boto3.client("s3", region_name=REGION)

def compute_reference_stats(df:pd.DataFrame) -> dict:
    """
    Compute mean and std for each feature column.
    Called during training and saves during stats to s3.
    """

    stats = {}

    for col in df.columns:
        stats[col] = {
            'mean': df[col].mean(),
            'std': df[col].std()
        }
    
    return stats

def save_reference_stats(stats:dict, key:str="reference/feature_stats.json") -> None:

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(stats).encode('utf-8')
    )

    print(f"Reference stats saved to s3://{BUCKET}/{key}")


def load_reference_stats(key:str="reference/feature_stats.json") -> dict:
    """
    Load reference stats from s3.
    Called during inference to normalize features.
    """

    obj = s3.get_object(Bucket=BUCKET, Key=key)
    stats = json.loads(obj['Body'].read().decode())

    return stats

def apply_reference_stats(df:pd.DataFrame, stats:dict) -> pd.DataFrame:
    """
    Apply reference stats to normalize features.
    Called during inference to normalize features.
    """

    for col in df.columns:
        if col in stats:
            mean = stats[col]['mean']
            std = stats[col]['std']
            df[col] = (df[col] - mean) / std
        else:
            raise ValueError(f"Column {col} not found in reference stats.")
    return df

def run_batch_inference(input_data_path:str, output_data_path:str) -> None:
    """
    Run batch inference on input data and save predictions to output path.
    1. Read rae data from s3.
    2. Load references from s3.
    3. Apply reference stats to normalize features.
    4. Write features to s3.
    """

    obj = s3.get_object(Bucket=BUCKET, Key=input_data_path)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    print(f"Loaded raw data: {df.shape}")

    target = df['target']
    features = df.drop('target', axis=1)

    stats = load_reference_stats(key="reference/feature_stats.json")

    df_normalized = apply_reference_stats(features, stats)
    X_processed = df_normalized
    X_processed["target"] = target.values

    print(f"Preprocessing complete: {X_processed.shape}")

    csv_buffer = io.StringIO()
    X_processed.to_csv(csv_buffer, index=False)

    s3.put_object(
        Bucket=BUCKET,
        Key=output_data_path,
        Body=csv_buffer.getvalue()
    )
    print(f"Features written to s3://{BUCKET}/{output_data_path}")


if __name__ == "__main__":
    # Example usage
    input_data_path = "data/iris.csv"
    output_data_path = "data/iris_processed.csv"

    run_batch_inference(input_data_path, output_data_path)




