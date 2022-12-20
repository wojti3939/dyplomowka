import cv2
import chessboardDetection
import pieceDetection
import fusion_iou
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

    chessboardDetection.boarddetection(frame)
    pieceDetection.piece_detection(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    # if cv2.waitKey(1) == ord('q'):
    #     break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()