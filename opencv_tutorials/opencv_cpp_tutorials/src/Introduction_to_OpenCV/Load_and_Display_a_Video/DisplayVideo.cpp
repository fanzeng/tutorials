#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/videoio.hpp>
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
int main(int argc, char **argv)
{
    // Open camera with CAMERA_INDEX (webcam is typically #0).
    const int CAMERA_INDEX = 0;
 
    // cv::VideoCapture capture(CAMERA_INDEX);
    std::string filename = "/media/fzeng/Data/Codes/PycharmProjects/Practice/opencv_tutorials/samples/768x576.avi";
    cv::VideoCapture capture(filename);
 
    if(not capture.isOpened())
    {
        std::cout << "Failed to open camera with index " << CAMERA_INDEX << "!" << std::endl;
    }
 
    cv::Mat frame;  
    // std::cout << capture.read(frame) << std::endl; // Read one frame. If successful, will print out '1'.
    while(1)
    {
        capture >> frame;
        if (frame.empty())
            break;
        cv::namedWindow("Display window", cv::WINDOW_AUTOSIZE);
        cv::imshow("Display window", frame);
        cv::waitKey(3); // Wait for a keystroke in the window
    
    }
       
    capture.release();
    return 0;

}


