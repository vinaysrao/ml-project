#!/usr/bin/python

from PIL import Image
import sys

Image.open( sys.argv[ 1 ] ).filter( __import__( 'ImageFilter' ).FIND_EDGES ).save( 'edge.jpg' )