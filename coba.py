from ultralytics import YOLO

model = YOLO('model/best.pt') #bisa juga yng best.pt

#data = 'data/jalan.mp4'
model.predict(source=0, show=True,conf=0.5)