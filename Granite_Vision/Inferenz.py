from PIL import Image
import gradio as gr
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model and processor
model_path = "ibm-granite/granite-vision-3.2-2b"

processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForVision2Seq.from_pretrained(model_path).to(device)


def analyze_image(image, prompt):
    """Analyzes the uploaded image based on the entered prompt."""

    # Convert image to PIL format (if necessary)
    image = Image.open(image).convert("RGB")

    # Create chat template with image and prompt
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image", "url": image},
                {"type": "text", "text": prompt},  # Use the entered prompt
            ],
        },
    ]

    # Prepare data for the model
    inputs = processor.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(device)

    # Model generation
    output = model.generate(**inputs, max_new_tokens=100)
    response = processor.decode(output[0], skip_special_tokens=True)

    return response  # Return the model response


# Gradio interface with image upload and prompt input
iface = gr.Interface(
    fn=analyze_image,  # Function for image processing
    inputs=[
        gr.Image(type="filepath", label="Upload an image"),  # Image upload
        gr.Textbox(label="Enter a question or prompt")  # Free prompt
    ],
    outputs=gr.Textbox(label="Model response"),  # Model output
    title="🖼️ Interactive Image Analysis with Granite Vision",
    description="Upload an image and enter a question or prompt. The model analyzes the image based on your prompt.",
)

# Launch Gradio app
iface.launch()