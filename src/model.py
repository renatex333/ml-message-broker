import os
import pickle

MODEL_FOLDER = os.path.relpath("models", os.getcwd())

def load_model(model_path: str = "model.pkl"):
    model_path = os.path.join(MODEL_FOLDER, model_path)
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

def load_encoder(encoder_path: str = "ohe.pkl"):
    encoder_path = os.path.join(MODEL_FOLDER, encoder_path)
    with open(encoder_path, "rb") as file:
        encoder = pickle.load(file)
    return encoder