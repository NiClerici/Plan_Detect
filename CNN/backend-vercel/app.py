import cv2
import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from huggingface_hub import hf_hub_download
# Detectron2 nachträglich installieren (nur wenn nötig)
try:
    import detectron2
except ImportError:
    print("📦 Installing detectron2...")
    os.system("pip install git+https://github.com/facebookresearch/detectron2.git")


# Flask setup
app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app, origins=["https://ebeg-frontend.vercel.app"])



# Upload folder setup
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Detectron2 configuration with Hugging Face weights
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
))
model_path = hf_hub_download(repo_id="clery27/plan_detect", filename="model_final.pth")
cfg.MODEL.WEIGHTS = model_path
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 16
cfg.MODEL.DEVICE = "cpu"
cfg.INPUT.MIN_SIZE_TEST = 1024
cfg.INPUT.MAX_SIZE_TEST = 2048
cfg.TEST.DETECTIONS_PER_IMAGE = 50
cfg.MODEL.RPN.NMS_THRESH = 0.7
cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.5

# Metadata setup
dataset_name = "train_dataset"
MetadataCatalog.get(dataset_name).set(thing_classes=[
    "Strassenname", "Gebaeude Neu", "Gebaeude Bestehend",
    "GeometerStempel", "Nordpfeil", "Massstab", "Parzellengrenze", "Masslinie",
    "Unterschriften", "Titelinformation", "Gebaeude Untergrund", "Legende",
    "M.ü.M", "Gebaeude Abbruch", "Parzellennummer", "Gebaeudenummer"
])
metadata = MetadataCatalog.get(dataset_name)
predictor = DefaultPredictor(cfg)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return jsonify({"error": "Unsupported file format"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({"error": "Image could not be read"}), 400

    outputs = predictor(image)

    if outputs["instances"].has("pred_boxes") and len(outputs["instances"]) > 0:
        v = Visualizer(image[:, :, ::-1], metadata, scale=2.0)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        processed_file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], "processed_" + file.filename
        )
        cv2.imwrite(processed_file_path, out.get_image()[:, :, ::-1])
        return jsonify({
            "original": f"/static/uploads/{file.filename}",
            "processed": f"/static/uploads/processed_{file.filename}"
        })

    return jsonify({"error": "No objects detected"}), 200

@app.route('/list-processed-images', methods=['GET'])
def list_processed_images():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    processed_files = [
        f"/static/uploads/{file}" for file in files if file.startswith("processed_")
    ]
    return jsonify({"images": processed_files})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
