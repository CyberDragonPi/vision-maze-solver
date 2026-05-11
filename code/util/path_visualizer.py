import cv2

class PathVisualizer:
    def __init__(self, to_video=False, h=None, w=None):
        self.to_video = to_video
        self.h = h
        self.w = w
        if to_video:
            self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.out = cv2.VideoWriter("maze_output.avi", self.fourcc, 20.0, (w, h))


    def draw_path(self, image, path, color=(0, 255, 0), thickness=1):
        for x, y in path:
            cv2.circle(image, (y, x), thickness, color, -1)

        return image
    

    def show(self, title, image):
        cv2.imshow(title, image)
        key = cv2.waitKey(1) & 0xFF
        return key

    def to_video(self, frame):
        self.out.write(frame)

    def save(self, filename, image):
        cv2.imwrite(filename, image)

    def destroy_all_windows(self):
        cv2.destroyAllWindows()