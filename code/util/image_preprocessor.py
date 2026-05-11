import cv2
from matplotlib.pyplot import hsv
import numpy as np

class ImagePreprocessor:
    def __init__(self):
        self.M = None
        self.M_inv = None


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


    def preprocess(self, image=None):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        binary = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2  
        )

        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        return gray, blurred, binary


    def find_contours(self, blurred_image):
        edges = cv2.Canny(blurred_image, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)

        """
        debug = cv2.cvtColor(blurred_image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(debug, [largest], -1, (0, 255, 0), 2)

        cv2.imshow("Largest Contour", debug)
        cv2.waitKey(0)
        """

        peri = cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, 0.02 * peri, True)

        if len(approx) == 4:
            return approx

        return None
    

    def apply_mask(self, image, contour):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        masked_image = cv2.bitwise_and(image, image, mask=mask)

        return masked_image
    

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

        self.M = cv2.getPerspectiveTransform(rect, dst)
        self.M_inv = np.linalg.inv(self.M)
        warped = cv2.warpPerspective(image, self.M, (maxWidth, maxHeight))

        return warped
    

    def to_warped(self, pt):
        p = np.array([[[pt[1], pt[0]]]], dtype=np.float32)
        out = cv2.perspectiveTransform(p, self.M)
        x, y = out[0][0]
        return (int(y), int(x))
    

    def warp_to_original(self, pt):
        p = np.array([[[pt[1], pt[0]]]], dtype=np.float32)
        out = cv2.perspectiveTransform(p, self.M_inv)
        x, y = out[0][0]
        return (int(y), int(x))


    def clean_binary(self, binary):
        kernel_close1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close1)

        kernel_close2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel_close2)

        return cleaned


    def add_border_walls(self, binary, thickness=5):
        h, w = binary.shape
        bordered = binary.copy()

        bordered[:thickness, :] = 255
        bordered[h - thickness:, :] = 255

        bordered[:, :thickness] = 255
        bordered[:, w - thickness:] = 255

        return bordered


    def to_grid(self, binary_image):
        grid = (binary_image == 0).astype(np.uint8)
        return grid


    def find_start_end_hsv(self, image, neighbourhood=1):
        h, w = image.shape[:2]
        path_value = 0

        start = None
        n = max(h, w)

        for i in range(1, n - neighbourhood):
            x1 = max(0, i - neighbourhood)
            x2 = min(h, i + neighbourhood)
            y1 = max(0, i - neighbourhood)
            y2 = min(w, i + neighbourhood)

            neighborhood = image[x1:x2, y1:y2]

            if np.all(neighborhood == path_value):
                start = (i, i)
                break

        end = None
        for i in range(n - neighbourhood, neighbourhood - 1, -1):
            cx = min(i, h - 1)
            cy = min(i, w - 1)
            x1 = max(0, cx - neighbourhood)
            x2 = min(h, cx + neighbourhood)
            y1 = max(0, cy - neighbourhood)
            y2 = min(w, cy + neighbourhood)

            neighborhood = image[x1:x2, y1:y2]

            if np.all(neighborhood == path_value):
                end = (i, i)
                break
        
        #print(f"Start: {start}, End: {end}")
        return start, end


    def show_image(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def save_image(self, title, image):
        cv2.imwrite(title, image)