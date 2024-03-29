import cv2


class Tile:
    def __init__(self, p1, p2, p3, p4, tile_id):
        self.p1 = p1 # top left corner
        self.p2 = p2 # top right corner
        self.p3 = p3 # bottom right corner
        self.p4 = p4 # bottom left corner
        self.tile_id = tile_id # piece ID for example 'A8', 'G3'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x} y: {self.y}"

    __repr__ = __str__

tiles = []

def draw_corners(corner_chunks, frame, color=(0, 0, 255), text_offset = 2):
    for i, chunk in enumerate(corner_chunks):
        for j, corner in enumerate(chunk):
            x, y = int(corner.x), int(corner.y)
            cv2.circle(frame, (x, y), radius=1, color=color, thickness=3)
            cv2.putText(frame, f"{j},{i}", (x + text_offset, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), thickness=1)


# def draw_tile(frame, tile, p1, p2, p3, p4, color=(0, 255, 0)):
#     cv2.rectangle(frame, (int(p1.x), int(p1.y)), (int(p3.x), int(p3.y)), color)
#
#     cv2.putText(frame, tile.tile_id, (int((p4.x + p4.x + p3.x) / 3), int((p2.y + p3.y) / 2)), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.3, color, thickness=1)


def board_detection(frame):

    # The function attempts to determine whether the input image is a view of the chessboard pattern
    # and locate the internal chessboard corners.
    is_ret, corners = cv2.findChessboardCorners(frame, (7, 7),
                                                flags=cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                cv2.CALIB_CB_FAST_CHECK +
                                                cv2.CALIB_CB_NORMALIZE_IMAGE)


    if not is_ret:
        print("No Checkerboard Found")
        return

    # creating list of (x,y) points
    # sorting to organize points into chunks
    # each chunk represents 7 points in horizontal orientation
    # starting from top to bottom
    corners = [Point(item[0][0], item[0][1]) for item in corners]
    corners.sort(key=lambda corner: corner.y)

    corner_chunks = [corners[0:7], corners[7:14], corners[14:21], corners[21:28], corners[28:35], corners[35:42], corners[42:49]]

    # sorting of chunks
    for chunk in corner_chunks:
        chunk.sort(key=lambda corner: corner.x)

    # Calculating Points of all tiles
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


    for i in range(8):
        for j in range(8):
            p1 = corner_chunks[i][j]
            p2 = corner_chunks[i][j+1]
            p3 = corner_chunks[i+1][j+1]
            p4 = corner_chunks[i+1][j]

            row_id = row_ids[i]
            column_id = column_ids[j]
            tile = Tile(p1, p2, p3, p4, f"{column_id}{row_id}")
            tiles.append(tile)

    # draw_corners(corner_chunks, frame)  # Drawing points and coordinates of chessboard tiles

