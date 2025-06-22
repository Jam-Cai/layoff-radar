import pickle
import pandas as pd
from features_model import Features


def predict(features: Features):
    with open("model", "rb") as f:
        model = pickle.load(f)

    new_sample = pd.DataFrame(
        {
            "Location_HQ": ["Khoros"],
            "Industry": ["Sales"],
            "Stage": ["Private"],
            "Year": [2025],
            "log10_Funds_Raised": [138],
        }
    )

    prediction = model.predict(new_sample)

    return prediction[0]