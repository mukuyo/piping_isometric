from object_detection.detect import Detect
from pose_estimate.src.predict import Pose

model_path = './runs/detect/train/weights/best.pt'
img_path = './data/pipe/test/images/1000.png'
class Main:
    def __init__(self):
        self.detect = Detect(model_path=model_path)
        self.pose = Pose()

    def run(self):
        detection_results = self.detect.run_detect(img_path=img_path)
        for i, result in enumerate(detection_results):
            results = self.pose.predict(img_path=img_path, result=result)
            print(results.name , results.position, results.size, results.pose)
            break

if __name__ == "__main__":
    print("init model")
    main = Main()
    print("start predict")
    main.run()
