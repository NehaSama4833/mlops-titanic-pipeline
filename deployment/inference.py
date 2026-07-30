import joblib
import os
import json
import numpy as np

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "titanic_model.pkl"))
    return model

def input_fn(request_body, content_type):
    data = json.loads(request_body)
    features = [
        data["Pclass"],
        data["Sex"],
        data["Age"],
        data["SibSp"],
        data["Parch"],
        data["Fare"],
        data["Embarked"]
    ]
    return np.array([features])

def predict_fn(input_data, model):
    return model.predict(input_data)

def output_fn(prediction, content_type):
    return json.dumps({"survived": int(prediction[0])})
