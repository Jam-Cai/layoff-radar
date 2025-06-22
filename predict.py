import pickle
import pandas as pd
from features_model import Features


def predict(features: Features):
    with open("model", "rb") as f:
        model = pickle.load(f)

    new_sample = pd.DataFrame([features.dict()])

    prediction = model.predict(new_sample)

    return prediction[0]