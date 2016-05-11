/*
 * DisplayImage.cpp
 *
 *  Created on: 13 mar 2016
 *      Author: alvis
 */

#include <opencv2/opencv.hpp>
#include <vector>
using namespace cv;

/**
 * Perform one thinning iteration.
 * Normally you wouldn't call this function directly from your code.
 *
 * @param  im    Binary image with range = 0-1
 * @param  iter  0=even, 1=odd
 */
void thinningIteration(cv::Mat& im, int iter)
{
    cv::Mat marker = cv::Mat::zeros(im.size(), CV_8UC1);

    for (int i = 1; i < im.rows-1; i++)
    {
        for (int j = 1; j < im.cols-1; j++)
        {
            uchar p2 = im.at<uchar>(i-1, j);
            uchar p3 = im.at<uchar>(i-1, j+1);
            uchar p4 = im.at<uchar>(i, j+1);
            uchar p5 = im.at<uchar>(i+1, j+1);
            uchar p6 = im.at<uchar>(i+1, j);
            uchar p7 = im.at<uchar>(i+1, j-1);
            uchar p8 = im.at<uchar>(i, j-1);
            uchar p9 = im.at<uchar>(i-1, j-1);

            int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) +
                     (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) +
                     (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
                     (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
            int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            int m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            int m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);

            if (A == 1 && (B >= 2 && B <= 6) && m1 == 0 && m2 == 0)
                marker.at<uchar>(i,j) = 1;
        }
    }

    im &= ~marker;
}

/**
 * Function for thinning the given binary image
 *
 * @param  im  Binary image with range = 0-255
 */
void thinning(cv::Mat& im)
{
    im /= 255;

    cv::Mat prev = cv::Mat::zeros(im.size(), CV_8UC1);
    cv::Mat diff;

    int i = 2;

    do {
        thinningIteration(im, 0);
        thinningIteration(im, 1);
        cv::absdiff(im, prev, diff);
        im.copyTo(prev);
        i--;
    }
    //while (cv::countNonZero(diff) > 0);
    while (i > 0);

    im *= 255;
}

int main(int argc, char** argv) {
	Mat inputImage = imread(argv[1]);
	if (!inputImage.data)
	    {
	        std::cout << "Image not loaded";
	        return -1;
	    }
	//imshow("Input Image", inputImage);

	Mat gray, thre, ero, dil, dst;
	cvtColor(inputImage, gray, CV_BGR2GRAY);
	//threshold(gray, thre, 120, 255, 0 );
	adaptiveThreshold(~gray, thre, 255, CV_ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 15, -2);
	int erosion_type = MORPH_CROSS;
	int erosion_size = 5;
	Mat element = getStructuringElement( erosion_type, Size( 2*erosion_size +1, 2*erosion_size+1 ), Point( erosion_size, erosion_size ) );

	  /// Apply the erosion operation
	//erode(thre, ero, element );
	morphologyEx(thre, ero, MORPH_CLOSE, element );
	//thinning(ero);

	int erosion_type2 = MORPH_ELLIPSE;
	int erosion_size2 = 3;
	Mat element2 = getStructuringElement( erosion_type2, Size( 2*erosion_size2 +1, 2*erosion_size2+1 ), Point( erosion_size2, erosion_size2 ) );
	morphologyEx(ero, dst, MORPH_OPEN, element2 );

	int scale = 1;
	int delta = 0;
	int ddepth = CV_16S;
	Mat grad_x, grad_y;
	Mat abs_grad_x, abs_grad_y;

	/// Gradient X
	Sobel( dst, grad_x, ddepth, 1, 0, 3, scale, delta, BORDER_DEFAULT );
	/// Gradient Y
	Sobel( dst, grad_y, ddepth, 0, 1, 3, scale, delta, BORDER_DEFAULT );
	//convertScaleAbs( grad_x, abs_grad_x );
	//convertScaleAbs( grad_y, abs_grad_y );
	//addWeighted( abs_grad_x, 0.5, abs_grad_y, 0.5, 0, dst );

	//int dilation_type = MORPH_ELLIPSE;
	//int dilation_size = 5;
	//Mat element2 = getStructuringElement( dilation_type, Size( 2*dilation_size + 1, 2*dilation_size+1 ), Point( dilation_size, dilation_size ) );
	  /// Apply the dilation operation
	//int kernel_size = 5;
	//float kernel_data[25] = {-1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1};
	//Mat kernel = cv::Mat(kernel_size, kernel_size, CV_32F, kernel_data);
	//dilate(ero, dil, element2 );
	blur( dst, dst, Size(1,3) );
	//Canny( dst, dst, 50, 300, 3 );
	//GaussianBlur( dil, dst, Size(1,1), 0, 0 );
	//Sobel( src_gray, grad_x, ddepth, 1, 0, 3, scale, delta, BORDER_DEFAULT );

	//int kernel_size = 5;
	//float kernel_data[25] = {-1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1};
	//Mat kernel = cv::Mat(kernel_size, kernel_size, CV_32F, kernel_data);
	//erode(dil, dst, kernel );

	Mat cdst;
	cvtColor(dst, cdst, CV_GRAY2BGR);
	//std::vector<Vec2f> lines;
	// detect lines
//	HoughLines(dst, lines, 1, CV_PI/180, 150, 0, 0 );
//	std::cout << lines.size() << std::endl;
//	for( size_t i = 0; i < lines.size(); i++ )
//	    {
//	        float rho = lines[i][0], theta = lines[i][1];
//	        if( theta>CV_PI/180*170 || theta<CV_PI/180*10) {
//	        	Point pt1, pt2;
//	    	    double a = cos(theta), b = sin(theta);
//	    	    double x0 = a*rho, y0 = b*rho;
//	    	    pt1.x = cvRound(x0 + 1000*(-b));
//	    	    pt1.y = cvRound(y0 + 1000*(a));
//	    	    pt2.x = cvRound(x0 - 1000*(-b));
//	    	    pt2.y = cvRound(y0 - 1000*(a));
//	    	    line(cdst, pt1, pt2, Scalar(0,0,255), 3, CV_AA);
//	        }
//
//	    }

    std::vector<Vec4i> lines;
    HoughLinesP( dst, lines, 1, CV_PI/180, 80, 30, 5);
    std::cout << lines.size() << std::endl;
    for( size_t i = 0; i < lines.size(); i++ )
    {
        line( cdst, Point(lines[i][0], lines[i][1]), Point(lines[i][2], lines[i][3]), Scalar(0,0,255), 5, CV_AA);
        //Vec4i l = lines[i];
        //line(cdst, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(255), 5, CV_AA);
    }

    std::string cat_name(argv[2]);
	imwrite(cat_name + std::string("dst.jpg"), dst);
	imwrite(cat_name + "cdst.jpg", cdst);
	imwrite(cat_name + "thre.jpg", thre);
	imwrite(cat_name + "ero.jpg", ero);
	imwrite(cat_name + "dil.jpg", dil);
	imwrite(cat_name + "grey.jpg", gray);

	//imshow("detected lines", cdst);
	//waitKey(0);
	std::cout << "SIALALLALA" << std::endl;
	return 0;
}



