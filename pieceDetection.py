import cv2
import chessboardDetection
import fusion_iou

# Import hosted api inference from Roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="0SN1gMRcHyIDN1zAHMU3")
project = rf.workspace().project("chess-pieces-detection-tahle")
model = project.version(2).model

# Constant chosen experimentally for proper piece to tile recognition
MIN_IOU_TO_RECOGNIZE = 0.2

# global list of properly recognized and assigned pieces
pieces_recognized = []
def piece_detection(frame):

    # assigns into preds variable array of predictions
    # "predictions": [
    #     {
    #         "x", horizontal center point of the detected object
    #         "y", vertical center point of the detected object
    #         "width", width of the bounding box
    #         "height", height of the bounding box
    #         "class," class label of the detected object
    #         "confidence", model's confidence that the detected object has the correct label and position coordinates
    #      }
    #  ]

    preds = model.predict(frame, confidence=80, overlap=30).json()
    detections = preds['predictions']

    for box in detections:
        # Calculating (x, y) of upper left and lower right Points
        x1 = box['x'] - box['width'] / 2
        x2 = box['x'] + box['width'] / 2
        y1 = box['y'] - box['height'] / 2
        y2 = box['y'] + box['height'] / 2
        boxA = [x1, y1, x2, y2]

        # drawing BoundingBox of each detected piece
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 1)

        list_tmp = []

        for tile in chessboardDetection.tiles:
            boxB = [tile.p1.x, tile.p1.y, tile.p3.x, tile.p3.y]
            # calculating iou of tiles and figures bounding boxes
            iou = fusion_iou.bb_intersection_over_union(boxA, boxB)
            tmp = {"tile": tile.tile_id, "piece": box['class'], "iou": iou}
            if not(iou < MIN_IOU_TO_RECOGNIZE):
                list_tmp.append(tmp)

            # drawing detected tiles
            cv2.rectangle(frame, (int(tile.p1.x), int(tile.p1.y)), (int(tile.p3.x), int(tile.p3.y)), (0, 255, 0), 1)

        if (list_tmp):
            # Appending to list most recognized piece
            list_tmp.sort(reverse=True, key=lambda tmp: tmp["iou"])
            pieces_recognized.append(list_tmp[0])
            text = list_tmp[0]['tile'] + ":" + box['class'] + ("%.2f" % box['confidence'])

            # showing on wich tile piece is detected and model's confidence that the object has correct label and coordinates
            cv2.putText(frame, text, (int(box['x']), int(box['y'])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), thickness=1)
            list_tmp.clear()

