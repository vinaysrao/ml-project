#!/usr/bin/python

import pickle

def norm( array, p = 2 ):
    return sum( [ i ** p for i in array ] ) ** 0.5

def normalize( array ):
    l2norm = norm( array )
    for i in xrange( len( array ) ):
        array[ i ] = array[ i ] / l2norm