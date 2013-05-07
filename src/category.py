import numpy
from scipy.cluster.vq import vq
import random
import numpy

import helpers
from helpers import FEATURE_TYPES


def get_features(features, n):
    from scipy.cluster.vq import kmeans2
    n = len(features) * n
    f_full = list()
    for feature in features:
        for f in feature:
            f_full.append(f)
    centroids, labels = kmeans2(numpy.array(f_full), n)
    return centroids


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
        self.bagofwords = list()

    def add_feature(self, feature):
        """Add one feature vector from one image"""
        if self.features is None:
            self.features = list()
        self.features.append(feature)

    def yield_features(self, n=20):
        """Yield a specific number of features for training.
        Defaults to n=10"""
        features = list()
        if n > len(self.features):
            n = len(self.features)
        features = get_features(self.features, n)
        #features = random.sample(self.features, n)
        return features

    def calc_bagofwords(self, centroids):
        """Calculate bag of words using the features
        added to an object."""
        for feature in self.features:
            try:
                labels, _ = vq(numpy.array(feature), centroids)
            except:
                continue
            bow = numpy.zeros(FEATURE_TYPES)
            for label in labels:
                bow[label] += 1
            helpers.normalize(bow)
            self.bagofwords.append(bow)