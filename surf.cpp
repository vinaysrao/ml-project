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
    Mat img, displayImg;
    vector<KeyPoint> keypoints;
    Mat descriptors;
    SurfFeatureDetector surf( 2500 );
    
    img = imread( argv[ 1 ], 0 );
    surf.detect( img, keypoints );
    surf.compute( img, keypoints, descriptors );
    
    drawKeypoints( img, keypoints, displayImg, Scalar( 255, 255, 255 ), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );
    imshow( "Image", displayImg );
    
    waitKey();
    
    Mat image( 500, 500, CV_8UC3 );
    Mat labels;
    int clusterCount = 5;
    Mat centers( clusterCount, 1, descriptors.type() );
    
    kmeans( descriptors, clusterCount, labels, TermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 1.0 ), 3, KMEANS_PP_CENTERS, centers );
    
    for( int i = 0; i < labels.rows; i++ )
        cout << labels.at<int>( i ) << " ";
    
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