import cv2
import sys
import numpy as np

import helpers
from helpers import FEATURE_TYPES
from scipy.cluster.vq import kmeans2

def routine(inputfile, outputfolder):
    if outputfolder[-1] != '/':
        outputfolder += '/'
    features = []
    surf = cv2.SURF(250, extended=False)


    print "Extracting SURF features"
    for line in open(inputfile):
        category, path = line.strip().split(';')
        img = cv2.imread(path)
        keypoints, descriptors = surf.detectAndCompute(img, None)
        if descriptors is None:
            continue
        for d in descriptors:
            features.append(d)

    features = np.array(features)

    print "Performing kmeans on: ", features.shape
    centroids, labels = kmeans2(features, FEATURE_TYPES)

    return centroids

if __name__ == "__main__"
    if len(sys.argv) < 3:
        print "Usage: $python traincentroids.py inputfile outputfolder"
        sys.exit(1)
    inputfile = sys.argv[1]
    outputfolder = sys.argv[2]
    centroids = routine(inputfile, outputfolder)
    helpers.saveObject(centroids, outputfolder + 'centroids.txt')