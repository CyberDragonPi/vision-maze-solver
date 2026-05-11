import cv2
import numpy

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


    def hsv_filter_stream(self):
        cv2.namedWindow("HSV Filter")

        cv2.createTrackbar("H min", "HSV Filter", 80, 179, lambda x: None)
        cv2.createTrackbar("S min", "HSV Filter", 100, 255, lambda x: None)
        cv2.createTrackbar("V min", "HSV Filter", 70, 255, lambda x: None)

        cv2.createTrackbar("H max", "HSV Filter", 125, 179, lambda x: None)
        cv2.createTrackbar("S max", "HSV Filter", 210, 255, lambda x: None)
        cv2.createTrackbar("V max", "HSV Filter", 190, 255, lambda x: None)

        while True:
            frame = self.get_frame()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower = numpy.array([
                cv2.getTrackbarPos("H min", "HSV Filter"),
                cv2.getTrackbarPos("S min", "HSV Filter"),
                cv2.getTrackbarPos("V min", "HSV Filter")
            ])

            upper = numpy.array([
                cv2.getTrackbarPos("H max", "HSV Filter"),
                cv2.getTrackbarPos("S max", "HSV Filter"),
                cv2.getTrackbarPos("V max", "HSV Filter")
            ])

            mask = cv2.inRange(hsv, lower, upper)

            result = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow("HSV Filter", result)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


    