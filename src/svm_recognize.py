#!/usr/bin/python

import sys
import cv2
from scipy.cluster.vq import vq
import numpy

import helpers
from category import Category


def recognize(img, category, surf, centroids, linear_clf, ids):
    keypoints, descriptors = surf.detectAndCompute(img, None)

    category = Category(label=category)
    category.add_feature(descriptors)
    category.calc_bagofwords(centroids)

    bow = category.bagofwords[0]
    id = int(linear_clf.predict(bow)[0])
    for i in ids:
        if ids[i] == id:
            label = i
    print category.label, ":", label
    del category


def loadObjects(training_folder):
    if training_folder[-1] != '/':
        training_folder += '/'

    ids = helpers.loadObject(training_folder + 'ids.txt')
    linear_clf = helpers.loadObject(training_folder + 'svm.txt')
    centroids = helpers.loadObject(training_folder + 'centroids.txt')

    return (ids, linear_clf, centroids)


def recognize_routine(recognize_file, training_folder):
    surf = cv2.SURF(250, extended=False)
    ids, linear_clf, centroids = loadObjects(training_folder)

    for line in open(recognize_file):
        try:
            cat, path = line.split(';')
        except:
            print "Error: File not in proper format. Ensure: <category/class name>; <path to image of said category>"
            sys.exit(0)
        path = path.strip()

        try:
            img = cv2.imread(path)
        except Exception as e:
            print e
            continue

        recognize(img, cat, surf, centroids, linear_clf, ids)


def video_routine(recognize_file, training_folder):
    cam = cv2.VideoCapture(0)
    surf = cv2.SURF(250, extended=False)
    ids, linear_clf, centroids = loadObjects(training_folder)

    while True:
        _, frame = cam.read()
        recognize(frame, '', surf, centroids, linear_clf, ids)

        keypoints, descriptors = surf.detectAndCompute(frame, None)
        for k in keypoints:
            x, y = [int(i) for i in k.pt]
            size = k.size
            cv2.circle(frame, (x, y), 2, (0, 0, 255))

        cv2.imshow("Video", frame)
        if cv2.waitKey(33)==27:
            break


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: $python svm_recognize.py recognize_file training_folder"
        sys.exit(1)
    recognize_routine(sys.argv[1], sys.argv[2])
    #video_routine(sys.argv[1], sys.argv[2])
