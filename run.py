from object_detection.detect import Detect
from pose_estimate.src.predict import Pose
from draw_isometric.main import Isometric
from common.pipe import Pipe

model_path = './data/detect/weights/best.pt'
img_path = './data/detect/datasets/pipe/test/images/1000.png'
output_path = './data/isometric/result/result.jpg'

class Main:
    def __init__(self):
        self.detect = Detect(model_path=model_path)
        self.pose = Pose()
        self.isometric = Isometric(output_path=output_path)

    def run(self):
        detection_results = self.detect.run_detect(img_path=img_path)
        pose_results = self.pose.predict(img_path=img_path, results=detection_results)
        self.isometric.run(pose_results)

if __name__ == "__main__":
    print("init model")
    main = Main()
    print("start predict")
    main.run()
