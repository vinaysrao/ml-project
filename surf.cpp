#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/nonfree/nonfree.hpp"

#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

int main( int argc, char *argv[] )
{
    Mat img1, img2, displayImg;
    vector<KeyPoint> keypoints;
    Mat descriptors1, descriptors2;
    SurfFeatureDetector surf( 2500 );
    
    img1 = imread( argv[ 1 ], 0 );
    img2 = imread( argv[ 2 ], 0 );
    surf.detect( img1, keypoints );
    surf.compute( img1, keypoints, descriptors1 );
    
    surf.detect( img2, keypoints );
    surf.compute( img2, keypoints, descriptors2 );
    
    Size newsize;
    newsize.height = descriptors1.rows + descriptors2.rows;
    newsize.width = descriptors1.cols;
    Mat descriptors( newsize, descriptors1.type() );
    
    for( int i = 0; i < descriptors1.rows; i++ )
        for( int j = 0; j < descriptors1.cols; j++ )
            descriptors.at<float>( i, j ) = descriptors1.at<float>( i, j );
    
    for( int i = descriptors1.rows; i < descriptors.rows; i++ )
        for( int j = 0; j < descriptors.cols; j++ )
            descriptors.at<float>( i, j ) = descriptors2.at<float>( i - descriptors1.rows, j );
    
//     drawKeypoints( img, keypoints, displayImg, Scalar( 255, 255, 255 ), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );
    
//     namedWindow( "Image", 0 );
//     imshow( "Image", displayImg );
//     
//     waitKey();
    
    //Mat image( 500, 500, CV_8UC3 );
    Mat labels;
    const int clusterCount = 10;
    Mat centers( clusterCount, 1, descriptors.type() );
    
    kmeans( descriptors, clusterCount, labels, TermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 1.0 ), 3, KMEANS_PP_CENTERS, centers );
    
    int bagofwords[ 2 ][ clusterCount ];
    for( int i = 0; i < 2; i++ )
        for( int j = 0; j < clusterCount; j++ )
            bagofwords[ i ][ j ] = 0;
    
    int k = 0;
    for( int i = 0; i < labels.rows; i++ )
    {
        bagofwords[ k ][ labels.at<int>( i ) ]++;
        if( ( i + 1 ) == labels.rows / 2 )
            k = 1;
    }
    
    for( int i = 0; i < 2; cout.operator<<( endl ), i++ )
        for( int j = 0; j < clusterCount; j++ )
            cout << bagofwords[ i ][ j ] << ' ';
    
//     ofstream ofile( "descriptors.txt" );
//     for( int i = 0; i < descriptors.rows; i++ )
//     {
//         for( int j = 0; j < descriptors.cols; j++ )
//             ofile << descriptors.at<float>( i, j ) << ' ';
//         ofile << '\n';
//     }
//     ofile.close();
        
//     for( int i = 0; i < descriptors.rows; i++ )
//     {
//         int clusterIdx = labels.at<int>( i );
//         Point ipt = centers.at<Point2f>( i );
//         cout << ipt << '\t';
//         cout.flush();
//         circle( image, ipt, 2, colorTab[ clusterIdx ], CV_FILLED, CV_AA );
//     }
    
//     imshow("clusters", image );
    
//     waitKey();
    
    return 0;
}