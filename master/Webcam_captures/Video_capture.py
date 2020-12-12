import cv2

# import cv
from PyQt5 import QtCore


def getCapture():
    # capture = cv.CaptureFromCAM(0)
    capture = cv2.VideoCapture(-1)
    # cv.NamedWindow("capture", cv.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow("capture", cv2.WINDOW_AUTOSIZE)

    i = 0
    while True:
        # frame = cv.QueryFrame(capture)
        result, img = capture.read()
        # cv.ShowImage("capture", frame)
        cv2.imshow("capture", img)
        # cv.WaitKey(10)
        cv2.waitKey(10)
        path = "capture%.4d.jpg" % i  # Уникальное имя для каждого кадра
        # cv.SaveImage(path, frame)
        cv2.imwrite(path, img)
        i += 1


def getCaprure_2():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Video', frame)
        # cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


class Video_capture(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.capture.read()
            self.signal.emit(frame)



if __name__ == '__main__':
    # getCapture()
    getCaprure_2()
