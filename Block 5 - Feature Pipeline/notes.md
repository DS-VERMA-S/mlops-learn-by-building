# Block 5 - Feature Pipeline

- [ ] Understand the feature pipeline's role
- [ ] Write preprocessing logic as a reusable function
- [ ] Save reference statistics (mean, std) to S3 during training
- [ ] Write batch feature pipeline that reads raw data from S3 and writes features back to S3
- [ ] Verify output features in S3


## Work Items: 
- Writing a reusable preprocessing logic
    - Code to preprocess and clean the data to get it ready for features pipeline.
    - 


## Key Learnings
    - To keep the preprocessing logic reusable, we can write it as a function and call it from different scripts.
    - To import the function from another script, we can use the `sys.path.append` method to add the path of the script to the system path.
    
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
        from feature_pipeline import compute_reference_stats, save_reference_stats

    - Training and inference pipelines should share the same preprocessing logic to ensure consistency in feature generation.


## Challenges Faced
    - Ensuring that the preprocessing logic is consistent between training and inference pipelines.
    - Managing and maintaining the preprocessing logic as the data and features evolve over time.
    - While writing the preprocessing logic for feature pipeline, make sure to convert it to ByteIO object before writing to S3, otherwise it will throw an error.