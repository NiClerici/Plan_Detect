import cv2
import os
import numpy as np
import gradio as gr
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog


# Image preprocessing function (scaling & sharpening)
def preprocess_image(image, scale_factor=1.5, sharpen=True):
    height, width = image.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    upscaled = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    if sharpen:
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        upscaled = cv2.filter2D(upscaled, -1, kernel)

    return upscaled


# Detectron2 configuration
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
# Set the path to your model weights (adjust the path as needed)
cfg.MODEL.WEIGHTS = "/Users/nicoclerici/Documents/Bewerbung/DBew/Prototyp_eBew/prototyp/Backend/model_final.pth"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 16
cfg.MODEL.DEVICE = "cpu"  # or "cuda" if GPU is available
cfg.INPUT.MIN_SIZE_TEST = 1024
cfg.INPUT.MAX_SIZE_TEST = 2048
cfg.TEST.DETECTIONS_PER_IMAGE = 50
cfg.MODEL.RPN.NMS_THRESH = 0.8
cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.5

# Set metadata for classes (translated into English)
dataset_name = "train_dataset"
MetadataCatalog.get(dataset_name).set(thing_classes=[
    "Street Name", "New Building", "Existing Building",
    "Surveyor Stamp", "North Arrow", "Scale", "Parcel Boundary", "Dimension Line",
    "Signatures", "Title Information", "Building Substructure", "Legend",
    "M.ü.M", "Building Demolition", "Parcel Number", "Building Number"
])
metadata = MetadataCatalog.get(dataset_name)

# Initialize the model
predictor = DefaultPredictor(cfg)
print("✅ Detectron2 model loaded successfully!")


def segment_image(input_image):
    """
    Performs instance segmentation on the input image.
    The input image is expected as a numpy array in RGB format.
    """
    # Preprocess the image (scaling & sharpening)
    processed_img = preprocess_image(input_image, scale_factor=2.0)

    # Convert the image to BGR as Detectron2 expects BGR images
    image_bgr = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)

    # Perform inference
    outputs = predictor(image_bgr)

    if outputs["instances"].has("pred_boxes") and len(outputs["instances"]) > 0:
        instances = outputs["instances"].to("cpu")
        # Create a Visualizer with the metadata (includes class names)
        visualizer = Visualizer(processed_img[:, :, ::-1], metadata, scale=1.0)
        out = visualizer.draw_instance_predictions(instances)
        result_image = out.get_image()[:, :, ::-1]
        return result_image
    else:
        # If no objects are detected, return the preprocessed image
        return processed_img


# Create Gradio interface
iface = gr.Interface(
    fn=segment_image,
    inputs=gr.Image(type="numpy", label="Upload an Image"),
    outputs=gr.Image(type="numpy", label="Segmented Output"),
    title="Detectron2 Instance Segmentation",
    description="Upload an image to get instance segmentation results."
)

if __name__ == "__main__":
    iface.launch()
