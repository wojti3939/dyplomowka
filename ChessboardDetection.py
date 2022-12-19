import cv2
import numpy as np

# min, min upper left
# max, max lower right

class Tile:
    def __init__(self, p1, p2, p3, p4, piece, color):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.piece = piece
        self.color = color

class Corner:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x} y: {self.y}"

    __repr__ = __str__


def boarddetection(frame):


    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # The function attempts to determine whether the input image is a view of the chessboard pattern
    # and locate the internal chessboard corners.
    is_ret, corners = cv2.findChessboardCorners(frame, (7, 7),
                                                flags=cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                cv2.CALIB_CB_FAST_CHECK +
                                                cv2.CALIB_CB_NORMALIZE_IMAGE)

    # Creating list of tupples with detected coordinates
    TmpListToSort = []

    corners = [Corner(item[0][0], item[0][1]) for item in corners]
    corners.sort(key=lambda corner: corner.x)

    corner_chunks = [corners[0:7], corners[7:14], corners[14:21], corners[21:28], corners[28:35], corners[35:42], corners[42:49]]

    for chunk in corner_chunks:
        chunk.sort(key=lambda corner: corner.y)


    if is_ret:
        # print("corners " + str(corners))
        fnl = cv2.drawChessboardCorners(frame, (7, 7), corners[0], is_ret)
        # cv2.imshow("fnl", fnl)
        # cv2.waitKey(0) # Stop frame when chessboard found
    else:
        print("No Checkerboard Found")
    # 311,257     277, 223
    # cv2.circle(frame, (295,361), radius=5, color=(0, 0, 255), thickness=5)
    # cv2.circle(frame, (329, 361), radius=5, color=(0, 0, 0), thickness=5)

