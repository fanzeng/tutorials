#include <opencv2/opencv.hpp>
#include <iostream>

double alpha;
int beta;

int main(int argc, char** argv)
{
    cv::Mat image = cv::imread(argv[1]);
    cv::Mat new_image = cv::Mat::zeros(image.size(), image.type());
    std::cout << "Basic Linear Transforms" << std::endl;
    std::cout << "-----------------------" << std::endl;
    std::cout << "Enter the alpha value [1.0-3.0]:"; std::cin >> alpha;
    std::cout << "Enter the beta value [0-100]:"; std::cin >> beta;
    
    for (int y = 0; y < image.rows; y++)
    {
        for (int x = 0; x < image.cols; x++)
        {
            for (int c = 0; c < 3; c++)
            {
                new_image.at<cv::Vec3b>(y, x)[c] = cv::saturate_cast<uchar>(alpha * (image.at<cv::Vec3b>(y, x)[c]) + beta);
            }
        }
    }
    
    cv::namedWindow("Original Image", cv::WINDOW_AUTOSIZE);

    
    cv::imshow("Original Image", image);
    cv::waitKey();
    cv::namedWindow("New Image", cv::WINDOW_AUTOSIZE);
    cv::imshow("New Image", new_image);
    cv::waitKey();
    
    return 0;
}