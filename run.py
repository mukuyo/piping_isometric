from object_detection.detect import Detect
from pose_estimate.src.predict import Pose

model_path = './runs/detect/train/weights/best.pt'
img_path = './data/pipe/test/images/256_png.rf.582ddfe4e5439094ba38ffa55b1af392.jpg'

class Main:
    def __init__(self):
        self.detect = Detect(model_path=model_path)
        self.pose = Pose()

    def run(self):
        detection_results = self.detect.run_detect(img_path=img_path)

        points = []
        for i, result in enumerate(detection_results):
            results, pts = self.pose.predict(img_path=img_path, result=result)
            points.append(pts)
            print(results.name , results.position, results.size, results.pose)
            
        self.pose.result_desplay(points)

if __name__ == "__main__":
    print("init model")
    main = Main()
    print("start predict")
    main.run()
