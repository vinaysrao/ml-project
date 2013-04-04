import numpy
from scipy.cluster.vq import vq

import helpers
from helpers import FEATURE_TYPES


class Category:
    """
    This class represents one category that is encountered
    while training. It is used to calculate the bag of words
    vector, after all possible feature types are added to this
    category.
    """
    def __init__(self, label=None, features=None):
        self.label = label
        self.features = features
        self.bagofwords = []

    def add_feature(self, feature):
        """Add one feature vector from one image"""
        if self.features is None:
            self.features = []
        self.features.append(feature)

    def calc_bagofwords(self, centroids):
        """Calculate bag of words using the features
        added to an object."""
        for feature in self.features:
            labels, _ = vq(numpy.array(feature), centroids)
            bow = numpy.zeros(FEATURE_TYPES)
            for label in labels:
                bow[label] += 1
            helpers.normalize(bow)
            self.bagofwords.append(bow)