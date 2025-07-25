import pickle
import pandas as pd
from features_model import Features


def predict(features: Features):
    with open("model", "rb") as f:
        model = pickle.load(f)

    new_sample = pd.DataFrame([features.dict()])

    prediction = model.predict(new_sample)

    return prediction[0]


if __name__ == "__main__":
    features = Features(
        Location_HQ="Google",
        Industry="Tech",
        Stage="Stage 1",
        Year=2020,
        log10_Funds_Raised=10
    )
    print(predict(features))