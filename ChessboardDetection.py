import cv2
# from dictionary import Tiles


class Tile:
    def __init__(self, p1, p2, p3, p4, pieceID):
        self.p1 = p1 # top left corner
        self.p2 = p2 # top right corner
        self.p3 = p3 # bottom right corner
        self.p4 = p4 # bottom left corner
        self.pieceID = pieceID # piece ID for example 'A8', 'G3'



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x} y: {self.y}"

    __repr__ = __str__


def draw_corners(corner_chunks, frame, color=(0, 0, 255), text_offset = 2):
    for i, chunk in enumerate(corner_chunks):
        for j, corner in enumerate(chunk):
            x, y = int(corner.x), int(corner.y)
            cv2.circle(frame, (x, y), radius=1, color=color, thickness=3)
            cv2.putText(frame, f"{j},{i}", (x + text_offset, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), thickness=1)


# def draw_tile(color=):


def boarddetection(frame):

    # The function attempts to determine whether the input image is a view of the chessboard pattern
    # and locate the internal chessboard corners.
    is_ret, corners = cv2.findChessboardCorners(frame, (7, 7),
                                                flags=cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                cv2.CALIB_CB_FAST_CHECK +
                                                cv2.CALIB_CB_NORMALIZE_IMAGE)

    # creating list of (x,y) points
    # sorting to organize points into chunks
    # each chunk represents 7 points in horizontal orientation
    # starting from top to bottom
    corners = [Point(item[0][0], item[0][1]) for item in corners]
    corners.sort(key=lambda corner: corner.y)

    corner_chunks = [corners[0:7], corners[7:14], corners[14:21], corners[21:28], corners[28:35], corners[35:42], corners[42:49]]

    for chunk in corner_chunks:
        chunk.sort(key=lambda corner: corner.x)

    # filling all corners with vector movement
    fillToTopChunk = [Point(firstH.x, 2*firstH.y - secondH.y) for firstH, secondH in zip(corner_chunks[0], corner_chunks[1])]
    fillToBottomChunk = [Point(eighthH.x, 2*eighthH.y - seventhH.y) for seventhH, eighthH in zip(corner_chunks[-2], corner_chunks[-1])]

    corner_chunks.insert(0, fillToTopChunk)
    corner_chunks.append(fillToBottomChunk)

    for chunk in corner_chunks:
        secondV, thirdV = chunk[0:2]
        fillToLeftChunk = Point(2*secondV.x - thirdV.x,secondV.y)
        chunk.insert(0, fillToLeftChunk)

    for chunk in corner_chunks:
        seventhV, eighthV = chunk[6:8]
        fillToRightChunk = Point(2*eighthV.x - seventhV.x,seventhV.y)
        chunk.append(fillToRightChunk)

    row_ids = "87654321"
    column_ids = "ABCDEFGH"

    tiles = []
    for i in range(8):
        for j in range(8):
            p1 = corner_chunks[i][j]
            p2 = corner_chunks[i][j+1]
            p3 = corner_chunks[i+1][j+1]
            p4 = corner_chunks[i+1][j]
            row_id = row_ids[i]
            column_id = column_ids[j]
            tile = Tile(p1, p2, p3, p4, f"{row_id}{column_id}")
            tiles.append(tile)
            cv2.rectangle(frame, p1, p3, (0, 0, 255))

    if is_ret:

        draw_corners(corner_chunks, frame)
        # print("corners " + str(corners))
        # fnl = cv2.drawChessboardCorners(frame, (7, 7), corners, is_ret)
        # cv2.imshow("fnl", fnl)
        cv2.waitKey(0) # Stop frame when chessboard found
    else:
        print("No Checkerboard Found")

    cv2.circle(frame, (137, 338), radius=3, color=(0,0,0), thickness=3)
    cv2.circle(frame, (137, 373), radius=3, color=(0, 0, 0), thickness=3)
