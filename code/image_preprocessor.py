import cv2
from matplotlib.pyplot import grid
import numpy as np

class ImagePreprocessor:
    def __init__(self, path="labirinto.jpg"):
        self.path = path


    def to_binary(self, gray_image):
        binary = cv2.adaptiveThreshold(
            gray_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,  
            2    
        )
        return binary
    

    def _order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)] 
        rect[2] = pts[np.argmax(s)] 

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  
        rect[3] = pts[np.argmax(diff)]  

        return rect


    def preprocess(self):
        image = cv2.imread(self.path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        _, binary = cv2.threshold(
            blurred,
            127,
            255,
            cv2.THRESH_BINARY_INV
        )

        return gray, blurred, binary


    def find_contours(self, blurred_image):
        edges = cv2.Canny(blurred_image, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)

        peri = cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, 0.02 * peri, True)

        if len(approx) == 4:
            return approx

        return None
    
    
    def four_point_transform(self, image, pts):
        rect = self._order_points(pts.reshape(4, 2))

        (tl, tr, br, bl) = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = int(max(widthA, widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = int(max(heightA, heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped


    def clean_binary(self, binary):
        kernel = np.ones((3, 3), np.uint8)

        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned


    def add_border_walls(self, binary, thickness=5):
        h, w = binary.shape
        bordered = binary.copy()

        bordered[:thickness, :] = 255
        bordered[h-thickness:, :] = 255

        bordered[:, :thickness] = 255
        bordered[:, w-thickness:] = 255

        return bordered


    def to_grid(self, binary_image):
        grid = (binary_image == 0).astype(np.uint8)
        return grid


    def find_start_end_points(self, grid):
        h, w = grid.shape
        start = None
        end = None

        for d in range(h + w):
            for i in range(d + 1):
                j = d - i
                if i < h and j < w:
                    if grid[i, j] == 1:
                        start = (i, j)
                        break
            if start is not None:
                break

        for d in range(h + w):
            for i in range(d + 1):
                j = d - i
                ii = h - 1 - i
                jj = w - 1 - j
                if 0 <= ii < h and 0 <= jj < w:
                    if grid[ii, jj] == 1:
                        end = (ii, jj)
                        break
            if end is not None:
                break

        return start, end


    def show_image(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()