from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="cafeteria-uao.v2i.yolov8/data.yaml",
    epochs=30,
    imgsz=640,
    batch=4,
    device="cpu"
)
