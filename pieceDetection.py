import cv2

from roboflow import Roboflow
rf = Roboflow(api_key="0SN1gMRcHyIDN1zAHMU3")
project = rf.workspace().project("chess-pieces-detection-tahle")
model = project.version(2).model

def piecedetection(frame):
    preds = model.predict(frame, confidence=80, overlap=30).json()
    detections = preds['predictions']
    # print(detections)
    for box in detections:
        x1 = box['x'] - box['width'] / 2
        x2 = box['x'] + box['width'] / 2
        y1 = box['y'] - box['height'] / 2
        y2 = box['y'] + box['height'] / 2
        print(box)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 3)