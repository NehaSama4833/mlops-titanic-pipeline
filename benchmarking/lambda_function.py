import json
import boto3
import csv
import io
import time

runtime = boto3.client("sagemaker-runtime")
s3 = boto3.client("s3")

ENDPOINT_NAME = "titanic-endpoint"
BUCKET = "neha-mlops-2026"
KEY = "experiment-data/sample_25.csv"

def lambda_handler(event, context):
    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    csv_data = obj["Body"].read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(csv_data))
    rows = list(reader)

    row = rows[event.get("row_index", 0) % len(rows)]

    sex_map = {"male": 0, "female": 1}
    embarked_map = {"S": 0, "C": 1, "Q": 2}

    payload = {
        "Pclass": int(row["Pclass"]),
        "Sex": sex_map.get(row["Sex"].strip().lower(), 0),
        "Age": float(row["Age"]) if row["Age"] else 0.0,
        "SibSp": int(row["SibSp"]),
        "Parch": int(row["Parch"]),
        "Fare": float(row["Fare"]) if row["Fare"] else 0.0,
        "Embarked": embarked_map.get(row["Embarked"].strip().upper(), 0)
    }

    start = time.time()
    try:
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps(payload)
        )
        result = json.loads(response["Body"].read().decode())
        latency_ms = round((time.time() - start) * 1000, 2)
        return {
            "statusCode": 200,
            "success": True,
            "latency_ms": latency_ms,
            "prediction": result
        }
    except Exception as e:
        latency_ms = round((time.time() - start) * 1000, 2)
        return {
            "statusCode": 500,
            "success": False,
            "latency_ms": latency_ms,
            "error": str(e)
        }
