#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
int main(int argc, char** argv)
{
    cv::Mat img = cv::imread("/home/fzeng/build/HappyFish.jpg", 0);
    cv::imwrite("/home/fzeng/build/HappyFish.png", img);
    cv::Scalar intensity = img.at<uchar>(3, 2);
    std::cout << "Gray: " << intensity.val[0] << std:: endl;
    intensity = img.at<uchar>(cv::Point(3, 2));
    std::cout << "Gray: " << intensity[0] << std::endl;
    
    img = cv::imread("/home/fzeng/build/HappyFish.jpg");
    cv::Vec3b intensity1 = img.at<cv::Vec3b>(3, 2);
    uchar blue = intensity1.val[0];
    uchar green = intensity1.val[1];
    uchar red = intensity1.val[2];
    std::cout << "BGR: " << int(blue) << ", " << int(green) << ", " << int(red) << std::endl;
    
    std::vector<cv::Point3f> points;
    points.push_back(cv::Point3f(0, 1, 2));
    points.push_back(cv::Point3f(3, 4, 5));
    points.push_back(cv::Point3f(6, 7, 8));
    std::cout << points << std::endl;
//    cv::Mat pointsMat = cv::Mat(points);
//    std::cout << pointsMat << std::endl;
    cv::Mat pointsMat = cv::Mat(points).reshape(1);
    std::cout << pointsMat << std::endl;
    
    // Make a black image
    img = cv::Scalar(0);
    cv::Rect r(10, 10, 100, 100);
    cv::Mat smallImg = img(r);
    cv::namedWindow("smallImg", cv::WINDOW_AUTOSIZE);
    cv::imshow("smallImg", smallImg);
    cv::waitKey();
    
    cv::Mat img1 = cv::imread("/home/fzeng/build/HappyFish.jpg");
    cv::Mat grey;
    cv::cvtColor(img1, grey, cv::COLOR_BGR2GRAY);
    cv::Mat sobelx;
    cv::Sobel(grey, sobelx, CV_32F, 1, 0);
    double minVal, maxVal;
    cv::minMaxLoc(sobelx, &minVal, &maxVal);
    cv::Mat draw;
    sobelx.convertTo(draw, CV_8U, 255.0/(maxVal - minVal), -minVal*255.0/(maxVal - minVal));
    cv::namedWindow("draw", cv::WINDOW_AUTOSIZE);
    cv::imshow("draw", draw);
    cv::waitKey();
    return 0;
}