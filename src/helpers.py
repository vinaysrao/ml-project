#!/usr/bin/python

import pickle
import sys

def norm( array, p = 2 ):
    return sum( [ i ** p for i in array ] ) ** 0.5

def normalize( array ):
    l2norm = norm( array )
    for i in xrange( len( array ) ):
        array[ i ] = array[ i ] / l2norm

def saveObject( object, file ):
    try:
        f = open( file, 'w' )
    except Exception as e:
        print e
        sys.exit( 1 )
    
    pickle.dump( object, f )
    f.close()
    print "Saved object to :", file