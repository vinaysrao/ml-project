#!/usr/bin/python

from numpy import linalg
from numpy import matrix
import sys


def xWithY( xdata, ydata, xpower = 1 ):
	xwithy = []
	l = len( xdata )
	for i in xrange( l ):
		xwithy.append( ( xdata[ i ] ** xpower ) * ydata[ i ] )
	return xwithy


def fitPolynomial( xdata, ydata, order ):
	"""Fit a polynomial of the given order
	that matches the given x and y coordinates.
	This function takes the x and y coordinates
	separately, and their length must match.
	"""
	assert( len( xdata ) == len( ydata ) )

	X = []
	for i in range( order + 1 ):
		X.append( sum( xWithY( xdata, ydata, xpower = i ) ) )
	
	from numpy import zeros
	A = zeros( ( order + 1, order + 1 ) )
	del zeros

	for i in xrange( order + 1 ):
		for j in xrange( order + 1 ):
			if ( i - 1 ) >= 0 and ( j + 1 ) <= order:
				A[ i ][ j ] = A[ i - 1 ][ j + 1 ]
			else:
				k = i + j
				A[ i ][ j ] = sum( [ x ** k for x in xdata ] )
	A[ 0 ][ 0 ] = len( xdata )
	result = linalg.solve( A, X )
	return result


def yForX( x, consts, order = 2 ):
	y = 0
	for i in xrange( order, -1, -1 ):
		y += ( ( x ** i ) * consts[ i ] )
	return y

if __name__ == '__main__': #Then show this example
	import matplotlib.pyplot as plt
	from numpy import arange

	xdata = [ 1, 2, 3, 4, 5, 6, 7 ]
	ydata = [ 1, 4, 8, 17, 25, 31, 50 ]
	abc = fitPolynomial( xdata, ydata, 4 )
	print abc

	X = arange( min( xdata ), max( xdata ) + 1 )
	Y = [ yForX( x, abc, 4 ) for x in X ]

	plt.plot( xdata, ydata, 'o', X, Y, 'k' )

	plt.show()