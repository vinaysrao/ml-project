#!/usr/bin/python

from numpy import linalg
from numpy import matrix


def xWithY( xdata, ydata ):
	xwithy = []
	l = len( xdata )
	for i in xrange( l ):
		xwithy.append( xdata[ i ] * ydata[ i ] )
	return xwithy


def fitQuadratic( xdata, ydata ):
	'''
	Uses method of least squares to find a, b, c to 
	fit into a quadratic of the form a.x^2 + b.x + c
	'''

	if len( xdata ) != len( ydata ):
		return
	yi = sum( ydata )
	xiyi = sum( xWithY( xdata, ydata ) )
	xi2yi = sum( xWithY( [ i ** 2 for i in xdata ], ydata ) )

	x = []
	for i in xrange( 1, 5 ):
		x.append( sum( [ j ** i for j in xdata ] ) )

	A = matrix( [ [ len( xdata ), x[ 0 ], x[ 1 ] ], x[ 0 : 3 ], x[ 1 : ] ] )
	X = [ yi, xiyi, xi2yi ]

	a, b, c = linalg.solve( A, X )
	return ( c, b, a )


def fitLinear( xdata, ydata ):
	'''
	Finds a, b to fit into a line of form a.x + b
	'''
	if len( xdata ) != len( ydata ):
		return
	yi = sum( ydata )
	xiyi = sum( xWithY( xdata, ydata ) )
	x = []
	for i in xrange( 1, 3 ):
		x.append( sum( [ j ** i for j in xdata ] )  )

	A = matrix( [ [ len( xdata ), x[ 0 ] ], x ] )
	X = [ yi, xiyi ]

	a, b = linalg.solve( A, X )
	return ( b, a )


def yForX( x, abc ):
	try:
		a, b, c = abc
		return a * ( x ** 2 ) + b * x + c
	except:
		a, b = abc
		return a * x + b

if __name__ == '__main__': #Then show this example
	import matplotlib.pyplot as plt
	from numpy import arange

	xdata = [ 1, 2, 3, 4, 5, 6, 7 ]
	ydata = [ 1, 4, 8, 17, 25, 31, 50 ]

	abc = fitQuadratic( xdata, ydata )
	print abc

	X = arange( min( xdata ), max( xdata ) + 1 )
	Y = [ yForX( x, abc ) for x in X ]

	ab = fitLinear( xdata, ydata )
	Y2 = [ yForX( x, ab ) for x in X ]
	plt.plot( xdata, ydata, 'o', X, Y, 'k', X, Y2 )

	plt.show()
