#!/usr/bin/python

import cv2
import sys
from PyQt4 import QtGui, QtCore
from scipy.misc import toimage
import numpy as np
import ImageQt
from scipy.cluster.vq import kmeans2, vq
from sklearn import svm
from PIL import ImageDraw

import category
from helpers import FEATURE_TYPES

import warnings
warnings.simplefilter('default')

cam = cv2.VideoCapture(0)


class MLUI(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setCentralWidget(ContainerWidget())
        self.setWindowTitle("Recognizer")
        self.setGeometry(QtCore.QRect(100, 100, 500, 500))
        self.show()


class ContainerWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.vlayout = QtGui.QVBoxLayout()
        self.hlayout = QtGui.QHBoxLayout()
        self.trainbutton = QtGui.QPushButton("Train")
        self.trainbutton.clicked.connect(self.train)
        self.classname = QtGui.QLineEdit()
        self.finalizebutton = QtGui.QPushButton("Finalize")
        self.finalizebutton.clicked.connect(self.finalize)
        self.finalizebutton.setDisabled(True)
        self.hlayout.addWidget(self.classname)
        self.hlayout.addWidget(self.trainbutton)
        self.hlayout.addWidget(self.finalizebutton)
        self.vlayout.addLayout(self.hlayout)
        self.hlayout1 = QtGui.QHBoxLayout()
        self.videowidget = VideoWidget()
#        self.hlayout1.addWidget(self.videowidget)
#        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addWidget(self.videowidget)
        self.setLayout(self.vlayout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.procedure)
        self.timer.start(50)

        self.centroids = None
        self.features = list()
        self.surf = cv2.SURF(1000, extended=False)
        self.categories = dict()
        self.ids = dict()
        self.id = 1
        self.trained = False
        self.recogclass = None

    def procedure(self):
        if self.trained:
            self.recognize()
        self.videowidget.updateWidget(self.recogclass, x)

    def train(self, event):
        classname = self.classname.text()
        if classname == "":
            return
        if len(self.categories) > 1:
            self.finalizebutton.setDisabled(False)
        if classname not in self.categories:
            self.categories[classname] = category.Category(label=classname)
        if self.videowidget.rectangle:
            (x1, y1, x2, y2) = self.videowidget.rectangle
            frame = self.videowidget.frame[y1:y2, x1:x2]
        else:
            frame = self.videowidget.frame
        #cv2.namedWindow("This", 0)
        #cv2.imshow("This", frame)
        keypoints, descriptors = self.surf.detectAndCompute(frame, None)
        self.features.extend(descriptors)
        self.categories[classname].add_feature(descriptors, keypoints,
                                               frame.shape)
        self.videowidget.clearRectangle()

    def recognize(self):
        frame = self.videowidget.frame
        cat = category.Category()
        keypoints, descriptors = self.surf.detectAndCompute(frame, None)
        cat.add_feature(descriptors)
        cat.calc_bagofwords(self.centroids)
        bow = cat.bagofwords[0]
        #print self.lin_clf.predict(bow)
        cat_id = int(self.lin_clf.predict(bow)[0])
        label = None
        for i in self.ids:
            if self.ids[i] == cat_id:
                label = i
        if label:
            self.recogclass = label

    def finalize(self):
        if len(self.categories) < 2:
            return
        features = np.array(self.features)
        self.centroids, _ = kmeans2(features, FEATURE_TYPES)
        #print self.centroids.shape
        X, Y = list(), list()
        for cat in self.categories:
            self.ids[cat] = self.id
            self.id += 1
            self.categories[cat].calc_bagofwords(self.centroids)
            self.categories[cat].bowN(len(features))
            for bow in self.categories[cat].bagofwords:
                X.append(bow)
                Y.append(self.ids[cat])
        self.lin_clf = svm.LinearSVC()
        self.lin_clf.fit(X, Y)
        self.trained = True
        self.trainbutton.setHidden(True)
        self.finalizebutton.setHidden(True)
        self.classname.setHidden(True)
        self.videowidget.clearRectangle()


class VideoWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.frame = None
        self.setMouseTracking(True)
        self.clearRectangle()
        self.drawing = False
        self.image = None
        #self.i = 0

    def clearRectangle(self):
        self.rectangle = None
        self.startXY = None
        self.endXY = None

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.endXY = event.pos()

    def mousePressEvent(self, event):
        self.startXY = event.pos()
        self.drawing = True

    def mouseReleaseEvent(self, event):
        #frame = self.frame.copy()
        self.endXY = event.pos()
        self.drawing = False
        x1, y1 = self.startXY.x(), self.startXY.y()
        x2, y2 = self.endXY.x(), self.endXY.y()
        w, h = abs(x1 - x2), abs(y1 - y2)
        if w == 0 or h == 0:
            return
        x1 = max(x1, x2) - w
        y1 = max(y1, y2) - h
        x2 = x1 + w
        y2 = y1 + h
        self.rectangle = (x1, y1, x2, y2)
        #cv2.imwrite("rectangle%s.jpg" % self.i, frame[y1:y2, x1:x2])
        #self.i += 1
        #cv2.namedWindow("rectangle", 0)
        #cv2.imshow("rectangle", frame[y1:y2, x1:x2])

    def updateWidget(self, text=None):
        _, frame = cam.read()
        self.frame = frame
        if text:
            cv2.putText(frame, str(text), (20, 20),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255))
        self.image = toimage(frame)
        self.update()

    def drawrectangle(self, p1, p2, image):
        draw = ImageDraw.Draw(image)
        draw.rectangle([p1, p2], outline=(255,255, 255))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.startXY and self.endXY:
            p1 = (self.startXY.x(), self.startXY.y())
            p2 = (self.endXY.x(), self.endXY.y())
            self.drawrectangle(p1, p2, self.image)
        if self.image:
            painter.drawImage(QtCore.QPoint(0, 0), ImageQt.ImageQt(self.image))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mlui = MLUI()
    sys.exit(app.exec_())
