import cv2
import numpy as np
import glob

# ---------------------------
# LOAD IMAGES
# ---------------------------
image_paths = sorted(glob.glob("../maps/*.png"))
index = 0

def nothing(x):
    pass

# ---------------------------
# TRACKBARS
# ---------------------------
cv2.namedWindow("Trackbars")

cv2.createTrackbar("R min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R max", "Trackbars", 255, 255, nothing)

cv2.createTrackbar("G min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G max", "Trackbars", 255, 255, nothing)

cv2.createTrackbar("B min", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("B max", "Trackbars", 255, 255, nothing)

# ---------------------------
# LOOP
# ---------------------------
while True:

    img = cv2.imread(image_paths[index])

    # get trackbar values
    rmin = cv2.getTrackbarPos("R min", "Trackbars")
    rmax = cv2.getTrackbarPos("R max", "Trackbars")

    gmin = cv2.getTrackbarPos("G min", "Trackbars")
    gmax = cv2.getTrackbarPos("G max", "Trackbars")

    bmin = cv2.getTrackbarPos("B min", "Trackbars")
    bmax = cv2.getTrackbarPos("B max", "Trackbars")

    # ---------------------------
    # MASK
    # ---------------------------
    mask = cv2.inRange(
        img,
        (bmin, gmin, rmin),
        (bmax, gmax, rmax)
    )
    result = mask
    cv2.imshow("Result", result)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break
    elif key == ord('d'):
        index = (index + 1) % len(image_paths)
    elif key == ord('a'):
        index = (index - 1) % len(image_paths)
    elif key == ord('s'):
        cv2.imwrite(f"maps/result_{index}.png", result)
        inverted = 255 - mask
        cv2.imwrite(f"maps/inverted_{index}.png", inverted)

        print("Saved!")

    print("min:", rmin, gmin, bmin)
    print("max:", rmax, gmax, bmax)

cv2.destroyAllWindows()