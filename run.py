from object_detection.detect import Detect
from pose_estimate.src.predict import Pose
from common.pipe import Pipe

model_path = './data/detect/weights/best.pt'
img_path = './data/detect/datasets/pipe/test/images/1000.png'

class Main:
    def __init__(self):
        self.detect = Detect(model_path=model_path)
        self.pose = Pose()

    def run(self):
        detection_results = self.detect.run_detect(img_path=img_path)
        pose_results = self.pose.predict(img_path=img_path, results=detection_results)
        for result in pose_results:
            print(result.name, result.position, result.size, result.pose)

if __name__ == "__main__":
    print("init model")
    main = Main()
    print("start predict")
    main.run()
