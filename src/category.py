import numpy
from scipy.cluster.vq import vq

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
        self.bow = numpy.zeros(FEATURE_TYPES)
        self.n_features = 0

    def add_feature(self, feature, keypoints=None, shape=None):
        """Add one feature vector from one image"""
        if self.features is None:
            self.features = list()
        self.n_features += len(feature)
        if keypoints and shape:
            pass
            #print keypoints[0].pt
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

    def addBow(self, bow):
        for i in xrange(len(bow)):
            self.bow[i] += bow[i]

    def bowN(self, n=None):
        bow = self.bow.copy()
        if n is None:
            n = self.n_features
        for i in xrange(len(self.bow)):
            bow[i] /= n
        return bow

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
            self.addBow(bow)
            helpers.normalize(bow)
            self.bagofwords.append(bow)
