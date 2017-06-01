#include <opencv2/opencv.hpp>
#include <iostream>

#define w 400

void MyLine(cv::Mat img, cv::Point start, cv::Point end)
{
    int thickness = 2;
    int lineType = 8;
    cv::line(img, start, end, cv::Scalar(0, 0, 0), thickness, lineType);
}

void MyEllipse(cv::Mat img, double angle)
{
    int thickness = 2;
    int lineType = 8;
    cv::ellipse(img, cv::Point(w/2.0, w/2.0), cv::Size(w/4.0, w/16.0), angle, 0, 360, cv::Scalar(255, 0, 0), thickness, lineType);
}

void MyFilledCircle(cv::Mat img, cv::Point center)
{
    int thickness = -1;
    int lineType = 8;
    
    cv::circle(img, center, w/32.0, cv::Scalar(0, 0, 255), thickness, lineType);
}

void MyPolygon(cv::Mat img)
{
    int lineType = 8;
    cv::Point rook_points[1][20];
    rook_points[0][0]  = cv::Point(    w/4,   7*w/8 );
    rook_points[0][1]  = cv::Point(  3*w/4,   7*w/8 );
    rook_points[0][2]  = cv::Point(  3*w/4,  13*w/16 );
    rook_points[0][3]  = cv::Point( 11*w/16, 13*w/16 );
    rook_points[0][4]  = cv::Point( 19*w/32,  3*w/8 );
    rook_points[0][5]  = cv::Point(  3*w/4,   3*w/8 );
    rook_points[0][6]  = cv::Point(  3*w/4,     w/8 );
    rook_points[0][7]  = cv::Point( 26*w/40,    w/8 );
    rook_points[0][8]  = cv::Point( 26*w/40,    w/4 );
    rook_points[0][9]  = cv::Point( 22*w/40,    w/4 );
    rook_points[0][10] = cv::Point( 22*w/40,    w/8 );
    rook_points[0][11] = cv::Point( 18*w/40,    w/8 );
    rook_points[0][12] = cv::Point( 18*w/40,    w/4 );
    rook_points[0][13] = cv::Point( 14*w/40,    w/4 );
    rook_points[0][14] = cv::Point( 14*w/40,    w/8 );
    rook_points[0][15] = cv::Point(    w/4,     w/8 );
    rook_points[0][16] = cv::Point(    w/4,   3*w/8 );
    rook_points[0][17] = cv::Point( 13*w/32,  3*w/8 );
    rook_points[0][18] = cv::Point(  5*w/16, 13*w/16 );
    rook_points[0][19] = cv::Point( w/4, 13*w/16 );
    
    const cv::Point* ppt[1] = {rook_points[0]};
    int npt[] = {20};
    
    cv::fillPoly(img, ppt, npt, 1, cv::Scalar(255, 255, 255), lineType);
}

int main(int argc, char** argv)
{
    cv::Point pt;
    pt.x = 10;
    pt.y = 8;
    std::cout << pt << std::endl;
    cv::Point pt_1 = cv::Point(10, 8);
    std::cout << pt << std::endl;
    
    char atom_window[] = "Drawing 1: Atom";
    char rook_window[] = "Drawing 2: Rook";
    
    cv::Mat atom_image = cv::Mat::zeros(w, w, CV_8UC3);
    cv::Mat rook_image = cv::Mat::zeros(w, w, CV_8UC3);
    
    MyEllipse(atom_image, 90);
    MyEllipse(atom_image, 0);
    MyEllipse(atom_image, 45);
    MyEllipse(atom_image, -45);

    MyFilledCircle(atom_image, cv::Point(w/2.0, w/2.0));
    
    MyPolygon(rook_image);
    cv::rectangle(rook_image, cv::Point(0, 7*w/8.0), cv::Point(w, w), cv::Scalar(0, 255, 255), -1, 8);
    MyLine(rook_image, cv::Point(0, 15*w/16), cv::Point(w, 15*w/16));
    MyLine(rook_image, cv::Point(w/4, 7*w/8), cv::Point(w/4, w));
    MyLine(rook_image, cv::Point(w/2, 7*w/8), cv::Point(w/2, w));
    MyLine(rook_image, cv::Point(3*w/4, 7*w/8), cv::Point(3*w/4, w));   
    
    cv::imshow(atom_window, atom_image);
    cv::moveWindow(atom_window, 0, 200);
    cv::imshow(rook_window, rook_image);
    cv::moveWindow(rook_window, w, 200);

    cv::waitKey(0);

    
    return 0;
}