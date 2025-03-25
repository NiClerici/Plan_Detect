import fitz  # PyMuPDF
import re
import gradio as gr

# Regular expression for measurements: xx.xxx, xx.xx, x.xxx, x.xx, x.x
pattern = r"\b\d{1,2}\.\d{1,3}\b"


def extract_numbers_and_preview(pdf_file):
    """Extracts measurements from a PDF file and displays them."""

    # Open PDF
    doc = fitz.open(pdf_file.name)
    found_numbers = []

    # Extract text from all pages
    for page in doc:
        text = page.get_text("text")
        numbers = re.findall(pattern, text)
        found_numbers.extend(numbers)

    # Return list of found numbers as text
    extracted_text = "\n".join(found_numbers) if found_numbers else "No measurements found."

    # Return extracted data + PDF for display
    return extracted_text, pdf_file.name


# Create Gradio interface
iface = gr.Interface(
    fn=extract_numbers_and_preview,  # Function for processing
    inputs=gr.File(label="Upload a PDF"),  # File upload
    outputs=[
        gr.Textbox(label="Found measurements"),  # Display extracted numbers
        gr.File(label="PDF preview")  # PDF as download and preview
    ],
    title="📄 PDF Measurement Extractor",
    description="This tool extracts measurements from a PDF file and displays the PDF.",
)

# Launch Gradio app
iface.launch()