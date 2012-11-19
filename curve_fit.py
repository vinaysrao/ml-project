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

	c, b, a = linalg.solve( A, X )
	return ( a, b, c )


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

	b, a = linalg.solve( A, X )
	return ( a, b )


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

	xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 2, 19, 20, 0, 1, 21, 22, 23, 4, 5, 6, 7, 24, 25, 26, 7, 8, 9, 10, 26, 27, 28, 1, 3, 4, 5, 11, 12, 13, 28, 29, 30, 1, 2, 5, 14, 15, 16, 17, 30, 31, 32, 0, 3, 4, 5, 17, 18, 19, 20, 32, 33, 20, 21, 22, 23, 24, 27, 28, 33, 34, 24, 25, 26, 34, 35, 0, 1, 2, 3, 4, 5, 26, 27, 28, 29, 35, 29, 35, 30, 31, 35, 24, 26, 27, 28, 29, 31, 32, 35, 36, 24, 25, 32, 33, 34, 36, 36, 36, 36, 36, 36, 36, 11, 37, 8, 9, 10, 37, 0, 1, 2, 3, 4, 5, 7, 37, 6, 7, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 19, 20, 21, 22, 23, 36, 19, 23, 24, 36, 19, 24, 36, 18, 19, 24, 36, 18, 21, 24, 36, 18, 19, 21, 22, 23, 24, 36, 19, 20, 21, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36]
#[ 1, 2, 3, 4, 5, 6, 7 ]
	ydata = [30, 30, 30, 30, 30, 30, 31, 31, 31, 31, 31, 32, 32, 32, 32, 32, 33, 33, 33, 34, 34, 34, 35, 35, 35, 35, 35, 36, 36, 36, 36, 36, 36, 36, 37, 37, 37, 37, 37, 37, 37, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 44, 44, 45, 45, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 47, 47, 47, 47, 48, 49, 50, 51, 52, 53, 54, 54, 55, 55, 55, 55, 56, 56, 56, 56, 56, 56, 56, 56, 57, 57, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 82, 82, 82, 82, 82, 83, 83, 83, 83, 84, 84, 84, 85, 85, 85, 85, 86, 86, 86, 86, 87, 87, 87, 87, 87, 87, 87, 88, 88, 88, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]#[ 1, 4, 8, 17, 25, 31, 50 ]
	print len(xdata),len(ydata)
	abc = fitQuadratic( xdata, ydata )
	print abc

	X = arange( min( xdata ), max( xdata ) + 1 )
	Y = [ yForX( x, abc ) for x in X ]

	plt.plot( xdata, ydata, 'o', X, Y, 'k' )

	plt.show()