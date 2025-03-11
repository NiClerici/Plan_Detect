import fitz  # PyMuPDF
import re
import gradio as gr

# Regulärer Ausdruck für Maßzahlen: xx.xxx, xx.xx, x.xxx, x.xx, x.x
pattern = r"\b\d{1,2}\.\d{1,3}\b"


def extract_numbers_and_preview(pdf_file):
    """Extrahiert Maßzahlen aus einer PDF-Datei und zeigt sie an."""

    # PDF öffnen
    doc = fitz.open(pdf_file.name)
    found_numbers = []

    # Text aus allen Seiten extrahieren
    for page in doc:
        text = page.get_text("text")
        numbers = re.findall(pattern, text)
        found_numbers.extend(numbers)

    # Liste der gefundenen Zahlen als Text zurückgeben
    extracted_text = "\n".join(found_numbers) if found_numbers else "Keine Maßzahlen gefunden."

    # Rückgabe der extrahierten Daten + PDF zur Anzeige
    return extracted_text, pdf_file.name


# Gradio-Interface erstellen
iface = gr.Interface(
    fn=extract_numbers_and_preview,  # Funktion für Verarbeitung
    inputs=gr.File(label="Lade eine PDF hoch"),  # Datei-Upload
    outputs=[
        gr.Textbox(label="Gefundene Maßzahlen"),  # Anzeige der extrahierten Zahlen
        gr.File(label="PDF-Vorschau")  # PDF als Download und Vorschau
    ],
    title="📄 PDF Masszahlen-Extraktor",
    description="Dieses Tool extrahiert Maßzahlen aus einer PDF-Datei und zeigt das PDF an.",
)

# Gradio-App starten
iface.launch()
