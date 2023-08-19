from pose_estimate.src.predict import run_predict
from ultralytics import YOLO

model = YOLO(model='./runs/detect/train/weights/best.pt', task='detect')
results = model.predict(
   source='./data/pipe/test/images/1000.png',
   save=True,
   conf=0.25,
)
for r in results:
    
    # annotator = Annotator(frame)
    
    boxes = r.boxes
    for box in boxes:
        
        b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
        c = box.cls
        print(b, c)
run_predict()