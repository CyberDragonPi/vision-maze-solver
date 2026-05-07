import cv2

class PathVisualizer:
    def __init__(self, image):
        self.image = image
        self.color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    def draw_path(self, path, color=(0, 0, 255), thickness=1):
        for x, y in path:
            cv2.circle(self.color_image, (y, x), thickness, color, -1)

        return self.color_image

    def show(self, title="Path"):
        cv2.imshow(title, self.color_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, filename="solved_maze.jpg"):
        cv2.imwrite(filename, self.color_image)