import cv2


class CameraController:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Cannot read frame")
        return frame

    def save_frame(self, frame, filename="labirinto.jpg"):
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")

    def preview_and_capture(self):
        while True:
            frame = self.get_frame()

            cv2.imshow("Camera Preview", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("c"):
                self.save_frame(frame)
                break

            elif key == ord("q"):
                print("Exit without saving")
                break

        self.release()

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()