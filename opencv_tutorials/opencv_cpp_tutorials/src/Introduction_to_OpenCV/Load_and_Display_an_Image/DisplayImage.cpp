#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <string>
using namespace std;

int main(int argc, char** argv)
{
    string imageName("/media/fzeng/DATA/PycharmProjects/Practice/opencv_tutorials/samples/HappyFish.jpg"); // default image;
    if (argc > 1)
    {
        imageName = argv[1];
    }

    cv::Mat image;
    image = cv::imread(imageName.c_str(), cv::IMREAD_COLOR); // Read the file

    if (image.empty())
    {
        cout << "SoCould not open or find the image" << endl;
        return -1;
    }
    
    cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
    cv::imshow("Display window", image);
    cv::waitKey(0); // Wait for a keystroke in the window
    return 0;
}
