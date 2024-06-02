from ultralytics import YOLO

# モデルのロード（小型モデルの例：yolov8s）
model = YOLO('yolov8s.pt')

# トレーニングの実行
results = model.train(data='data/detect/data.yaml', epochs=100, imgsz=640)