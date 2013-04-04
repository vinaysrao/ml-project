#!/usr/bin/python

import pickle
import sys

FEATURE_TYPES = 50  # Number of clusters features are put into; thus forming kinds of features. Usually sqrt(n/2)

def norm(array, p=2):
    """Returns the norm of the given array.
    p: The order of the norm, p = 2 by default.
    """
    return sum([i ** p for i in array]) ** 0.5


def normalize(array, p=2):
    """
    Normalizes a given array, i.e, divides each
    element of the array by the decided norm.
    Default: p = 2 (l2norm)
    """
    lpnorm = norm(array)
    for i in xrange(len(array)):
        array[i] = array[i] / lpnorm


def saveObject(object, file):
    """Uses pickle to dump an object onto the specified file."""
    try:
        f = open(file, 'w')
    except Exception as e:
        print e
        sys.exit(1)

    pickle.dump(object, f)
    f.close()
    print "Saved object to :", file


def loadObject(file):
    """Uses pickle to load an object from the given file."""
    try:
        f = open(file, 'r')
    except Exception as e:
        print e
        sys.exit(1)

    object = pickle.load(f)
    f.close()
    return object
