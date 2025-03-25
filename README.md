
# Plan Detection

**Plan Detection** is a comprehensive toolkit designed to accurately detect and extract dimension lines ("Masslinien") from architectural plans in PDF and PNG formats. It combines advanced techniques including convolutional neural networks (CNNs), text extraction, and multimodal vision-language modeling.

---

## 📁 Project Structure

```
.
├── CNN
│   └── Inferenz_CNN.py
├── Data
│   ├── PDF
│   │   └── TestSit.Plan.pdf
│   └── PNG
│       └── TestSit.Plan.jpg
├── Granite_Vision
│   └── Inferenz.py
├── PyMuPDF
│   └── PyMUPDF.py
├── README.md
├── get-pip.py
└── token
```

---

## 🚀 Workflows

The primary goal across all workflows is the precise identification of dimension lines:

### 🔍 CNN (Detectron2)
- **Input:** PNG images
- **Technique:** Object detection using Detectron2, specifically tuned for dimension line detection.
- **Script:** [`CNN/Inferenz_CNN.py`](./CNN/Inferenz_CNN.py)

### 📑 PyMuPDF
- **Input:** PDF documents
- **Technique:** Text-based extraction using PyMuPDF to identify numeric dimension annotations.
- **Script:** [`PyMuPDF/PyMUPDF.py`](./PyMuPDF/PyMUPDF.py)

### 🖼️ Granite Vision
- **Input:** PDF or PNG files
- **Technique:** Multimodal analysis using IBM Granite Vision for automatic dimension line detection.
- **Script:** [`Granite_Vision/Inferenz.py`](./Granite_Vision/Inferenz.py)

---

## 🗃️ Test Data

Sample files for testing and demonstration are included in the [`Data`](./Data/) directory:

- **PDF Example:** [`TestSit.Plan.pdf`](./Data/PDF/TestSit.Plan.pdf)
- **PNG Example:** [`TestSit.Plan.jpg`](./Data/PNG/TestSit.Plan.jpg)

---

## 🛠️ Installation

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

or manually install necessary packages:

```bash
pip install detectron2 PyMuPDF transformers torch gradio opencv-python-headless
```

---

## 💡 Usage

Launch individual scripts according to your needs. For instance, to run the CNN inference:

```bash
python CNN/Inferenz_CNN.py
```

Or use Gradio interfaces provided in scripts for interactive analysis.

---

## 🤝 Contribution

Contributions, feature suggestions, and bug reports are welcome. Please submit issues or pull requests on [GitHub](https://github.com/NiClerici/Plan_Detect).

---

## 📜 License

Specify your project's license here (e.g., MIT, Apache-2.0, etc.)

---

📌 [Project Repository](https://github.com/NiClerici/Plan_Detect)

Thank you for exploring **Plan Detection**!
