#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>

void Sharpen(const cv::Mat& myImage, cv::Mat& Result)
{
    CV_Assert(myImage.depth() == CV_8U);
    Result.create(myImage.size(), myImage.type());
    const int nChannels = myImage.channels();
    for (int j = 1; j < myImage.rows - 1; ++j)
    {
        const uchar* previous = myImage.ptr<uchar>(j - 1);
        const uchar* current = myImage.ptr<uchar>(j);
        const uchar* next = myImage.ptr<uchar>(j + 1);
        
        uchar* output = Result.ptr<uchar>(j);
        
        for (int i = nChannels; i < nChannels * (myImage.cols - 1); ++i)
        {
            *output++ = cv::saturate_cast<uchar>(5 * current[i] - current[i - nChannels] - current[i + nChannels] - previous[i] - next[i]);
        }
        Result.row(0).setTo(cv::Scalar(0));
        Result.row(Result.rows - 1).setTo(cv::Scalar(0));
        Result.col(0).setTo(cv::Scalar(0));
        Result.col(Result.cols - 1).setTo(cv::Scalar(0));
    }
}
int main(int argc, char** argv)
{
    cv::Mat img = cv::imread("../../../samples/HappyFish.jpg");
    cv::Mat Result;
    Sharpen(img, Result);
    cv::namedWindow("Sharpen", cv::WINDOW_AUTOSIZE);
    cv::imshow("Sharpen", Result);
    cv::waitKey();
    
    cv::Mat kern = (cv::Mat_<char>(3, 3) << 0, -1, 0,   -1, 5, -1,   0, -1, 0);
    cv::filter2D(img, Result, img.depth(), kern);
    cv::namedWindow("Sharpen1", cv::WINDOW_AUTOSIZE);
    cv::imshow("Sharpen1", Result);
    cv::waitKey();
    return 0;
}