# Titanic MLOps Pipeline on AWS

This repository demonstrates an end-to-end MLOps pipeline built on AWS using Amazon SageMaker, Amazon S3, and AWS Lambda. It covers the complete workflow from model training and deployment to benchmarking and automated retraining.

**Read the full project walkthrough:**  
https://builder.aws.com/content/3HESLxUozSAASmmxHFhDK7bRTbM/how-i-built-my-first-end-to-end-mlops-pipeline-on-aws

---

## Project Overview

This project demonstrates how to:

- Train a machine learning model using scikit-learn
- Deploy the model as a real-time Amazon SageMaker endpoint
- Serve predictions through a custom inference script
- Benchmark endpoint latency using AWS Lambda
- Automatically retrain the model whenever new data is uploaded to Amazon S3

The model used is a **Random Forest Classifier** trained on the Titanic dataset, achieving **82.68% test accuracy**. Since the goal of this project was to learn MLOps, I focused on building a reliable pipeline rather than maximizing model performance.

---

## Architecture

> Replace the image path below after adding your architecture diagram to the repository.

<p align="center">
  <img src="assets/architecture.png" alt="Architecture Diagram" width="900">
</p>

---

## Repository Structure

```text
mlops-titanic-pipeline/
├── deployment/
│   └── inference.py
├── benchmarking/
│   ├── lambda_function.py
│   ├── run_benchmark.ps1
│   ├── sample_25.csv
│   └── results.csv
├── retraining/
│   ├── lambda_function.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── notification.json
└── README.md
```

---

## Pipeline Walkthrough

### 1. Model Training

- Titanic dataset stored in Amazon S3
- Data cleaned and preprocessed
- Random Forest Classifier trained using scikit-learn
- Test Accuracy: **82.68%**
- Model saved as `titanic_model.pkl`

### 2. Model Deployment

The trained model was packaged and deployed to a real-time Amazon SageMaker endpoint using a custom `inference.py` script to handle JSON requests and responses.

### 3. Benchmarking

An AWS Lambda function invokes the SageMaker endpoint using a fixed sample dataset stored in Amazon S3.

| Metric | Value |
|---------|-------|
| Cold Start | **216.63 ms** |
| Warm Invocations | **13.82–48.23 ms** |
| Average Warm Latency | **~26 ms** |
| Success Rate | **25/25 (100%)** |

### 4. Automated Retraining

Uploading a new dataset to the `raw-data/` folder in Amazon S3 automatically triggers a Lambda function that retrains the model and uploads the updated artifact.

---

## Tech Stack

**AWS:** Amazon SageMaker, Amazon S3, AWS Lambda, AWS IAM, Amazon CloudWatch, Amazon ECR

**Python:** scikit-learn, pandas, boto3, joblib

**Tools:** Docker, Jupyter Notebook, PowerShell

---

## What I Learned

- Building an end-to-end MLOps workflow on AWS
- Deploying and updating SageMaker endpoints
- Writing custom inference scripts
- Benchmarking real-time ML endpoints
- Automating retraining with AWS Lambda and Amazon S3 events
- Debugging IAM, networking, and data preprocessing issues

---

## Resources

**GitHub Repository**  
https://github.com/NehaSama4833/mlops-titanic-pipeline

**AWS Builder Center Article**  
https://builder.aws.com/content/3HESLxUozSAASmmxHFhDK7bRTbM/how-i-built-my-first-end-to-end-mlops-pipeline-on-aws

---

If you found this project useful, consider starring the repository or sharing your feedback. Contributions and suggestions are always welcome.
