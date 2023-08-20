from object_detection.detect import run_detect
from pose_estimate.src.predict import run_predict

if __name__ == "__main__":
    run_detect(model_path='./runs/detect/train/weights/best.pt', 
            img_path='./data/pipe/test/images/1000.png')

    run_predict()