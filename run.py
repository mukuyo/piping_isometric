from object_detection.detect import Detect
from pose_estimate.src.predict import Pose
from isometric.iso import Iso
import yaml

class Main:
    def __init__(self, cfg):
        self.cfg = cfg
        self.detect = Detect(self.cfg)
        self.pose = Pose(self.cfg)
        self.isometric = Iso(self.cfg)

    def run(self):
        detection_results = self.detect.run_detect()
        pose_results = self.pose.predict(results=detection_results)
        self.isometric.run(pose_results)

if __name__ == "__main__":
    with open('./config/main.yaml', 'r') as yml:
        cfg = yaml.safe_load(yml)

    print("init model")
    main = Main(cfg)
    print("start predict")
    main.run()
