#!/usr/bin/python

import sys
import cv2
from scipy.cluster.vq import vq
import numpy

import helpers
from category import Category


def recognize_routine(recognize_file, training_folder):
    surf = cv2.SURF(250)

    if training_folder[-1] != '/':
        training_folder += '/'

    ids = helpers.loadObject(training_folder + 'ids.txt')
    linear_clf = helpers.loadObject(training_folder + 'svm.txt')
    centroids = helpers.loadObject(training_folder + 'centroids.txt')

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

        keypoints, descriptors = surf.detectAndCompute(img, None)

        category = Category(label=cat)
        category.add_feature(descriptors)
        category.calc_bagofwords(centroids)

        bow = category.bagofwords[0]
        id = int(linear_clf.predict(bow)[0])
        for i in ids:
            if ids[i] == id:
                label = i
        print category.label, ":", label


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: $python svm_recognize.py recognize_file training_folder"
        sys.exit(1)

    recognize_routine(sys.argv[1], sys.argv[2])
