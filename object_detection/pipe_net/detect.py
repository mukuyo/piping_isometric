import argparse
from pathlib import Path

from PIL import Image
from common.pipe import Pipe
from .src.detector import Detector


class PipeNet:
    """Pipe network class"""
    def __init__(self, conf):
        self.cfg = conf
        self.__detector = Detector(self.cfg)

    def run_detect(self):
        """run detect"""
        detection_results = []
        detections, img_paths = self.__detector.detect_from_path()
        
        for detection, img_path in zip(detections, img_paths):
            for box in detection:
                print(
                    f"{box['class_name']} {box['confidence']:.0%} "
                    f"({box['x1']:.0f}, {box['y1']:.0f}, {box['x2']:.0f}, {box['y2']:.0f})"
                )
                size = (abs(box['x1'] - box['x2']) + abs(box['y1'] - box['y2'])) / 2
                position = ((box['x1'] + box['x2']) / 2, (box['y1'] + box['y2']) / 2)
                pipe = Pipe(box['class_name'], position, size)
                detection_results.append(pipe)
            img = Image.open(img_path)
            self.__detector.draw_boxes(img, detection)
            img.save(Path(self.cfg['detect']['pipe_net']['output_path']) / Path(img_path).name)

        return detection_results