from PIL import Image
import gradio as gr
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

# Prüfe, ob CUDA verfügbar ist
device = "cuda" if torch.cuda.is_available() else "cpu"

# Modell und Prozessor laden
model_path = "ibm-granite/granite-vision-3.2-2b"
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForVision2Seq.from_pretrained(model_path).to(device)


def analyze_image(image, prompt):
    """Analysiert das hochgeladene Bild basierend auf dem eingegebenen Prompt."""

    # Bild in PIL-Format umwandeln (falls nötig)
    image = Image.open(image).convert("RGB")

    # Chat-Template mit Bild und Prompt erstellen
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image", "url": image},
                {"type": "text", "text": prompt},  # Nutze den eingegebenen Prompt
            ],
        },
    ]

    # Daten für das Modell vorbereiten
    inputs = processor.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(device)

    # Modellgenerierung
    output = model.generate(**inputs, max_new_tokens=100)
    response = processor.decode(output[0], skip_special_tokens=True)

    return response  # Rückgabe der Modellantwort


# Gradio-Interface mit Bild-Upload und Prompt-Eingabe
iface = gr.Interface(
    fn=analyze_image,  # Funktion für Bildverarbeitung
    inputs=[
        gr.Image(type="filepath", label="Lade ein Bild hoch"),  # Bild-Upload
        gr.Textbox(label="Gib eine Frage oder einen Prompt ein")  # Freier Prompt
    ],
    outputs=gr.Textbox(label="Modellantwort"),  # Ausgabe des Modells
    title="🖼️ Interaktive Bildanalyse mit Granite Vision",
    description="Lade ein Bild hoch und gib eine Frage oder einen Prompt ein. Das Modell analysiert das Bild basierend auf deinem Prompt.",
)

# Gradio-App starten
iface.launch()
