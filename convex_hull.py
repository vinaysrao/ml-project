#!/usr/bin/python

def cross_product( u, v, w ):
	return ( v[ 0 ] - u[ 0 ] ) * ( w[ 1 ] - u[ 1 ] ) - ( v[ 1 ] - u[ 1 ] ) * ( w[ 0 ] - u[ 0 ] )


def monotone_chain( xdata, ydata ):
	if len( xdata ) != len( ydata ):
		return

	points = []
	for i in range( len( xdata ) ): points.append( ( xdata[ i ], ydata[ i ] ) )

	points = sorted( points )

	lower = []
	for p in points:
		while len( lower ) >= 2 and cross_product( lower[ -2 ], lower[ -1 ], p ) <= 0:
			lower.pop()
		lower.append( p )

	upper = []
	for p in reversed( points ):
		while len( upper ) >= 2 and cross_product( upper[ -2 ], upper[ -1 ], p ) <= 0:
			upper.pop()
		upper.append( p )

	return lower + upper


if __name__ == '__main__':
	import matplotlib.pyplot as plt
	from random import randint
	# xdata = [ randint( 1, 100 ) for i in xrange( 25 ) ]
	# ydata = [ randint( 1, 100 ) for i in xrange( 25 ) ]
	from divplot import edgeConv
	import cv
	import sys
	edges = edgeConv( sys.argv[ 1 ] )
	xdata, ydata = [], []
	for j in xrange( edges.height ):
		for i in xrange( edges.width ):
			if edges[ j, i ] == 255:
				xdata.append( i )
				ydata.append( j )
	hull = monotone_chain( xdata, ydata )
	X = [ x[ 0 ] for x in hull ]
	Y = [ y[ 1 ] for y in hull ]

	from curve_fit import xWithY

	b = -( sum( [ x ** 2 for x in X ] ) - sum( [ y ** 2 for y in Y ] ) ) / ( 2 * sum( xWithY( X, Y ) ) )
	from math import sqrt
	x = [ b + sqrt( b ** 2 + 1 ), b - sqrt( b ** 2 + 1 ) ]
	y = [ 1, 1 ]
	plt.plot( X, Y, 'k', x, y, 'o' )
	plt.show()