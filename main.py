import cv2
import chessboardDetection
import pieceDetection

# Capturing video into cap variable
cap = cv2.VideoCapture(0)

# If it's impossible to capture video exit program with warning
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Board_detection method from chessboardDetection module
    chessboardDetection.board_detection(frame)
    # Piece_detection method from pieceDetection module
    pieceDetection.piece_detection(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    # Program waits for keyboard input to continue
    cv2.waitKey(0)

    # Clears neccesary lists
    pieceDetection.pieces_recognized.clear()
    chessboardDetection.tiles.clear()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()