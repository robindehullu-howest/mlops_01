import gradio as gr
from PIL import Image
from transformers import pipeline, AutoModelForImageClassification, AutoImageProcessor, AutoTokenizer
import os
from datetime import datetime

current_model = "dennisjooo/Birds-Classifier-EfficientNetB2"
model_pipeline = None

def load_model(model_name):
    global model_pipeline
    model_path = os.path.join("models", model_name.replace("/", "_"))
    model = AutoModelForImageClassification.from_pretrained(model_path)
    image_processor = AutoImageProcessor.from_pretrained(model_path)
    model_pipeline = pipeline("image-classification", model=model, feature_extractor=image_processor)

def classify_image(image):
    if model_pipeline is None:
        load_model(current_model)
    result = model_pipeline(image)[0]
    return {result["label"]: result["score"]}

def upload_images(files):
    upload_dir = "data/uploaded_images"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    for i, file in enumerate(files):
        current_time = datetime.now().strftime("%y%m%d%H%M%S")
        file_path = os.path.join(upload_dir, f"IMG_{current_time}{i}.jpg")
        with open(file_path, "wb") as f:
            f.write(file)
    
    return f"Uploaded {len(files)} images for training."

def list_models():
    models_dir = "models"
    models = [model.replace("_", "/") for model in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, model))]
    return models

def select_model(selected_model):
    global current_model
    current_model = selected_model
    load_model(current_model)
    return f"Selected model: {selected_model}"

def create_gradio_interface():
    with gr.Blocks() as demo:
        with gr.Tab("Classify Image"):
            gr.Markdown("Upload an image of a bird to classify it.")
            image_input = gr.Image(type="pil")
            label_output = gr.Label()
            classify_button = gr.Button("Classify")
            classify_button.click(classify_image, inputs=image_input, outputs=label_output)
        
        with gr.Tab("Upload Images for Training"):
            gr.Markdown("Upload multiple images of birds to train the model.")
            file_input = gr.File(file_count="multiple", type="binary")
            upload_button = gr.Button("Upload")
            upload_output = gr.Textbox()
            upload_button.click(upload_images, inputs=file_input, outputs=upload_output)

        with gr.Tab("Select Model"):
            gr.Markdown("Select a trained model from the list.")
            model_list = gr.Dropdown(list_models(), label="Available Models")
            select_button = gr.Button("Select Model")
            model_output = gr.Textbox()
            select_button.click(select_model, inputs=model_list, outputs=model_output)

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch()