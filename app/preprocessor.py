import cv2


class Preprocessing:
    def grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
