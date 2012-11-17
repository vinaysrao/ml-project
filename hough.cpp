#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <string>


using namespace cv;
using namespace std;

int main( int argc, char *argv[] )
{
	const char *filename = argv[ 1 ];

	Mat src = imread( filename, 0 );
	if( src.empty() )
	{
		cout << "Can't open " << filename << endl;
		return 1;
	}

	Mat dst, cdst;
	for( int iter = 0; iter < 5; iter++ )
	{
		Canny( src, dst, 50 + ( iter * 50 ), 750, 3 );
		cvtColor( dst, cdst, CV_GRAY2BGR );

		vector<Vec4i> lines;
		HoughLinesP( dst, lines, 1, CV_PI/180, 50, 50, 10 );
		for( size_t i = 0; i < lines.size(); i++ )
		{
			Vec4i l = lines[ i ];
			line( cdst, Point( l[ 0 ], l[ 1 ] ), Point( l[ 2 ], l[ 3 ] ), Scalar( 0, 0, 255 ), 3, CV_AA );
		}

		vector<int> compression_params;
	    compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
	    compression_params.push_back(9);

	    stringstream s;
	    s << iter;
		imwrite( s.str() + string( ".png" ), cdst, compression_params );
	}

	waitKey();

	return 0;
}