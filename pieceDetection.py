import cv2
import chessboardDetection
import fusion_iou

from roboflow import Roboflow
rf = Roboflow(api_key="0SN1gMRcHyIDN1zAHMU3")
project = rf.workspace().project("chess-pieces-detection-tahle")
model = project.version(2).model


# class PieceRecognized:
#     def __init__(self, ):


def piece_detection(frame):
    preds = model.predict(frame, confidence=80, overlap=30).json()
    detections = preds['predictions']
    # print(detections)
    for box in detections:
        x1 = box['x'] - box['width'] / 2
        x2 = box['x'] + box['width'] / 2
        y1 = box['y'] - box['height'] / 2
        y2 = box['y'] + box['height'] / 2
        boxA = [x1, y1, x2, y2]
        # print(box)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 1)

        for tile in chessboardDetection.tiles:
            boxB = [tile.p1.x, tile.p1.y, tile.p3.x, tile.p3.y]
            iou = fusion_iou.bb_intersection_over_union(boxA, boxB)
            print(tile.tile_id, ": ", iou)
            cv2.rectangle(frame, (int(tile.p1.x), int(tile.p1.y)), (int(tile.p3.x), int(tile.p3.y)), (0, 255, 0), 1)
            # print(tile.tile_id)

