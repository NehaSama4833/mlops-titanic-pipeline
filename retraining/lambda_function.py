import boto3
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

s3 = boto3.client("s3")
BUCKET = "neha-mlops-2026"
DATA_KEY = "raw-data/titanic.csv"
MODEL_KEY = "model-artifacts/titanic_model.pkl"

def lambda_handler(event, context):
    local_data_path = "/tmp/titanic.csv"
    local_model_path = "/tmp/titanic_model.pkl"

    s3.download_file(BUCKET, DATA_KEY, local_data_path)
    df = pd.read_csv(local_data_path)

    df = df.drop(columns=["Cabin", "Name", "Ticket", "PassengerId"])
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

    X = df.drop(columns=["Survived"])
    y = df["Survived"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Retrained model accuracy: {accuracy:.4f}")

    joblib.dump(model, local_model_path)
    s3.upload_file(local_model_path, BUCKET, MODEL_KEY)

    return {"statusCode": 200, "body": f"Retrained. Accuracy: {accuracy:.4f}"}
