from ultralytics import YOLO

source = "https://ultralytics.com/images/bus.jpg" # 自身が検出したいデータの位置
model = YOLO('./data/detect/weights/best.pt') # 学習した重みデータ

model.predict(source, save=True, imgsz=640, conf=0.5)