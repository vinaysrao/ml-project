#!/usr/bin/python

import sys
import cv2
from sklearn import svm
from scipy.cluster import kmeans2, vq
import numpy

import helpers

FEATURE_TYPES = 500

class Category:
    def __init__( self, label, features = [] ):
        self.label = label
        self.features = features
        self.bagofwords = []
    
    def add_feature( self, feature ):
        self.features.extend( feature )
    
    def calc_bagofwords( self, centroids ):
        for feature in self.features:
            labels, _ = vq( numpy.array( feature ), centroids )
            bow = numpy.zeros( FEATURE_TYPES )
            for label in labels:
                bow[ label ] += 1
            helpers.normalize( bow )
            self.bagofwords.append( bow )