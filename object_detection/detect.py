from ultralytics import YOLO
from common.pipe import Pipe 

class Detect():
    def __init__(self, model_path):
        self.__yolo_model = YOLO(model=model_path, task='detect')

    def run_detect(self, img_path) -> list:
        pred = self.__yolo_model.predict(
            source=img_path,
            save=True,
            conf=0.3,
        )

        detection_results = []
        for result in pred:
            boxes = result.boxes
            for box in boxes:
                _box = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
                size = (abs(_box[0].item() - _box[2].item()) + abs(_box[1].item() - _box[3]).item()) / 2
                position = [(_box[0].item() + _box[2].item()) / 2 , (_box[1].item() + _box[3].item()) / 2]
                class_num = int(box.cls.item())
                if class_num == 0:
                    name = "bent"
                else:
                    name = "junction"
                pipe = Pipe(class_num, name, position, size)
                detection_results.append(pipe)
        
        return detection_results