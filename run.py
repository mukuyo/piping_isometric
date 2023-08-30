"""This is a main script"""
import yaml
from object_detection.detect import Detect
from pose_estimate.src.predict import Pose
from isometric.src.iso import Iso


class Main:
    """Main class"""
    def __init__(self, _cfg):
        self.cfg = _cfg
        self.detect = Detect(self.cfg)
        self.pose = Pose(self.cfg)
        self.isometric = Iso(self.cfg)

    def run(self):
        """run program"""
        detection_results = self.detect.run_detect()
        pose_results = self.pose.predict(results=detection_results)
        self.isometric.generate_iso(pose_results)

if __name__ == "__main__":
    with open('./config/main.yaml', 'r', encoding="utf8") as yml:
        cfg = yaml.safe_load(yml)

    print("init model")
    main = Main(cfg)

    print("start predict")
    main.run()
