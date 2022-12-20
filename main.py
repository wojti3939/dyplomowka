import cv2
import ChessboardDetection

from roboflow import Roboflow
rf = Roboflow(api_key="0SN1gMRcHyIDN1zAHMU3")
project = rf.workspace().project("chess-pieces-detection-tahle")
model = project.version(2).model

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    ChessboardDetection.boarddetection(frame)
    preds = model.predict(frame, confidence=60, overlap=30).json()
    detections = preds['predictions']
    # print(detections)
    for box in detections:
        x1 = box['x'] - box['width'] / 2
        x2 = box['x'] + box['width'] / 2
        y1 = box['y'] - box['height'] / 2
        y2 = box['y'] + box['height'] / 2
        # print(x1," ", x2, " ", y1," ", y2)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 3)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    # cv2.waitKey(0)
    # if cv2.waitKey(1) == ord('q'):
    #     break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()