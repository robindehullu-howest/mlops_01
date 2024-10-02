from transformers import AutoModelForImageClassification, AutoTokenizer, AutoImageProcessor
import os

token = os.getenv("HUGGINGFACE_TOKEN_BIRDS")

model_names = [
    "dennisjooo/Birds-Classifier-EfficientNetB2",
    "ozzyonfire/bird-species-classifier",
    "chriamue/bird-species-classifier"
    ]

def download_model(model_name, token):
    local_path = os.path.join("models", model_name.replace("/", "_"))

    if os.path.exists(local_path):
        print(f"Model and tokenizer already exist at {local_path}")
        return

    model = AutoModelForImageClassification.from_pretrained(model_name, use_auth_token=token)

    model.save_pretrained(local_path)
    print(f"Model saved to {local_path}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
        tokenizer.save_pretrained(local_path)
        print(f"Tokenizer saved to {local_path}")
    except Exception as e:
        print(f"Tokenizer not found for {model_name}: {e}")

    try:
        preprocessor = AutoImageProcessor.from_pretrained(model_name, use_auth_token=token)
        preprocessor.save_pretrained(local_path)
        print(f"Preprocessor saved to {local_path}")
    except Exception as e:
        print(f"Preprocessor not found for {model_name}: {e}")

for model_name in model_names:
    download_model(model_name, token)