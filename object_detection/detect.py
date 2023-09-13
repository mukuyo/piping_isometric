"""Detect pipe"""
from ultralytics import YOLO
from common.pipe import Pipe

class Detect():
    """Detect class"""
    def __init__(self, conf):
        self.cfg = conf
        self.__yolo_model = YOLO(model=self.cfg['detect']['model_path'], task='detect')

    def run_detect(self) -> list:
        """run pipe detection"""
        pred = self.__yolo_model.predict(
            source=self.cfg['detect']['rgb_path'] + self.cfg['input_name'],
            save=True,
            conf=self.cfg['detect']['conf_val'],
            project=self.cfg['detect']['output_path'],
            name=self.cfg['detect']['output_name']
        )

        detection_results = []
        for result in pred:
            boxes = result.boxes
            for box in boxes:
                _box = box.xyxy[0]
                size = (abs(_box[0].item() - _box[2].item()) +
                        abs(_box[1].item() - _box[3]).item()) / 2
                position = (int((_box[0].item() + _box[2].item()) / 2),
                            int((_box[1].item() + _box[3].item()) / 2))
                class_num = int(box.cls.item())
                if class_num == 0:
                    name = "elbow"
                else:
                    name = "tee"
                pipe = Pipe(name, position, size)
                detection_results.append(pipe)

        return detection_results
