#coding:utf-8
import cv2
import sys
from PIL import Image
import numpy
sys.path.append('..')
import os
import time

class FaceDetect(object):

    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), "face_detect.xml"))

    def detect(self, image):
        '''image 为 PIL 的 Image 对象'''

        if getattr(image, 'layers', None):
            gray = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_BGR2GRAY)
        else:
            gray = numpy.asarray(image)

        # Detect faces in the image
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
            # flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        return len(faces) > 0

    def detect_and_draw(self, img_path):
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
            # flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Faces found", image)
        cv2.waitKey(0)

face_detect = FaceDetect()

if __name__ == '__main__' :
    image_path = '/Users/hulk/Workspace/PycharmProjects/FaceDetect/test.jpg'
    start_time = time.time()
    for i in range(0, 1):
        image = Image.open(image_path)
        flag = face_detect.detect(image)
        print(flag)
    end_time = time.time()

    print(end_time - start_time)

    # image = Image.open(image_path)
    # image.show()
    # img = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
    # cv2.imshow("OpenCV", img)
    # cv2.waitKey()