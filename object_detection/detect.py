from ultralytics import YOLO
from common.pipe import Pipe 

def run_detect(model_path, img_path):
    yolo_model = YOLO(model=model_path, task='detect')
    pred = yolo_model.predict(
    source=img_path,
    save=True,
    conf=0.25,
    )
    for result in pred:
        boxes = result.boxes
        for box in boxes:
            _box = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            _class = box.cls
            Pipe(_class, _box)
            print(b, c)