from cv2 import SURF, imread
import sys
from scipy.cluster.vq import kmeans2, vq
from sklearn import svm
import numpy

features = []

for im in open( sys.argv[ 1 ] ):
    img = imread( im.strip() )
    
    surf = SURF( 500 )
    keypoints, descriptors = surf.detectAndCompute( img, None )
    
    features.extend( descriptors )
    
    #for k in keypoints:
        #x, y = [ int( y ) for y in k.pt ]
        #circle( img, ( x, y ), 2, ( 0, 0, 255 ) )
    #imshow( "Features", img )
    #waitKey()
np_features = numpy.array( features )
centroids, labels = kmeans2( np_features, 50 )
print labels

counter = 1
X = []
Y = []

for im in open( sys.argv[ 1 ] ):
    counts = numpy.zeros( 50 )
    img = imread( im.strip() )
    k, d = surf.detectAndCompute( img, None )
    labels, _ = vq( numpy.array( d ), centroids )
    for i in labels:
        counts[ i ] += 1
    X.append( counts.tolist() )
    Y.append( counter )
    counter += 1
    
lin_clf = svm.LinearSVC()
lin_clf.fit( X, Y )

print lin_clf.predict( X[ 3 ] )