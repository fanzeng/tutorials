#include <opencv2/opencv.hpp>
using namespace std;
int main(int argc, char** argv)
{
    char* imageName = argv[1];
    
    cv::Mat image;
    image = cv::imread(imageName, 1);
    
    if (argc != 2 || !image.data)
    {
        printf("No image data \n");
        return -1;
    }
    
    cout << "argv[0]=" << argv[0] << endl;
    cout << "argv[1]=" << argv[1] << endl;
    
    cv::Mat gray_image;
    cv::cvtColor(image, gray_image, cv::COLOR_BGR2GRAY);
    
    cout << cv::imwrite("./Gray_Image.jpg", gray_image) << endl;;
    
    cv::namedWindow(imageName, cv::WINDOW_AUTOSIZE);
    cv::namedWindow("Gray image", cv::WINDOW_AUTOSIZE);
    cv::imshow(imageName, image);
    cv::imshow("Gray image", gray_image);
    cv::waitKey(0);
    return 0;
    
}
